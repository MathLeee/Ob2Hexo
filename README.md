# Obsidian to Hexo Converter (Ob2Hexo)

一个用于将 Obsidian 格式的 Markdown 文件转换为 Hexo 博客兼容格式的工具集，包含 Python 脚本和 Obsidian 插件两个版本。

## 🚀 快速开始

### Python 脚本版本

```bash
# 克隆仓库
git clone https://github.com/MathLeee/Ob2Hexo.git
cd Ob2Hexo

# 转换单个文件
python obsidian_to_markdown_converter.py input.md -o output.md
```

### Obsidian 插件版本

1. 下载 `obsidian-markdown-converter` 文件夹
2. 复制到你的 Obsidian 插件目录
3. 在 Obsidian 中启用插件
4. 右键点击文件选择"转换为 Hexo 格式"

## 📦 两个版本对比

| 特性 | Python 脚本 | Obsidian 插件 |
|------|-------------|---------------|
| 使用便利性 | 命令行操作 | 图形界面，右键转换 |
| 批量处理 | ✅ 支持 | ✅ 支持 |
| 依赖要求 | Python 3.6+ | Obsidian 软件 |
| 自定义程度 | 高 | 中等 |

### 🔗 链接转换
- **内部链接**: `[[#标题|显示文本]]` → `[显示文本](#标题)`
- **跨文档链接**: `[[文档名|显示文本]]` → `[显示文本](文档名.md)`
- **自动锚点处理**: 移除锚点中的空格，确保链接正确跳转

### 📝 Note 卡片转换
将 Obsidian 的 Note 卡片转换为带有赛博朋克 2077 风格的 HTML 格式：

**支持的 Note 类型**:
- `[!NOTE]` - 信息提示 (青色)
- `[!TIP]` - 技巧提示 (绿色)
- `[!WARNING]` - 警告信息 (黄色)
- `[!DANGER]` - 危险警告 (红色)
- `[!INFO]` - 一般信息 (青色)
- `[!EXAMPLE]` - 示例说明 (紫色)
- `[!QUOTE]` - 引用内容 (紫色)

**设计特色**:
- 🎨 赛博朋克 2077 主题配色
- ✨ 霓虹发光效果和扫描线动画
- 🔤 Orbitron 字体增强科技感
- 📱 响应式设计，支持移动端

### 🖼️ 图片引用转换
- `![[图片名]]` → `![图片名](图片名)`
- 自动修复错误的文件扩展名

### 📄 Hexo 兼容性
- 自动添加 YAML Front Matter
- 内置 CSS 样式，无需额外配置
- 生成当前时间戳

## 安装要求

- Python 3.6+
- 无需额外依赖包

## 使用方法

### 命令行使用

```bash
# 转换单个文件
python obsidian_to_markdown_converter.py input.md -o output.md

# 转换整个目录
python obsidian_to_markdown_converter.py input_dir -o output_dir

# 不添加 CSS 样式
python obsidian_to_markdown_converter.py input.md --no-css
```

### 作为模块使用

```python
from obsidian_to_markdown_converter import ObsidianToMarkdownConverter

# 创建转换器实例
converter = ObsidianToMarkdownConverter()

# 转换单个文件
converter.convert_file('input.md', 'output.md')

# 转换目录
converter.convert_directory('input_dir', 'output_dir')
```

### 直接运行

将脚本放在包含 `CQU校园网解决方案.md` 文件的目录中，直接运行：

```bash
python obsidian_to_markdown_converter.py
```

## 转换示例

### 内部链接转换

**转换前 (Obsidian)**:
```markdown
[[#方案二|点击查看方案二]]
```

**转换后 (标准 Markdown)**:
```markdown
[点击查看方案二](#方案二)
```

### Note 卡片转换

**转换前 (Obsidian)**:
```markdown
> [!NOTE] 重要提示
> 这是一个重要的提示信息
> 请仔细阅读
```

**转换后 (HTML)**:
```html
<div class="note note-info">
  <div class="note-title">
    <span class="note-icon">📝</span>
    <span class="note-text">重要提示</span>
  </div>
  <div class="note-content">
    <p>这是一个重要的提示信息</p>
    <p>请仔细阅读</p>
  </div>
</div>
```

## 输出文件结构

转换后的文件将包含：

1. **YAML Front Matter** - 包含标题、日期、标签等元数据
2. **CSS 样式** - 赛博朋克主题的 Note 卡片样式
3. **转换后的内容** - 标准 Markdown 格式的文档内容

## 特色功能

### 🎨 赛博朋克 2077 主题
- 深色渐变背景
- 霓虹色彩边框和文字
- 发光文字效果
- 扫描线动画
- 闪烁指示器
- 鼠标悬停故障效果

### 🔧 智能处理
- 自动识别和转换各种 Obsidian 语法
- 保持原有的文档结构
- 错误处理和异常捕获
- 支持中文文件名和内容

## 适用场景

- 📝 将 Obsidian 笔记迁移到 Hexo 博客
- 🔄 批量转换 Obsidian 文档格式
- 🎨 为技术文档添加炫酷的视觉效果
- � 学术论文和技术报告的格式转换

## 注意事项

- 转换后的文件包含 HTML 和 CSS，需要支持 HTML 渲染的 Markdown 解析器
- 建议在转换前备份原始文件
- CSS 样式使用了 Google Fonts，需要网络连接才能正常显示字体

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request 来改进这个工具！

---

**让你的 Obsidian 笔记在 Hexo 中闪闪发光！** ✨🚀

## 🤝 贡献指南

1. Fork 本仓库
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 Pull Request

## 📄 更新日志

### v1.0.0 (最新)
- ✨ 新增 Obsidian 插件版本

### v0.5.0
- 🎉 初始版本发布
- 📝 基础 Markdown 转换功能
- 🎨 优化赛博朋克 2077 主题样式
- 🐛 修复图片显示问题
- 🔧 改进锚点生成逻辑
