# Lyrics Next 格式规范第一版

> [!note]   
> 仅供娱乐，当然如果你的软件想使用这个格式是完全可以的（真的会有人用吗？）

一种基于 [LRC](https://zh.wikipedia.org/wiki/LRC%E6%A0%BC%E5%BC%8F) 的逐字歌词格式，参考了 [TTML](https://en.wikipedia.org/wiki/Timed_Text_Markup_Language) 和 [Lyricify Syllable](https://github.com/WXRIW/Lyricify-App/blob/main/docs/Lyricify%204/Lyrics.md#lyricify-syllable-%E6%A0%BC%E5%BC%8F%E8%A7%84%E8%8C%83)  
Lyrics Next 为了解决普通歌词可读性差、兼容性低的问题而诞生  
Lyrics Next 歌词文件可以直接使用 `lrc` 后缀，也可以使用单独的 `lrcn`

带 * 的条目为非强制要求

## 更改

<details>
<summary>点击展开</summary>
<br>

相较于原本的 LRC-Super[^1]，Lyrics Next 进行了许多更改。新版规范无法适配旧版规范，请以新版规范为准

[^1]: LRC-Super 是 Lyrics Next 的前身。目前已归档不再使用。

### 更多信息
Lyrics Next 的规范增加了更多详细标准释义，包括 [规范用语](#规范用语) 和更多 [头部信息标准](#头部信息)
### 格式更改
Lyrics Next 对歌词正文格式进行了调整。具体如下：
- 歌词行标签增加 `duration` 信息，标记歌词行时长
- 将 `agent` 信息移动至歌词行标签内部
- 简化了逐行版本的格式

### 翻译/音译支持
Lyrics Next 修改了对翻译/音译的格式规范

</details>

## 规范用语

### 时间标签
在 Lyrics Next 中，歌词行行首被 `[]` 包裹的内容被称为 `标签`，后续的歌词内容被称为 `正文`  
正文中被 `<>` 包裹的内容被称为 `时间(轴)标签` 或 `时间(轴)标记`  
凡事使用时间轴标记的内容均可称为 `项目`，包括行，字，词或音节  

### 歌曲对唱关系
根据音乐中常见的演唱方式，歌词分为 `主唱(人声/歌词)` 与 `背景(人声/歌词)`  
**主唱**: 常规的 `agent` 均为 `主唱人声`，属于歌词正文，用于主要歌词  
**背景**: `agent` 带有 `bg` 字样为 `背景人声`，一般用于背景声。
背景人声的歌词位于主唱歌词下方，字体较小，该歌词行称为 `背景人声` `背景行` `bg 行`

根据 `agent` 标签的信息进行的实际歌词排版称为 `对唱视图`  
左对齐且一般为主唱的歌词为 `左视图` `主视图` `左对唱` `主对唱`  
右对齐且一般为第二位歌手的歌词为 `右视图` `副视图` `右对唱` `副对唱`  
> 对唱视图是基于 Apple Music 的歌词节目制定的名称
> 实际上 Apple Music 使用的歌词包含完整的 `agent` 信息

## 头部信息 *

<details>
<summary>点击展开</summary>
<br>

歌词头部可选的包含歌词相关信息，如：  
| 标签                               | 含义                                                     |
| ---------------------------------- | -------------------------------------------------------- |
| [lrcn-vertion:v3.0]                | Lyrics Next 格式版本                                     |
| [timing:syllable]                  | 项目类型<br>`line` 为逐行，`word` `syllable` 为逐字/音节 |
| [ti:On the Journey]                | 歌曲标题                                                 |
| [ar:HOYO-MiX]                      | 歌手名                                                   |
| [ar-v1:魏晨]                       | 歌手名，但包含 `agent` 对应信息                          |
| [ar-v2:Nea]                        | ^^                                                       |
| [al:On the Journey]                | 专辑名                                                   |
| [from:QQMusic]                     | 歌词源                                                   |
| [by:MiaowCham]                     | 歌词制作者                                               |
| [offset:0]                         | 歌曲偏移量（单位毫秒）                                   |
| [QQMusic-mid:0049lelQ3EY4jN]       | 歌曲对应平台及平台 ID，下同                              |
| [ncmid:2699981246]                 | ^^                                                       |
| [spotifyid:0HqjLk8hVH78mkgY6Z2eX6] | ^^                                                       |

若一个标签有多个内容，可以用 `,` 分割或者使用多个标签表示

*注意：该内容可以不填，不要包含重复标签。(重复标签指完全相同的标签)*  

### 关于 ***歌曲对应平台及平台 ID***，推荐使用以下标准 *

```
[对应标签-额外信息（可选）:ID]
```
| 平台        | 对应标签   | 额外信息 |
| ----------- | ---------- | -------- |
| 网易云      | ncmid      |          |
| QQ音乐      | QQMusic    | mid/id   |
| 酷狗音乐    | kugouid    |          |
| Spotify     | spotifyid  | 地区     |
| Apple Music | applemusic | 地区     |

关于 Apple Music 和 Spotify 的地区信息，一般遵循以下标准：

- 除去隔壁特殊区外的总区，使用英文 - `global` 或直接使用语言代号 `en`
- 使用简体中文的中国区 - `hans` 或直接使用地区代号 `cn`
- 使用繁体中文的港澳台地区 - `hant` 或直接使用地区代号 `hk` `tw`
- 使用日语的日区 - `jp`
- 使用韩语的韩区 - `kr`

</details>

## 歌词
Lyrics Next 歌词的标准格式为：
```
[start,duration,agent]<start,duration>Word <start,duration>word
```
- `agent` 用于标记该句演唱歌词的艺人的 ID。  
一般 `v1` 对应左视图，`v2` 对应右视图。若只有一个演唱者可以不填。
- `start` 为起始时间,其时间戳使用同步多媒体集成语言（SMIL）表示。  
    一般情况下使用SMIL表示，可提供完整或部分时钟值：  
    `hh:mm:ss.sss（时:分:秒.毫秒）`   
    *其中，小时和毫秒可不提供。  
- `duration` 为时长。使用毫秒计数。如果未填写 `duration` 则将后一个项目的开始时间作为结束时间（兼容增强型lrc）  
- `<>` 中的时间戳为后方单词的起始时间和时长。

### **特殊歌词**  

包括背景人声、翻译/音译信息，这些内容均视为主唱歌词的附属歌词  
`bg` 对应背景人声，`ts` `trans` 对应翻译行，`roma` 对应音译行

翻译/音译只针对主唱歌词，若需要标记背景人声的歌词，需要使用 `主唱 (背景)` 的格式  
不建议在歌词文件中包含音译信息，应当优先使用播放器的自动生成功能

> [!note]
> 即使背景人声的起始时间在主句前面，背景人声也得在主句的后一行
> 主唱和背景人声的翻译之间需要有一个空格分割，否则无法精准拆分

附属歌词必须在主唱歌词下方使用 `[]` 包裹，具体格式如下：
```
[start,duration,agent]<start,duration>Word <start,duration>word  # 主唱歌词
[agent:<start,duration>Word <start,duration>word]               # 翻译/音译
```

示例：
```
[00:10.856,856,v1]<10.856,342>Had <11.198,160>to <11.358,363>have...
[trans:我必须对生活抱有超高的期望 (满怀期望)]
[bg:<8.705,456>High, <9.161,782>high <9.943,709>hopes]
```

### **逐句歌词：**  
如果想使用 Lyrics Next 记录逐句而非逐字歌词，则无需逐词标记时间信息：
```
[start,duration,agent]Lyrics
```

## 翻译/音译

Lyrics Next 支持多种翻译/音译格式

### 内置翻译/音译方案（推荐）
- 详见 [#特殊歌词](#特殊歌词)

### 外置 lrc 翻译/音译（传统）
使用独立的 lrc 翻译/音译文件。需要与原文歌词保持逐句对应  
歌词解析应当保留模糊余地，使不完全对应的翻译也能被识别  
但歌词制作者不应当制作/提供有无法对应行的翻译/音译文件

### 对应 LRC 翻译/音译
Lyrics Next 需要将 **拥有相同开始时间** 且 **行数更靠后的 LRC 格式歌词** 视为翻译  
>该方案实际为将外置翻译内嵌化的方案，理论上该方案不支持音译，具体以实际解析为准

示例：
```
[00:34.390,3660,v1]<00:34.390,1120>Legends <00:35.510,630>aren't <00:36.140,660>born <00:36.800,600>that <00:37.400,650>way
[00:34.390]传奇并非天成
```

## 兼容 *
Lyrics Next 直接兼容 `逐行lrc` 和 `增强型lrc`；兼容 `逐字lrc`，但不能与其他格式混用  
不兼容 `lys` `ttml`,但由于特性相似可以实现转换  
但只有完整且规范的 Lyrics Next 才能激活其完整特性（对唱视图、背景人声等）