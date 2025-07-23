import re
import os
import argparse
from pathlib import Path

class ObsidianToMarkdownConverter:
    def __init__(self):
        self.note_types = {
            'NOTE': ('info', '📝'),
            'TIP': ('tip', '💡'),
            'WARNING': ('warning', '⚠️'),
            'DANGER': ('danger', '🚨'),
            'INFO': ('info', 'ℹ️'),
            'EXAMPLE': ('example', '📋'),
            'QUOTE': ('quote', '💬')
        }
    
    def convert_internal_links(self, content):
        """
        转换内部链接格式
        [[#标题|显示文本]] -> [显示文本](#标题)
        [[#标题]] -> [标题](#标题)
        """
        # 匹配 [[#标题|显示文本]] 格式
        def replace_with_display_text(match):
            anchor = match.group(1).replace(' ', '')
            display_text = match.group(2)
            return f'[{display_text}](#{anchor})'
        
        pattern1 = r'\[\[#([^|\]]+)\|([^\]]+)\]\]'
        content = re.sub(pattern1, replace_with_display_text, content)
        
        # 匹配 [[#标题]] 格式
        def replace_without_display_text(match):
            title = match.group(1)
            anchor = title.replace(' ', '')
            return f'[{title}](#{anchor})'
        
        pattern2 = r'\[\[#([^\]]+)\]\]'
        content = re.sub(pattern2, replace_without_display_text, content)
        
        return content
    
    def convert_cross_document_links(self, content):
        """
        转换跨文档链接
        [[文档名]] -> [文档名](文档名.md)
        [[文档名|显示文本]] -> [显示文本](文档名.md)
        """
        # 匹配 [[文档名|显示文本]] 格式（不包含#的跨文档链接）
        pattern1 = r'\[\[([^#|\]]+)\|([^\]]+)\]\]'
        content = re.sub(pattern1, r'[\2](\1.md)', content)
        
        # 匹配 [[文档名]] 格式（不包含#的跨文档链接）
        pattern2 = r'\[\[([^#\]]+)\]\]'
        content = re.sub(pattern2, r'[\1](\1.md)', content)
        
        return content
    
    def convert_note_cards(self, content):
        """
        转换Note卡片为HTML格式
        > [!NOTE] 标题
        > 内容
        """
        lines = content.split('\n')
        result_lines = []
        i = 0
        
        while i < len(lines):
            line = lines[i]
            
            # 检查是否是Note卡片的开始
            note_match = re.match(r'^>\s*\[!([A-Z]+)\]\s*(.*)', line)
            if note_match:
                note_type = note_match.group(1)
                note_title = note_match.group(2).strip()
                
                # 获取Note类型对应的样式
                if note_type in self.note_types:
                    css_class, icon = self.note_types[note_type]
                else:
                    css_class, icon = 'info', '📝'
                
                # 如果没有标题，使用默认标题
                if not note_title:
                    note_title = note_type.title()
                
                # 收集Note内容
                note_content = []
                i += 1
                while i < len(lines) and lines[i].startswith('>'):
                    content_line = lines[i][1:].strip()  # 移除 > 符号
                    if content_line:  # 只添加非空行
                        note_content.append(content_line)
                    i += 1
                
                # 生成HTML Note卡片
                html_note = self.generate_note_html(css_class, icon, note_title, note_content)
                result_lines.append(html_note)
                
                # 回退一行，因为while循环会再次递增
                i -= 1
            else:
                result_lines.append(line)
            
            i += 1
        
        return '\n'.join(result_lines)
    
    def generate_note_html(self, css_class, icon, title, content_lines):
        """
        生成HTML格式的Note卡片
        """
        content_html = '\n'.join([f'  <p>{line}</p>' for line in content_lines if line])
        
        html = f'''<div class="note note-{css_class}">
  <div class="note-title">
    <span class="note-icon">{icon}</span>
    <span class="note-text">{title}</span>
  </div>
  <div class="note-content">
{content_html}
  </div>
</div>'''
        
        return html
    
    def convert_file(self, input_file, output_file=None, add_css=True):
        """
        转换单个文件
        """
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 执行转换
            content = self.convert_internal_links(content)
            content = self.convert_cross_document_links(content)
            content = self.convert_images(content)
            content = self.convert_note_cards(content)
            
            # 为Hexo添加YAML front matter和CSS样式
            if add_css:
                # 从原文件名提取标题
                input_path = Path(input_file)
                title = input_path.stem.replace('_', ' ')
                
                # 构建完整的Hexo文档
                hexo_content = f'''---
title: {title}
date: {self.get_current_date()}
tags: []
categories: []
---

{self.add_css_styles()}

{content}'''
                content = hexo_content
            
            # 确定输出文件名
            if output_file is None:
                input_path = Path(input_file)
                output_file = input_path.parent / f"{input_path.stem}_converted{input_path.suffix}"
            
            # 写入转换后的内容
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"转换完成: {input_file} -> {output_file}")
            return True
            
        except Exception as e:
            print(f"转换失败: {e}")
            return False
    
    def get_current_date(self):
        """
        获取当前日期，格式为YYYY-MM-DD HH:MM:SS
        """
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def convert_images(self, content):
        """
        转换图片引用
        ![[图片名]] -> ![图片名](图片名)
        """
        pattern = r'!\[\[([^\]]+)\]\]'
        # 修正图片链接，移除错误的.md后缀
        content = re.sub(pattern, r'![\1](\1)', content)
        # 修复可能存在的.png.md这样的错误后缀
        content = re.sub(r'\.(png|jpg|jpeg|gif|webp)\.md\)', r'.\1)', content)
        return content
    
    def add_css_styles(self):
        """
        返回Note卡片的CSS样式 - 赛博朋克2077风格
        """
        css = '''
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');

.note {
  margin: 1.5em 0;
  padding: 1.2em;
  border: 2px solid;
  border-radius: 8px;
  background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
  box-shadow: 0 0 20px rgba(0, 255, 255, 0.3), inset 0 0 20px rgba(0, 0, 0, 0.5);
  font-family: 'Orbitron', monospace;
  position: relative;
  overflow: hidden;
}

.note::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(0, 255, 255, 0.1), transparent);
  animation: scan 3s infinite;
}

@keyframes scan {
  0% { left: -100%; }
  100% { left: 100%; }
}

.note-info {
  border-color: #00ffff;
  color: #00ffff;
  text-shadow: 0 0 10px #00ffff;
}

.note-tip {
  border-color: #39ff14;
  color: #39ff14;
  text-shadow: 0 0 10px #39ff14;
}

.note-warning {
  border-color: #ffff00;
  color: #ffff00;
  text-shadow: 0 0 10px #ffff00;
}

.note-danger {
  border-color: #ff073a;
  color: #ff073a;
  text-shadow: 0 0 10px #ff073a;
}

.note-example {
  border-color: #ff00ff;
  color: #ff00ff;
  text-shadow: 0 0 10px #ff00ff;
}

.note-quote {
  border-color: #9d4edd;
  color: #9d4edd;
  text-shadow: 0 0 10px #9d4edd;
}

.note-title {
  font-weight: 900;
  font-size: 1.1em;
  margin-bottom: 0.8em;
  display: flex;
  align-items: center;
  text-transform: uppercase;
  letter-spacing: 2px;
  border-bottom: 1px solid currentColor;
  padding-bottom: 0.5em;
  position: relative;
  z-index: 1;
}

.note-icon {
  margin-right: 0.8em;
  font-size: 1.2em;
  filter: drop-shadow(0 0 5px currentColor);
}

.note-text {
  position: relative;
}

.note-content {
  position: relative;
  z-index: 1;
}

.note-content p {
  margin: 0.8em 0;
  line-height: 1.6;
  font-weight: 400;
  background: rgba(0, 0, 0, 0.3);
  padding: 0.5em;
  border-radius: 4px;
  border-left: 3px solid currentColor;
}

.note-content p:first-child {
  margin-top: 0;
}

.note-content p:last-child {
  margin-bottom: 0;
}

/* 添加闪烁效果 */
.note-title::after {
  content: '';
  position: absolute;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 8px;
  height: 8px;
  background: currentColor;
  border-radius: 50%;
  animation: blink 1.5s infinite;
}

@keyframes blink {
  0%, 50% { opacity: 1; }
  51%, 100% { opacity: 0; }
}

/* 鼠标悬停效果 */
.note:hover {
  transform: translateY(-2px);
  box-shadow: 0 0 30px rgba(0, 255, 255, 0.5), inset 0 0 30px rgba(0, 0, 0, 0.7);
  transition: all 0.3s ease;
}

.note:hover .note-title {
  animation: glitch 0.5s infinite;
}

@keyframes glitch {
  0% { transform: translateX(0); }
  10% { transform: translateX(-2px); }
  20% { transform: translateX(2px); }
  30% { transform: translateX(-1px); }
  40% { transform: translateX(1px); }
  50% { transform: translateX(0); }
  100% { transform: translateX(0); }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .note {
    margin: 1em 0;
    padding: 1em;
  }
  
  .note-title {
    font-size: 1em;
    letter-spacing: 1px;
  }
}
</style>
'''
        return css
    
    def convert_directory(self, input_dir, output_dir=None, add_css=True):
        """
        转换目录中的所有Markdown文件
        """
        input_path = Path(input_dir)
        if output_dir is None:
            output_path = input_path / "converted"
        else:
            output_path = Path(output_dir)
        
        # 创建输出目录
        output_path.mkdir(exist_ok=True)
        
        # 转换所有.md文件
        md_files = list(input_path.glob("*.md"))
        if not md_files:
            print(f"在 {input_dir} 中没有找到Markdown文件")
            return
        
        for md_file in md_files:
            output_file = output_path / md_file.name
            self.convert_file(md_file, output_file, add_css)

def main():
    parser = argparse.ArgumentParser(description='将Obsidian Markdown转换为标准Markdown')
    parser.add_argument('input', help='输入文件或目录路径')
    parser.add_argument('-o', '--output', help='输出文件或目录路径')
    parser.add_argument('--no-css', action='store_true', help='不添加CSS样式')
    
    args = parser.parse_args()
    
    converter = ObsidianToMarkdownConverter()
    
    input_path = Path(args.input)
    add_css = not args.no_css
    
    if input_path.is_file():
        converter.convert_file(args.input, args.output, add_css)
    elif input_path.is_dir():
        converter.convert_directory(args.input, args.output, add_css)
    else:
        print(f"错误: {args.input} 不是有效的文件或目录")

if __name__ == "__main__":
    # 如果直接运行脚本，可以在这里测试
    converter = ObsidianToMarkdownConverter()
    
    # 转换当前目录下的CQU校园网解决方案.md文件
    current_file = "CQU校园网解决方案.md"
    if os.path.exists(current_file):
        converter.convert_file(current_file)
        print("\n转换完成！生成的文件包含了CSS样式，可以直接在支持HTML的Markdown渲染器中查看。")
        print("\n主要转换内容：")
        print("1. 内部链接 [[#标题|文本]] -> [文本](#标题)")
        print("2. Note卡片 > [!NOTE] -> HTML格式的提示框")
        print("3. 图片引用 ![[图片]] -> ![图片](图片)")
        print("4. 跨文档链接 [[文档名]] -> [文档名](文档名.md)")
    else:
        print("请将此脚本放在包含Obsidian Markdown文件的目录中运行")
        print("\n使用方法：")
        print("python obsidian_to_markdown_converter.py <输入文件或目录> [-o 输出路径] [--no-css]")