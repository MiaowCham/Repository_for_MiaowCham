# Lyricify Syllable Next 格式规范

> [!note]   
> 仅供娱乐，当然如果你的软件想使用这个格式是完全可以的（真的会有人用吗？）

这玩意原本叫 Lyrics Next（兼容版），~~因为是拿 Lyrics Next 文档改的(bush~~  
但是该版本的 Lyrics Next 彻底融合了 [Lyricify Syllable](https://github.com/WXRIW/Lyricify-App/blob/main/docs/Lyricify%204/Lyrics.md#lyricify-syllable-%E6%A0%BC%E5%BC%8F%E8%A7%84%E8%8C%83) 的特性

所以 Lyrics Next（兼容版）正式名称为 **Lyricify Syllable Next** (`.lysn`)  
当然 Lyricify Syllable Next 歌词文件也可以直接使用 `.lys` 后缀，因为它理论上属于 [Lyricify Syllable](https://github.com/WXRIW/Lyricify-App/blob/main/docs/Lyricify%204/Lyrics.md#lyricify-syllable-%E6%A0%BC%E5%BC%8F%E8%A7%84%E8%8C%83) 的一种扩展格式  

带 * 的条目为非强制要求

## 更改
Lyricify Syllable Next 是基于 [Lyricify Syllable](https://github.com/WXRIW/Lyricify-App/blob/main/docs/Lyricify%204/Lyrics.md#lyricify-syllable-%E6%A0%BC%E5%BC%8F%E8%A7%84%E8%8C%83) 的改进版本，和 Lyrics Next 版本相比，Lyricify Syllable Next 进行了以下更改：  

**歌词的时间轴标记方式完全使用 [Lyricify Syllable](https://github.com/WXRIW/Lyricify-App/blob/main/docs/Lyricify%204/Lyrics.md#lyricify-syllable-%E6%A0%BC%E5%BC%8F%E8%A7%84%E8%8C%83) 的方式**
- 统一时间轴单位为毫秒（原版的 `start` 使用同步多媒体集成语言(SMIL)表示）
- `agent` 信息兼容 [Lyricify Syllable](https://github.com/WXRIW/Lyricify-App/blob/main/docs/Lyricify%204/Lyrics.md#lyricify-syllable-%E6%A0%BC%E5%BC%8F%E8%A7%84%E8%8C%83) 的歌词行属性 `property` 标记

相较于 [Lyricify Syllable](https://github.com/WXRIW/Lyricify-App/blob/main/docs/Lyricify%204/Lyrics.md#lyricify-syllable-%E6%A0%BC%E5%BC%8F%E8%A7%84%E8%8C%83) 原版，做出了以下更改：
- `property` 支持使用 `agent` 填写
- `property` 前面加入了整行的时间轴信息
- 添加了内置翻译/音译方案

## 头部信息 *

同 Lyricify Syllable，详见 [Lyricify Syllable 格式规范](https://github.com/WXRIW/Lyricify-App/blob/main/docs/Lyricify%204/Lyrics.md#lyricify-syllable-%E6%A0%BC%E5%BC%8F%E8%A7%84%E8%8C%83)

*注意：该内容可以不填，不要包含重复标签。(重复标签指完全相同的标签)*  

## 歌词
Lyricify Syllable Next 歌词的标准格式为：
```
[start,duration,agent]Word (start,duration)word(start,duration)
```
- `agent` 用于标记该句演唱歌词的艺人的 ID（或歌词行属性信息）。  
一般 `v1` 对应左视图，`v2` 对应右视图，`bg` 对应背景人声，`ts` 对应翻译行，`roma` 对应音译行。
- `start` 为起始时间，`duration` 为时长。 
- `()` 中的时间戳为前方单词的起始时间和时长。
- 时间戳的是大于零的整数，单位是毫秒 (ms)。  

关于 `agent` 信息，Lyricify Syllable Next 要求能够兼容 Lyricify Syllable 的 `property` 属性，具体如下：
| 属性  | 背景人声 | 对唱视图 |
| :---: | :------: | :------: |
|   0   |  未设置  |  未设置  |
|   1   |  未设置  |    左    |
|   2   |  未设置  |    右    |
|   3   |    否    |  未设置  |
|   4   |    否    |    左    |
|   5   |    否    |    右    |
|   6   |    是    |  未设置  |
|   7   |    是    |    左    |
|   8   |    是    |    右    |

### **注意和示例：**  
即使背景人声的起始时间在主句前面，背景人声也得在主句的后一行，如：
```
[25910,14980,3]They (25910,370)think (26280,550)that (26830,460)we're (27530,410)no (27940,610)one(28550,460)
[14010,7170,6](We (14010,580)are (14590,760)we (15750,410)are. (16160,820)We (17450,340)are (17790,860)we (19110,400)are)(19510,1670)
```

### **逐句歌词：**  
如果想使用 Lyricify Syllable Next 记录逐句而非逐字歌词，则无需逐词标记时间信息：
```
[start,duration,agent]Lyrics
```

## 翻译/音译

Lyricify Syllable Next 支持多种翻译/音译格式

### 对应标签翻译/音译（推荐） 
该方案使用 Lyricify Syllable Next 的标签信息来标记翻译/音译行  
支持类似 LRC 的免排序歌词行的效果，只需要保证时间轴对应，无需保证一定位于原歌词行下方，即可完成翻译/音译对应
```
[34390,,ts]传奇并非天成          # 不填写 duration 信息
[39110,1010,ts]但由功迹铸就      # 完整版（推荐）
[40800,835,roma]音译             # 音译
```

### 对应 LRC 翻译/音译
Lyricify Syllable Next 需要将 **拥有相同开始时间** 且 **行数更靠后的 LRC 格式歌词** 视为翻译  
>该方案实际为将外置翻译内嵌化的方案，理论上该方案不支持音译，具体以实际解析为准

示例：
```
[34390,3660,v1]Legends (34390,1120)aren't (35510,630)born (36140,660)that (36800,600)way(37400,650)
[34.390]传奇并非天成
```

### 外置 lrc 翻译/音译（传统）
使用独立的 lrc 翻译/音译文件。需要与原文歌词保持逐句对应  
歌词解析应当保留模糊余地，使不完全对应的翻译也能被识别  
但歌词制作者不应当制作/提供有无法对应行的翻译/音译文件

## 兼容 *
顾名思义，Lyricify Syllable Next 兼容 [Lyricify Syllable](https://github.com/WXRIW/Lyricify-App/blob/main/docs/Lyricify%204/Lyrics.md#lyricify-syllable-%E6%A0%BC%E5%BC%8F%E8%A7%84%E8%8C%83) (无法反向兼容)  
也许更加兼容 QRC (Lyricify 标准) ，因为长得很像，只比QRC多了个 `agent` 信息