# How to Convert AMLL-TTML to Apple Syllable

###### [简体中文](./How-to-Convert.md) / English

> [!note]  
This document was translated by DeepSeek. For feedback or issues, please refer to the original content.

This document will guide you through converting TTML files created by AMLL TTML Tool (referred to as ATT) into Apple Syllable format.

## Preparation

### Before conversion, prepare the following:
- VSCode with Copilot
- [TTML file created by ATT](./AMLL-TTML.ttml)

### If you want segmented lyrics based on song structure, you'll also need:
- [Plain text lyrics with song structure tags](/docs/Lyric%20Booklets/苏逸Suyi,%20喵☆酱%20-%20Light%20in%20Abyss%20-%20Full%20ver.txt)
- [A segmented standard Apple Syllable file (formatted version)](./三Z-Studio,%20HOYO-MiX,%20雷雨心%20-%20制服·剪刀·鲨鱼尾_Format.ttml)
    - Not required, but having a completed standard version helps AI modify your document more accurately

## Pre-editing
Preprocessing is needed before handing files to AI for editing.

### Formatting
No one enjoys editing compressed XML files.  
While AI could theoretically understand compressed files, formatting helps humans edit and verify AI modifications.

---

Before formatting your TTML file, replace `</span> <span` with `</span><space/><span` using VSCode's replace function.  
Apple Syllable uses spaces between `<span>` tags as word separators, and formatting tools often break these spaces. Converting spaces to custom tags first is optimal.

You'll then get [formatted lyrics](./Format.ttml).

### Manual Processing
Make preliminary "Apple-ization" adjustments before AI editing:
- Modify the `<tt>` tag:
    - Remove AMLL namespace: `xmlns:amll="http://www.example.com/ns/amll"`
    - Add lyric type marker after iTunes namespace: `itunes:timing="Word" xml:lang="en"`
    - Final `<tt>` tag should resemble:
    ```xml
    <tt
        xmlns="http://www.w3.org/ns/ttml"
        xmlns:ttm="http://www.w3.org/ns/ttml#metadata"
        xmlns:itunes="http://music.apple.com/lyric-ttml-internal" itunes:timing="Word" xml:lang="en">
    ```
- Modify the `<head>` tag:
    - Delete all `<amll:meta>` elements in head > metadata (e.g., `<amll:meta key="qqMusicId" value="002lWTZR2zfSFX"/>`)
    - For songs with >2 vocalists: 
        - Tag vocalists in `<metadata>` per Apple specifications
        - Modify `ttm:agent` attributes in lyric line `<p>` tags
        - Reference [this example](./苏逸_Suyi,爆裂菊是也,小N%20-%20别忘记查收关心！_Format.ttml)
        - *Note: Optional as most official lyrics omit this*
- Remove leading zeros in timestamps:
    - Using VSCode replace (without regex):
        - Minutes: `00:`→(blank) `01:`→`1:` `02:`→`2:` etc.
        - Seconds: `"00.`→`"0.` `"01.`→`"1.` `"02.`→`"2.` etc.
- Adjust backing vocals (marked with `ttm:role="x-bg"`):
    - Remove timing info: Change to `<span ttm:role="x-bg">`
    - If backing vocals start before main vocals: Move `<span>` to beginning of lyric line
    - If backing vocals outlast main vocals: Extend the `<p>` tag's duration to cover full backing vocals

After these steps, your file is ready for AI modification.

## AI Modification
Enable Copilot in VSCode and ensure your lyrics file is included in references.

### Recommended Settings
- Mode: `Edit`
- Model: `Claude Sonnet 3.5`  
    - If using other editors (Trae/Cursor), prefer Claude Sonnet 3.7

### Initial Adjustment
ATT's TTML has reversed line/vocalist tags in `<p>`. Swap them (optional):

**Prompt:**
```prompt
Swap the positions of ttm:agent="v1" and itunes:key="L22" in all <p> tags,
changing them to itunes:key="L22" ttm:agent="v1"
```

### Translation & Songwriter Credits
Apple Music's WWDC25 update supports translations but uses a different format than ATT.

If translations exist in ATT, convert them. Always add songwriter credits:
- Add new `<iTunesMetadata>` tag in head > metadata
- Use this structure:
```xml
<iTunesMetadata
    xmlns="http://music.apple.com/lyric-ttml-internal">
    <translations>
        <translation type="subtitle" xml:lang="[Language code e.g., zh-Hans-CN]">
            <text for="L1">[Copy one translated line here as AI format example]</text>
        </translation>
    </translations>
    <songwriters>
        <songwriter>[Songwriter name]</songwriter>
        <songwriter>[One tag per songwriter]</songwriter>
    </songwriters>
</iTunesMetadata>
```

---

**Prompt:**
```prompt
Current translations are located in body > div > p > span ttm:role="translation".
Move them to head > metadata > iTunesMetadata > translations > translation > text
using format:
`<text for="corresponding itunes:key">Translation</text>`
Example:
`<text for="L1">[Your manually copied translation]</text>`
Generate modified output directly - no conversion scripts.
```

> [!note]  
> For lyrics with backing vocals (x-bg):  
> - Format as `Main vocals (Backing vocals)` with space before parentheses  
> - If backing vocals precede main: `(Backing vocals) Main vocals`  
> *This prompt won't handle backing vocals - manual adjustment required*

### Song Structure Segmentation
Apple segments lyrics into `<div>` by song structure. Use Copilot to automate:

First add empty `itunes:songPart` to `<div>`:
```xml
<div begin="15.992" end="27.456" itunes:songPart="">
```

**Reference Files:**
- Plain text lyrics with structure tags:  
    `lyrics.txt`
- Segmented Apple Syllable example:  
    `三Z-Studio, HOYO-MiX, 雷雨心 - 制服·剪刀·鲨鱼尾_Format.ttml`

**Prompt:**
```prompt
Notice I added itunes:songPart to <div> tags.
Segment lyrics using #file:lyrics.txt - each `#` marker requires a separate <div> with correct begin/end times.
Reference implementation: #file:三Z-Studio, HOYO-MiX, 雷雨心 - 制服·剪刀·鲨鱼尾_Format.ttml
```

> [!note]  
> `#file:xxx` is Copilot's file reference syntax (blue text). Ensure correct file linking.

### Completion!
After these steps, your lyrics are fully "Apple-ized"!  
Example output: [Modified lyrics](./苏逸Suyi,%20喵☆酱%20-%20Light%20in%20Abyss%20-%20Full%20ver_Format.ttml)

Always proofread after AI edits. Finalize by:
1. Compressing the file with a formatter
2. Replacing `<space/>` back to spaces
3. Saving as [final version](./苏逸Suyi,%20喵☆酱%20-%20Light%20in%20Abyss%20-%20Full%20ver.ttml)
> Keep both formatted and compressed versions for future editing

Submit the compressed version to Apple.

## Post-processing
Apple Music transmits lyrics in JSON-wrapped TTML. To recreate this format:
1. Replace all `"` with `\"` in TTML
2. Insert into JSON template:
    ```json
    {"data":[{"id":"unknown_id","type":"syllable-lyrics","attributes":{"ttml":"[Paste processed lyrics here]","playParams":{"id":"unknown_id","kind":"lyric","catalogId":"unknown_id","displayType":2}}}]}
    ```
    Formatted version:
    ```json
    {
        "data": [
            {
                "id": "unknown_id",
                "type": "syllable-lyrics",
                "attributes": {
                    "ttml": "[Paste processed lyrics here]",
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
    For localized translations: Replace `ttml` with `ttmlLocalizations`  
    Replace `unknown_id` with Apple Music song ID

Final output: [JSON lyrics](./苏逸Suyi,%20喵☆酱%20-%20Light%20in%20Abyss%20-%20Full%20ver.json)

*Do not submit JSON to Apple - this is only for transmission/parsing.*