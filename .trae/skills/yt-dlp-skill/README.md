# yt-dlp 视频下载器 Skill

## 简介

这是一个基于开源工具 yt-dlp 的视频下载 Skill，只要提供视频链接，就可以帮助下载视频。

## 功能特性

- ✅ 支持超过 10,000+ 个视频网站
- ✅ 自动检查和安装 yt-dlp
- ✅ 支持自定义输出目录
- ✅ 支持指定视频质量
- ✅ 详细的下载进度和结果显示

## 支持的网站

- YouTube
- 哔哩哔哩 (B站)
- 爱奇艺
- 腾讯视频
- 优酷
- 抖音
- 快手
- 微博视频
- 以及其他 10,000+ 个视频网站

## 使用方法

### 基本用法

只需要提供视频链接，Skill 会自动处理下载：

```
https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

### 高级用法

如果需要指定输出目录或视频质量，可以使用命令行模式：

```bash
python scripts/download_video.py <video-url> [-o <output-directory>] [-q <quality>] [-v]
```

参数说明：
- `<video-url>`: 视频链接（必填）
- `-o <output-directory>`: 输出目录（可选）
- `-q <quality>`: 视频质量（可选，默认 best）
- `-v`: 显示详细信息（可选）

## 目录结构

```
yt-dlp-skill/
├── SKILL.md          # Skill 配置文件
├── scripts/          # 脚本目录
│   └── download_video.py  # 核心下载脚本
└── README.md         # 说明文档
```

## 技术实现

### 核心脚本

**scripts/download_video.py**

- 使用 yt-dlp 库进行视频下载
- 自动检查并安装依赖
- 支持多种下载选项
- 提供友好的用户反馈

### 依赖项

- Python 3.6+
- yt-dlp（会自动安装）

## 注意事项

1. **版权声明**：下载视频时请遵守相关网站的使用条款和版权规定
2. **网络连接**：需要稳定的网络连接以确保下载成功
3. **文件大小**：大型视频文件可能需要较长的下载时间
4. **认证需求**：某些网站可能需要登录才能下载视频

## 故障排除

### 常见问题

1. **无法安装 yt-dlp**
   - 解决方案: 手动安装 `pip install yt-dlp`

2. **下载失败**
   - 检查网络连接
   - 确认视频链接是否有效
   - 尝试使用 `-v` 参数查看详细错误信息

3. **视频质量问题**
   - 使用 `-q` 参数指定质量，例如: `-q bestvideo+bestaudio`

4. **文件路径问题**
   - 使用 `-o` 参数指定具体的输出目录

## 示例

### 示例 1: 下载 YouTube 视频

```
https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

### 示例 2: 下载 B 站视频

```
https://www.bilibili.com/video/BV1xx411c7mW
```

## 许可证

本项目基于 MIT 许可证开源。