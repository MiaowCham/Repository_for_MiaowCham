# How to Convert AMLL-TTML to Apple Syllable

###### 简体中文 / [English](./How-to-Convert-EN.md)

本文档将会告诉你如何将 AMLL TTML Tool（下称 ATT） 制作的 TTML 转换成 Apple Syllable

## 准备

### 在进行转换前，请先准备以下内容：
- VSCode with Copilot
- [ATT 制作的 TTML](./AMLL-TTML.ttml)

### 如果你希望根据歌曲结构进行分段，你还需要以下内容：

- [包含歌曲结构标签的纯文本歌词](/docs/Lyric%20Booklets/苏逸Suyi,%20喵☆酱%20-%20Light%20in%20Abyss%20-%20Full%20ver.txt)
- [一个带分段的标准 Apple Syllable（格式化版本）](./三Z-Studio,%20HOYO-MiX,%20雷雨心%20-%20制服·剪刀·鲨鱼尾_Format.ttml)
    - 这不是必须的，但有一份已经完成的标准版本的话，可能会让 AI 更加精确的修改你的文档

## 预先编辑
在把文件交付给 AI 编辑前，需要先进行一些预处理

### 格式化
没有人会喜欢编辑压缩状态下的 XML 文件  
虽然理论上无需格式化 AI 也能看懂，但其实格式化不是给 AI 干的，而是为了方便我们直接编辑和检查 AI 的修改

---

在把 TTML 文件丢给格式化工具前，你需要用 VSCode 的替换功能把文档中的 `</span> <span` 替换成 `</span><space/><span`  
因为 Apple Syllable 会通过 `<span>` 标签之间的空格来充当单词直接的空格，而格式化工具通常会把这些空格给破坏掉。提前将空格转换成自己喜欢的标签是最佳选择

然后你就可以得到 [格式化后的歌词](./Format.ttml)

### 人工处理
在把文件交付给 AI 编辑前，你可以自己先将其初步 “Apple 化”

- 首先查看 `<tt>` 标签
    - 将其中的 AMLL 命名空间 `xmlns:amll="http://www.example.com/ns/amll"` 去除
    - 在 itunes 命名空间后添加歌词类型标记，类似：`itunes:timing="Word" xml:lang="en"`
    - 完成处理的 `<tt>` 标签应该和下方的例子差不多：
    ```
    <tt
        xmlns="http://www.w3.org/ns/ttml"
        xmlns:ttm="http://www.w3.org/ns/ttml#metadata"
        xmlns:itunes="http://music.apple.com/lyric-ttml-internal" itunes:timing="Word" xml:lang="en">
    ```
- 然后是 `<head>` 标签
    - 在 head > metadata 标签下会有一些使用 amll 命名空间的元数据，类似：`<amll:meta key="qqMusicId" value="002lWTZR2zfSFX"/>`。将其全部删除
    - 如果歌词的歌曲实际的演唱者不止两个，请按照 Apple 官方规范在 `<metadata>` 中标记演唱者，并同步修改 `<body>` 中歌词行 `<p>` 标签的 `ttm:agent` 属性
        - 具体可以参考 [这份歌词](./苏逸_Suyi,爆裂菊是也,小N%20-%20别忘记查收关心！_Format.ttml)
        - 这不是必须的，虽然 Apple 官方规范要求你这么做，但绝大部分官方歌词都没有做到这点
- 删除时间轴的前导零（也就是时间轴高位的 0）
    - 你可以使用 VSCode 的替换功能，依次替换：
        - 不要按下 “使用正则表达式” 按钮
        - 代码块内的是查找的内容，括号内的是替换的内容
        - 分钟：`00:`(替换为空) `01:`(1:) `02:`(2:) `03:`(3:) `04:`(4:) 等
        - 秒钟：`"00.`("0.) `"01.`("1.) `"02.`("2.) 等
- 调整背景人声
    - 背景人声是拥有 `ttm:role="x-bg"` 标签的歌词，位于主歌词下方（iOS 26 中也可能在上方）的小字
    - 删除背景人声行 `<span>` 标签中的时间信息，使其变成：`<span ttm:role="x-bg">`
    - 如果背景人声的开始时间早于主歌词，请将整个背景人声的 `<span>` 标签移动至歌词行头部
    - 如果背景人声的持续时长超过主歌词，且你希望完整显示背景人声的话，请让歌词行 `<p>` 标签中的时间轴包含背景人声的持续时间

当你完成以上处理后，你就可以开始使用 AI 修改歌词了

## AI 修改
在接下来的修改中，请打开 VSCode 的 Copilot 面板，并确保在文件引用中包含待你的歌词

### 建议设置
- 设置模式：`Edit`
- 选取模型：`Claude Sonnet 3.5`  
    - 如果你在使用其他 AI 编辑器，如 Trae 或 Cursor，更加推荐使用 Claude Sonnet 3.7（如果可以）

### 初步调整
ATT 输出的 TTML 在 `<p>` 标签中，行数和演唱者标记是和 Apple 官方歌词相反的，可以给他调转一下。当然这不是必须的

**提示词：**

帮我把 p 标签里的 ttm:agent="v1" 和 itunes:key="L22" 调个位置，
变成 itunes:key="L22" ttm:agent="v1"


### 翻译与制作人
Apple 在 WWDC25 上发布的新版 Apple Music 已经支持翻译功能，但与 ATT 使用的翻译格式并不相同

如果你已经在 ATT 中填写了翻译，请按照以下步骤进行转换
即使你没有填写翻译，你也应当按照下方步骤填写制作人信息
- 在 head > metadata 中新添加一个 `<iTunesMetadata>` 标签
- 修改为下方的样式：
```xml
<iTunesMetadata
    xmlns="http://music.apple.com/lyric-ttml-internal">
    <translations>
        <translation type="subtitle" xml:lang="[请在这里填写语言代码，如“zh-Hans-CN”]">
            <text for="L1">[你可以手动复制一句翻译到此处，以此告诉 AI 具体格式]</text>

        </translation>
    </translations>
    <songwriters>
        <songwriter>[请在这里填写制作人]</songwriter>
        <songwriter>[一个制作人使用一个标签]</songwriter>
    </songwriters>
</iTunesMetadata>
```

---

**提示词：**

现在这个ttml歌词字幕的句子翻译在 body > div > p > span ttm:role="translation" 里，
我需要你帮我把它从这个位置移动到 head > metadata > iTunesMetadata > translations > translation > text 里
格式为：
`<text for="对应行的itunes:key值">翻译</text>`
例如：
`<text for="L1">[你手动复制的那一句翻译]</text>`
请直接生成修改，不要使用转换脚本

> [!note]  
如果你的歌词中包含 “背景人声”（x-bg），该提示词不能帮你进行转换，你需要手动按照 `主歌词 (背景人声)` 的格式进行记录。括号和主歌词之间有一个空格  
如果背景人声在主歌词前面，则应该使用 `(背景人声) 主歌词` 的格式

### 歌曲结构分段
Apple 会根据歌曲结构将 `<div>` 分段。手动分段是很麻烦的事情，借助 Copilot 可以快速进行分段

先在 `<div>` 标签加上一个空的 `itunes:songPart`，效果如下：
```xml
<div begin="15.992" end="27.456" itunes:songPart="">
```

**引用文件：**
- 包含歌曲结构标签的纯文本歌词：  
    `lyrics.txt`
- 一个带分段的标准 Apple Syllable（格式化版本）：  
    `三Z-Studio, HOYO-MiX, 雷雨心 - 制服·剪刀·鲨鱼尾_Format.ttml`

**提示词：**

你可以注意到我在 div 标签中添加了一个 itunes:songPart，
你帮我根据 #file:lyrics.txt 这个词本对歌词进行分段，每个`#`标记的音乐结构都需要使用独立的 div 标签，需要注意开始和结束时间
具体效果可以参考 #file:三Z-Studio, HOYO-MiX, 雷雨心 - 制服·剪刀·鲨鱼尾_Format.ttml 

> [!note]  
`#file:xxx` 是 Copilot 的引用功能，输入 `#` 后选定对应文件。请确保其显示为**蓝底蓝字**

### 完成！
如果你根据以上步骤完成修改，那你的歌词现在已经非常 “Apple 化”！  
比如我们开头举例的歌词，修改后变成了[这个](./苏逸Suyi,%20喵☆酱%20-%20Light%20in%20Abyss%20-%20Full%20ver_Format.ttml)

建议你在每次 AI 编辑后进行校对，并在完成修改后进行整体校对  
确保文件无误后，使用格式化工具对其进行压缩，并重新将 `<space/>` 替换回空格，得到[最终成果](./苏逸Suyi,%20喵☆酱%20-%20Light%20in%20Abyss%20-%20Full%20ver.ttml)
> 建议同时保存格式化和压缩版本，方便后续查看与编辑

如果你要将歌词提交的话，请将压缩版本提交给 Apple 官方

## 后续操作
Apple Music 在传输时其实并不是直接传输 TTML 原文件，而是套了一层 JSON 进行传输  
如果你先还原此 JSON 格式歌词，可以按照下方操作:

- 首先，使用替换功能将 TTML 中的 `"` 全部替换成 `\"`
- 然后将得出的结果填入下方 JSON 模板中：
    ```json
    {"data":[{"id":"unknown_id","type":"syllable-lyrics","attributes":{"ttml":"[请将处理好的歌词复制到此处]","playParams":{"id":"unknown_id","kind":"lyric","catalogId":"unknown_id","displayType":2}}}]}
    ```
    格式化版本：
    ```json
    {
        "data": [
            {
                "id": "unknown_id",
                "type": "syllable-lyrics",
                "attributes": {
                    "ttml": "[请将处理好的歌词复制到此处]",
                    "playParams": {
                        "id": "unknown_id",
                        "kind": "lyric",
                        "catalogId": "unknown_id",
                        "displayType": 2
                    }
                }
            }
        ]
    }
    ```
    如果包含本地化翻译，请将 `ttml` 改为 `ttmlLocalizations`  
    `unknow_id` 处可填写歌曲的 Apple Music ID

最终效果：[JSON 歌词](./苏逸Suyi,%20喵☆酱%20-%20Light%20in%20Abyss%20-%20Full%20ver.json)

请不要将 JSON 歌词提交给 Apple，这只是为了传输和快捷解析使用的中间格式