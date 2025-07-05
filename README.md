# Repository for MiaowCham
本仓库主要用于暂存文件并生成直链  
若有问题请直接联系@MiaowCham

## File structure | 文件结构
<pre><code>Repository_for_MiaowCham/
├── docs                          # 文档文件夹
│   ├── log/                        # 日志文件夹，记录项目相关信息
│   ├── Lyric Booklets/             # 数字歌词本。路径下的文件内包含歌曲结构，原文及中文翻译
│   ├── Translation comparison/     # 不同歌词翻译版本对比资料
│   ├── example-json-lyrics.json    # 基于 Apple Syllable 编写的 json 格式歌词/传输协议
│   ├── Lyricify_Syllable_Next.md   # Lyricify Syllable Next 格式规范说明
│   └── Lyrics_Next.md              # lyrics Next 格式规范说明
├── images/                       # 图片资源
│   ├── DeepSeek.webp               # DeepSeek logo 
│   ├── Lyricify.ico                # Lyricify 图标
│   └── Spotify.ico                 # Spotify 图标
├── lyrics raw file/              # 歌词原始文件
│   ├── apple syllable/             # 符合 Apple Syllable 规范的歌词（测试）*
│   │   ├── How-to-Convert.md        # 将 AMLL TTML 转换为 Apple Syllable 的说明文档（中文）
│   │   └── How-to-Convert-EN.ttml   # Documentation for Convert AMLL TTML to Apple Syllable (English)
│   ├── ass/                        # 使用 Aegisub 制作的 ass 格式字幕/歌词
│   └── lyricify syllable/          # 喵锵上传至 Lyricify 4 的歌词的备份目录
├── music/                        # 音乐文件
├── video/                        # 视频文件
├── LICENSE.CC0-1.0               # 项目许可证（CC0 1.0）
├── LICENSE                       # 项目许可证
└── README.md                     # 项目说明文档

* 经实验验证，"./lyrics raw file/apple syllable/" 下的歌词文件可被 Apple Music 网页版正确识别，
  感兴趣者可自行通过浏览器开发工具(DevTool)对 Apple Music 网页版缓存歌词进行替换体验。
  使用 Beta 版(beta.music.apple.com)以查看翻译。
</code></pre>

## Attribution Table | 借物表
|文件|对应来源|原物直链|
|-|-|-|
|[images/DeepSeek.webp](images/DeepSeek.webp)|[Deepseek 官网](https://www.deepseek.com/)|[官网 Logo](https://cdn.deepseek.com/logo.png?x-image-process=image%2Fresize%2Cw_828)|
|[images/Lyricify.ico](images/Lyricify.ico)|[Lyricify 官网](https://lyricify.app/) · [Github](https://github.com/WXRIW/Lyricify-App/blob/main/images/lyricify_icon.png)|[官网 Logo](https://lyricify.app/_asset/Lyricify-icon.BDCo8SZW.png) · [Github Raw Link](https://raw.githubusercontent.com/WXRIW/Lyricify-App/refs/heads/main/images/lyricify_icon.png)|
|[images/Spotify.ico](images/Spotify.ico)|[Spotify 官网](https://open.spotify.com/)|[官网 Logo](https://open.spotify.com/favicon.ico)

## License  |  许可证  
This repository uses the CC0 1.0 License  |  本仓库使用 CC0 1.0 许可证  
This means anyone can freely use the content of this repository  |  这意味着任何人都可以随意使用该仓库的内容  

### Exceptions  |  特例  
I. Contents listed in the attribution table are excluded.  
I. 借物表包含的内容除外。  
   - Contents within the attribution table follow their original license/copyright statement.
   - 借物表内包含的内容遵循其原始许可证/版权声明。  
   - For any copyright disputes/objections, please directly contact @MiaowCham or submit an issue to request removal.
   - 若有版权纠纷/异议请直接联系 @MiaowCham 或者提交 issues 请求删除。  

II. For files in the `./lyrics raw file` directory:  
II. 若要使用 `./lyrics raw file` 目录下的文件：  
   - Please clearly label the author(@MiaowCham) when using it.
   - 请在使用时明确标记作者(@MiaowCham)
