# Ob2Hexo - Obsidian to Hexo Converter

<p align="center">
  <img src="https://img.shields.io/github/v/release/MathLeee/Ob2Hexo?style=for-the-badge" alt="GitHub release (latest by date)">
  <img src="https://img.shields.io/github/downloads/MathLeee/Ob2Hexo/total?style=for-the-badge" alt="GitHub all releases">
  <img src="https://img.shields.io/github/license/MathLeee/Ob2Hexo?style=for-the-badge" alt="GitHub">
</p>

一个强大的工具，旨在将你的Obsidian笔记无缝转换为与Hexo博客系统完全兼容的Markdown格式。项目提供两种使用方式：**Obsidian插件**（推荐）和**独立的Python脚本**。

## 核心功能

- **✨ 智能链接转换**: 自动处理内部链接、跨文档链接，并生成符合规范的锚点。
- **🎨 赛博朋克Note卡片**: 将Obsidian的Callouts（如 `[!NOTE]`）转换为带有赛博朋克2077风格的HTML卡片，支持多种类型和自定义标题。
- **🖼️ 图片引用修复**: 自动转换 `![[图片]]` 格式为标准Markdown图片引用。
- **📄 Hexo兼容**: 自动为转换后的文件添加YAML Front Matter，包含标题、日期等。
- **🚀 批量处理**: 支持一键转换文件夹内的所有Markdown文件。

---

## 🚀 方案一：Obsidian插件（推荐）

在Obsidian中直接享受最流畅、最便捷的转换体验。

### 安装插件

1.  访问本项目的 [Releases页面](https://github.com/MathLeee/Ob2Hexo/releases)。
2.  下载最新的 `main.js` 和 `manifest.json` 文件。
3.  在你的Obsidian仓库中，进入 `.obsidian/plugins/` 目录（如果没有，请手动创建）。
4.  创建一个新的文件夹，例如 `ob2hexo-converter`。
5.  将下载的 `main.js` 和 `manifest.json` 放入该文件夹。
6.  重启Obsidian，在 `设置` -> `社区插件` 中启用 "Obsidian to Hexo Converter"。

### 使用方法

启用插件后，你有多种方式触发转换：

- **右键菜单**: 在文件浏览器中右键点击一个Markdown文件，选择 `🔄 转换为Hexo格式`。
- **命令面板**: 按 `Ctrl+P` 打开命令面板，输入并选择：
    - `转换当前文件为Hexo格式`
    - `批量转换当前文件夹的所有MD文件`

转换后的文件将以 `_converted.md` 后缀保存在原文件旁边。

---

## 🐍 方案二：独立Python脚本

适用于不希望安装插件，或需要在自动化流程中使用的场景。

### 环境要求

- Python 3.6+
- 无需额外依赖包

### 使用方法

```bash
# 克隆仓库
git clone https://github.com/MathLeee/Ob2Hexo.git
cd Ob2Hexo

# 转换单个文件
python obsidian_to_markdown_converter.py path/to/your/file.md

# 转换整个目录
python obsidian_to_markdown_converter.py path/to/your/directory

# 查看帮助
python obsidian_to_markdown_converter.py -h
```

## 🎨 赛博朋克Note卡片展示

转换后的Note卡片拥有独特的赛博朋克风格，支持多种类型：

| 类型 | 颜色 | 图标 |
| :--- | :--- | :--- |
| `[!NOTE]` | 青色 | 📝 |
| `[!TIP]` | 绿色 | 💡 |
| `[!WARNING]`| 黄色 | ⚠️ |
| `[!DANGER]` | 红色 | 🚨 |
| `[!INFO]` | 青色 | ℹ️ |
| `[!EXAMPLE]`| 紫色 | 📋 |
| `[!QUOTE]` | 紫色 | 💬 |

**示例效果**:

*（这里可以放一张Note卡片的截图）*

## 贡献

欢迎通过提交 **Issues** 或 **Pull Requests** 来帮助改进这个项目。无论是功能建议、Bug报告还是代码贡献，我们都非常欢迎！

## 许可证

本项目基于 [MIT License](LICENSE) 开源。

---

**让你的Obsidian笔记在Hexo中闪闪发光！** ✨🚀
        
