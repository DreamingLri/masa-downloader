# Masa-Downloader

<img src="https://img.shields.io/badge/version-1.0.0-blue"/>

一个便捷的命令行工具，用于自动下载最新版本的Masa模组集合（如Litematica、MiniHUD、Tweakeroo等）

~~ModRinth不是最新版，天天从GitHub上爬取太难了~~

## 📋 安装步骤

### 方法1：使用发布版本

从[Release页面](https://github.com/DreamingLri/masa-downloader/releases)下载最新版本的可执行文件，直接运行即可

### 方法2：从源码运行

1. 克隆项目:
   ```bash
   git clone https://github.com/yourusername/masa-downloader.git
   cd masa-downloader
   ```

2. 安装依赖:
   ```bash
   pip install -r requirements.txt
   ```

3. 运行脚本:
   ```bash
   python main.py
   ```

---

## 🚀 使用指南

1. 首次运行时会在同目录下生成`config.json`配置文件
2. 运行程序后，根据提示选择需要下载的模组
3. 选择是否删除旧版本模组文件
4. 等待下载完成

---

## ⚙️ 配置说明

配置文件`config.json`包含以下关键参数：

### `repositories` (仓库列表)

| 参数名 | 类型 | 说明 |
|--------|------|------|
| owner | 字符串 | GitHub仓库所有者名称 |
| repo | 字符串 | GitHub仓库名称 |
| version | 字符串 | 模组适用的Minecraft版本号 |

示例配置:

```json
"repositories": [
    {
        "owner": "sakura-ryoko",
        "repo": "litematica",
        "version": "1.21.4"
    },
    {
        "owner": "sakura-ryoko",
        "repo": "malilib",
        "version": "1.21.4" 
    }
]
```

### `download_dir` (下载目录)

指定模组文件的下载保存位置：

- **相对路径**: `"download_dir": "downloads"` (保存在程序同目录下的downloads文件夹)
- **绝对路径**: `"download_dir": "C:/Minecraft/mods"`
- **null或空字符串**: 默认使用用户的"Downloads"目录

---

## 💡 常见问题

- **Q**: 无法连接到GitHub API
  **A**: 由于使用的是 Github Api，有时候大陆会连接不通，考虑一下魔法

- **Q**: 下载的模组与 Minecraft 版本不兼容
  **A**: 请在`config.json`中修改相应模组的`version`字段为您的 Minecraft 版本

- **Q**: 我发现了bug?
  **A**: 欢迎提交 [Issue](https://github.com/DreamingLri/masa-downloader/issues/new)