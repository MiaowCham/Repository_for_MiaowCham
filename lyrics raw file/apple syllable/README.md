## 该目录存储完全符合 Apple Syllable 的 TTML 及 Json 歌词

该目录下分为：
- json 包裹的传输版本 (.json)
- 原始 ttml 歌词 (.ttml)
- 格式化的 ttml 歌词 (_Format.json)

其中，json 版本支持直接被 Apple Music (如果你能给苹果的原始json请求给抓包调换的话) 和 Lyricify 4 (部分)识别，原始 ttml 版本支持被 AMLL 识别。

现已开始使用 Apple 官方翻译格式。最新版 AMLL TTML Tool 或 [Apple Music Web Beta](https://beta.music.apple.com/) 可正确解析翻译。

由于遵循 Apple 规范，人声 ID 数量可能大于 2，导致在不同平台出现不同的对唱效果。本仓库只保证歌词的准确性，不能保证对唱的一致性。若您想获取针对对唱视图适配的版本，请尝试前往 [/lyrics raw file](../) 目录下其他文件夹查找适配版本。

---

**如果你也想通过 AMLL TTML Tool 制作 Apple Syllable 歌词，请参阅：[如何将 AMLL TTML 转换为 Apple 音节](./How-to-Convert.md)**