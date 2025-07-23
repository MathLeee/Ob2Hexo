# InLnJpO2H
一个Obsidian的链接格式规范器，将你的Obsidian文章链接风格一键更改为Hexo可识别的格式

## Obsidian vs HTML 链接格式对比

主要的转换需求包括：<mcreference link="https://help.obsidian.md/links" index="3">参考obsidian官方文档</mcreference>

1. **Obsidian Wikilink格式**: `[[文件名]]` 或 `[[文件名|显示文本]]`
2. **Obsidian 内部锚点**: `[[#标题]]` 或 `[[#^块ID]]`
3. **Obsidian 图片嵌入**: `![[图片名.png]]`
4. **HTML 锚点格式**: `<a href="#anchor-id">显示文本</a>` 或 `[显示文本](#anchor-id)`

## 使用方法

### 1. 转换单个文件
```bash
python obsidian_to_html_converter.py "目标文档地址"
```

### 2. 转换整个目录
```bash
python obsidian_to_html_converter.py . -o ./converted
```

### 3. 自定义路径设置
```bash
python obsidian_to_html_converter.py "目标文档地址" --image-path "/assets/images/" --file-path "/posts/"
```

## 转换示例

基于我的文档，以下是转换效果：

**转换前（Obsidian格式）：**
```markdown
![[Pasted image 20250722213238.png]]
[[#2. 大佬搭建的的云端编译平台（牛逼，编译速度快）|方案二]]
[[#^11cf71|23.05.4]]
```

**转换后（HTML格式）：**
```markdown
![Pasted image 20250722213238](/images/Pasted image 20250722213238.png)
<a href="#2-大佬搭建的的云端编译平台牛逼编译速度快">方案二</a>
<a href="#11cf71">23.05.4</a>
```

## 程序特点

1. **全面支持**：处理所有常见的Obsidian链接格式<mcreference link="https://help.obsidian.md/links" index="3">3</mcreference>
2. **智能转换**：自动将中文标题转换为HTML友好的锚点ID
3. **批量处理**：支持单文件和整个目录的批量转换
4. **路径自定义**：可以自定义图片和文件的基础路径
5. **安全备份**：可以指定输出目录，避免覆盖原文件
6. **错误处理**：完善的错误处理和进度反馈

这个程序应该能够满足您将Obsidian文档转换为Hexo兼容格式的需求。您可以根据具体的Hexo配置调整图片和文件的基础路径。
