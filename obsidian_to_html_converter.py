#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Obsidian到HTML链接转换器
将Obsidian的内部链接语法转换为HTML格式，适用于Hexo等静态网站生成器
"""

import re
import os
import argparse
from pathlib import Path

class ObsidianToHtmlConverter:
    def __init__(self):
        # 编译正则表达式模式
        self.patterns = {
            # 匹配 [[#标题]] 格式的内部锚点链接
            'internal_anchor': re.compile(r'\[\[#([^\]]+?)\]\]'),
            
            # 匹配 [[#标题|显示文本]] 格式的内部锚点链接
            'internal_anchor_with_text': re.compile(r'\[\[#([^\|\]]+?)\|([^\]]+?)\]\]'),
            
            # 匹配 [[#^块ID]] 格式的块引用
            'block_reference': re.compile(r'\[\[#\^([^\]]+?)\]\]'),
            
            # 匹配 [[#^块ID|显示文本]] 格式的块引用
            'block_reference_with_text': re.compile(r'\[\[#\^([^\|\]]+?)\|([^\]]+?)\]\]'),
            
            # 匹配 ![[图片.png]] 格式的图片嵌入
            'image_embed': re.compile(r'!\[\[([^\]]+?\.(png|jpg|jpeg|gif|svg|webp))\]\]', re.IGNORECASE),
            
            # 匹配 [[文件名]] 格式的文件链接
            'file_link': re.compile(r'\[\[([^#\^\|\]]+?)\]\]'),
            
            # 匹配 [[文件名|显示文本]] 格式的文件链接
            'file_link_with_text': re.compile(r'\[\[([^#\^\|\]]+?)\|([^\]]+?)\]\]')
        }
    
    def convert_to_anchor_id(self, text):
        """
        将文本转换为HTML锚点ID格式
        遵循HTML标准：小写、空格转连字符、移除特殊字符
        """
        # 转换为小写
        anchor_id = text.lower()
        # 空格转连字符
        anchor_id = re.sub(r'\s+', '-', anchor_id)
        # 移除特殊字符，只保留字母、数字、连字符
        anchor_id = re.sub(r'[^a-z0-9\-\u4e00-\u9fff]', '', anchor_id)
        # 移除多余的连字符
        anchor_id = re.sub(r'-+', '-', anchor_id)
        # 移除首尾连字符
        anchor_id = anchor_id.strip('-')
        return anchor_id
    
    def convert_internal_anchors(self, content):
        """
        转换内部锚点链接
        [[#标题]] -> <a href="#标题">标题</a>
        [[#标题|显示文本]] -> <a href="#标题">显示文本</a>
        """
        # 处理带显示文本的锚点链接
        def replace_anchor_with_text(match):
            anchor = match.group(1)
            display_text = match.group(2)
            anchor_id = self.convert_to_anchor_id(anchor)
            return f'<a href="#{anchor_id}">{display_text}</a>'
        
        content = self.patterns['internal_anchor_with_text'].sub(replace_anchor_with_text, content)
        
        # 处理普通锚点链接
        def replace_anchor(match):
            anchor = match.group(1)
            anchor_id = self.convert_to_anchor_id(anchor)
            return f'<a href="#{anchor_id}">{anchor}</a>'
        
        content = self.patterns['internal_anchor'].sub(replace_anchor, content)
        
        return content
    
    def convert_block_references(self, content):
        """
        转换块引用
        [[#^块ID]] -> <a href="#块ID">块ID</a>
        [[#^块ID|显示文本]] -> <a href="#块ID">显示文本</a>
        """
        # 处理带显示文本的块引用
        def replace_block_with_text(match):
            block_id = match.group(1)
            display_text = match.group(2)
            return f'<a href="#{block_id}">{display_text}</a>'
        
        content = self.patterns['block_reference_with_text'].sub(replace_block_with_text, content)
        
        # 处理普通块引用
        def replace_block(match):
            block_id = match.group(1)
            return f'<a href="#{block_id}">{block_id}</a>'
        
        content = self.patterns['block_reference'].sub(replace_block, content)
        
        return content
    
    def convert_image_embeds(self, content, image_base_path="/images/"):
        """
        转换图片嵌入
        ![[图片.png]] -> ![图片](图片路径)
        """
        def replace_image(match):
            image_name = match.group(1)
            # 移除文件扩展名作为alt文本
            alt_text = os.path.splitext(image_name)[0]
            return f'![{alt_text}]({image_base_path}{image_name})'
        
        return self.patterns['image_embed'].sub(replace_image, content)
    
    def convert_file_links(self, content, base_path="/"):
        """
        转换文件链接
        [[文件名]] -> [文件名](文件路径)
        [[文件名|显示文本]] -> [显示文本](文件路径)
        """
        # 处理带显示文本的文件链接
        def replace_file_with_text(match):
            filename = match.group(1)
            display_text = match.group(2)
            # 将文件名转换为URL友好格式
            url_filename = filename.replace(' ', '-').lower()
            return f'[{display_text}]({base_path}{url_filename}/)'
        
        content = self.patterns['file_link_with_text'].sub(replace_file_with_text, content)
        
        # 处理普通文件链接
        def replace_file(match):
            filename = match.group(1)
            # 将文件名转换为URL友好格式
            url_filename = filename.replace(' ', '-').lower()
            return f'[{filename}]({base_path}{url_filename}/)'
        
        content = self.patterns['file_link'].sub(replace_file, content)
        
        return content
    
    def convert_content(self, content, image_base_path="/images/", file_base_path="/"):
        """
        转换所有Obsidian链接格式到HTML格式
        """
        # 按顺序进行转换，避免冲突
        content = self.convert_internal_anchors(content)
        content = self.convert_block_references(content)
        content = self.convert_image_embeds(content, image_base_path)
        content = self.convert_file_links(content, file_base_path)
        
        return content
    
    def convert_file(self, input_file, output_file=None, image_base_path="/images/", file_base_path="/"):
        """
        转换单个文件
        """
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            converted_content = self.convert_content(content, image_base_path, file_base_path)
            
            if output_file is None:
                # 如果没有指定输出文件，则覆盖原文件
                output_file = input_file
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(converted_content)
            
            print(f"✅ 转换完成: {input_file} -> {output_file}")
            return True
            
        except Exception as e:
            print(f"❌ 转换失败 {input_file}: {str(e)}")
            return False
    
    def convert_directory(self, input_dir, output_dir=None, image_base_path="/images/", file_base_path="/"):
        """
        批量转换目录中的所有markdown文件
        """
        input_path = Path(input_dir)
        
        if output_dir is None:
            output_path = input_path
        else:
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
        
        success_count = 0
        total_count = 0
        
        for md_file in input_path.rglob('*.md'):
            total_count += 1
            
            if output_dir is None:
                output_file = md_file
            else:
                # 保持相对路径结构
                relative_path = md_file.relative_to(input_path)
                output_file = output_path / relative_path
                output_file.parent.mkdir(parents=True, exist_ok=True)
            
            if self.convert_file(md_file, output_file, image_base_path, file_base_path):
                success_count += 1
        
        print(f"\n📊 转换统计: {success_count}/{total_count} 个文件转换成功")

def main():
    parser = argparse.ArgumentParser(description='将Obsidian链接格式转换为HTML格式')
    parser.add_argument('input', help='输入文件或目录路径')
    parser.add_argument('-o', '--output', help='输出文件或目录路径（可选，默认覆盖原文件）')
    parser.add_argument('--image-path', default='/images/', help='图片基础路径（默认: /images/）')
    parser.add_argument('--file-path', default='/', help='文件基础路径（默认: /）')
    
    args = parser.parse_args()
    
    converter = ObsidianToHtmlConverter()
    
    input_path = Path(args.input)
    
    if input_path.is_file():
        # 转换单个文件
        converter.convert_file(args.input, args.output, args.image_path, args.file_path)
    elif input_path.is_dir():
        # 转换目录
        converter.convert_directory(args.input, args.output, args.image_path, args.file_path)
    else:
        print(f"❌ 错误: 路径 '{args.input}' 不存在")

if __name__ == '__main__':
    main()