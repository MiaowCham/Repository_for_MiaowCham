import argparse
import os
import re
import xml.etree.ElementTree as ET
from collections import OrderedDict

TTML_NS = "http://www.w3.org/ns/ttml"
TTM_NS = "http://www.w3.org/ns/ttml#metadata"
ITUNES_NS = "http://music.apple.com/lyric-ttml-internal"
XML_NS = "http://www.w3.org/XML/1998/namespace"

ET.register_namespace("", TTML_NS)
ET.register_namespace("ttm", TTM_NS)
ET.register_namespace("xml", XML_NS)
ET.register_namespace("itunes", ITUNES_NS)


def normalize_time_value(value: str) -> str:
    if ":" not in value:
        return value
    parts = value.split(":")
    if parts[0] == "00":
        parts = parts[1:]
    else:
        parts[0] = str(int(parts[0])) if parts[0].isdigit() else parts[0].lstrip("0") or "0"
    return ":".join(parts)


def normalize_time_attributes(element: ET.Element):
    for attr_name, attr_value in list(element.attrib.items()):
        if attr_name in {"begin", "end", "dur"}:
            element.attrib[attr_name] = normalize_time_value(attr_value)


def collect_translations(root: ET.Element):
    """
    返回字典 mapping itunes_key -> (main_translation, bg_translation)
    bg_translation 来自于被 ttm:role="x-bg" 包裹的 x-translation
    同时会从树中移除这些 x-translation 节点，并删除 x-bg 标签的 begin/end 属性
    """
    translations = {}
    p_tag = f"{{{TTML_NS}}}p"
    span_tag = f"{{{TTML_NS}}}span"
    role_attr = f"{{{TTM_NS}}}role"
    key_attr = f"{{{ITUNES_NS}}}key"

    for p in root.findall(f".//{p_tag}"):
        itunes_key = p.attrib.get(key_attr)
        if not itunes_key:
            continue

        main_frags = []
        bg_frags = []

        def traverse(parent: ET.Element):
            for child in list(parent):
                # 如果是 x-bg 的容器，先去掉其 begin/end，然后继续深入查找其中的 x-translation
                if child.tag == span_tag and child.attrib.get(role_attr) == "x-bg":
                    # 删除 begin/end 属性
                    for a in ("begin", "end"):
                        if a in child.attrib:
                            del child.attrib[a]
                    # 继续遍历子节点以寻找其中的 x-translation，并保留其他 lyric span
                    traverse(child)
                # 若为翻译节点，依据父节点是否为 x-bg 来分类
                elif child.tag == span_tag and child.attrib.get(role_attr) == "x-translation":
                    text = "".join(child.itertext()).strip()
                    # 判断 parent 是否为 x-bg
                    if parent is not None and parent.attrib.get(role_attr) == "x-bg":
                        if text:
                            bg_frags.append(text)
                    else:
                        if text:
                            main_frags.append(text)
                    # 从父节点移除该翻译节点
                    parent.remove(child)
                else:
                    traverse(child)

        traverse(p)

        # 合并为字符串
        main_text = " ".join(f for f in main_frags if f).strip()
        bg_text = " ".join(f for f in bg_frags if f).strip()

        if main_text or bg_text:
            translations[itunes_key] = (main_text, bg_text)

        reorder_p_attributes(p, key_attr)

    return translations


def reorder_p_attributes(p: ET.Element, key_attr_name: str):
    agent_attr_name = f"{{{TTM_NS}}}agent"
    if key_attr_name not in p.attrib or agent_attr_name not in p.attrib:
        return

    items = list(p.attrib.items())
    reordered = []
    for name, value in items:
        if name in {key_attr_name, agent_attr_name}:
            continue
        reordered.append((name, value))
    reordered.append((key_attr_name, p.attrib[key_attr_name]))
    reordered.append((agent_attr_name, p.attrib[agent_attr_name]))

    p.attrib.clear()
    p.attrib.update(OrderedDict(reordered))


def ensure_itunes_translation_metadata(root: ET.Element, translations):
    head = root.find(f"{{{TTML_NS}}}head")
    if head is None:
        head = ET.SubElement(root, f"{{{TTML_NS}}}head")

    metadata = head.find(f"{{{TTML_NS}}}metadata")
    if metadata is None:
        metadata = ET.SubElement(head, f"{{{TTML_NS}}}metadata")

    # 查找或创建一个不带前缀的 iTunesMetadata 元素，并在其上声明默认 itunes 命名空间
    itunes_meta = None
    for child in metadata:
        tag = child.tag
        if isinstance(tag, str) and tag.endswith("}iTunesMetadata") or tag == "iTunesMetadata":
            itunes_meta = child
            break

    if itunes_meta is None:
        itunes_meta = ET.SubElement(metadata, "iTunesMetadata")
        itunes_meta.set("xmlns", ITUNES_NS)

    translations_el = itunes_meta.find("translations")
    if translations_el is None:
        translations_el = ET.SubElement(itunes_meta, "translations")

    translation_el = None
    for candidate in translations_el.findall("translation"):
        if candidate.get("type") == "subtitle" and candidate.get(f"{{{XML_NS}}}lang") == "zh-Hans-CN":
            translation_el = candidate
            break

    if translation_el is None:
        translation_el = ET.SubElement(
            translations_el,
            "translation",
            {
                "type": "subtitle",
                f"{{{XML_NS}}}lang": "zh-Hans-CN",
            },
        )
    else:
        for child in list(translation_el):
            translation_el.remove(child)

    for key, pair in translations.items():
        main_text, bg_text = pair
        text_el = ET.SubElement(translation_el, "text", {"for": key})
        # 主翻译文本放在 text 节点的文本中
        if main_text:
            text_el.text = main_text
        else:
            text_el.text = ""

        # 若存在来自 x-bg 的翻译，则在 text 节点下加入一个不带前缀的 span，并在该 span 上声明 TTML 命名空间和 ttm 前缀
        if bg_text:
            bg_span = ET.SubElement(text_el, "span")
            # 按照要求设置属性顺序：先 xmlns:ttm，再 ttm:role，最后 xmlns
            bg_span.set("xmlns:ttm", TTM_NS)
            # 先设置 ttm:role
            bg_span.set(f"{{{TTM_NS}}}role", "x-bg")
            # 最后设置默认 TTML 命名空间 xmlns
            bg_span.set("xmlns", TTML_NS)
            bg_span.text = f"({bg_text})"


def normalize_times_in_tree(root: ET.Element):
    for element in root.iter():
        normalize_time_attributes(element)


def convert_file(input_path: str, output_path: str):
    tree = ET.parse(input_path)
    root = tree.getroot()

    translations = collect_translations(root)
    if translations:
        ensure_itunes_translation_metadata(root, translations)

    normalize_times_in_tree(root)

    tree.write(output_path, encoding="utf-8", xml_declaration=False, short_empty_elements=True)


def parse_args():
    parser = argparse.ArgumentParser(description="Convert TTML translations into iTunesMetadata subtitles.")
    parser.add_argument("input", nargs="?", help="Input TTML file path")
    parser.add_argument("output", nargs="?", help="Optional output path")
    return parser.parse_args()


def prompt_for_input_path() -> str:
    while True:
        input_path = input("请输入要转换的 TTML 文件路径: ").strip()
        if input_path:
            return input_path
        print("输入不能为空，请输入一个有效的文件路径。")


def main():
    args = parse_args()
    input_path = args.input
    if not input_path:
        input_path = prompt_for_input_path()

    input_path = os.path.abspath(input_path)
    if not os.path.isfile(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")

    output_path = args.output
    if not output_path:
        base, ext = os.path.splitext(input_path)
        output_path = f"{base}_converted{ext}"

    convert_file(input_path, output_path)
    print(f"Converted TTML saved to: {output_path}")


if __name__ == "__main__":
    main()
