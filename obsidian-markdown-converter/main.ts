import { Notice, Plugin, TFile, Menu } from 'obsidian';

interface NoteType {
    class: string;
    icon: string;
}

export default class MarkdownConverterPlugin extends Plugin {
    private noteTypes: Record<string, NoteType> = {
        'NOTE': { class: 'info', icon: '📝' },
        'TIP': { class: 'tip', icon: '💡' },
        'WARNING': { class: 'warning', icon: '⚠️' },
        'DANGER': { class: 'danger', icon: '🚨' },
        'INFO': { class: 'info', icon: 'ℹ️' },
        'EXAMPLE': { class: 'example', icon: '📋' },
        'QUOTE': { class: 'quote', icon: '💬' }
    };

    async onload() {
        console.log('Loading Obsidian to Hexo Converter Plugin');

        // 注册右键菜单事件
        this.registerEvent(
            this.app.workspace.on('file-menu', (menu: Menu, file: TFile) => {
                // 只对.md文件显示转换选项
                if (file.extension === 'md') {
                    menu.addItem((item) => {
                        item
                            .setTitle('🔄 转换为Hexo格式')
                            .setIcon('file-text')
                            .onClick(async () => {
                                await this.convertFile(file);
                            });
                    });
                }
            })
        );

        // 添加命令面板命令
        this.addCommand({
            id: 'convert-current-file',
            name: '转换当前文件为Hexo格式',
            checkCallback: (checking: boolean) => {
                const activeFile = this.app.workspace.getActiveFile();
                if (activeFile && activeFile.extension === 'md') {
                    if (!checking) {
                        this.convertFile(activeFile);
                    }
                    return true;
                }
                return false;
            }
        });

        // 添加批量转换命令
        this.addCommand({
            id: 'convert-all-files',
            name: '批量转换当前文件夹的所有MD文件',
            callback: async () => {
                await this.convertAllFiles();
            }
        });
    }

    async convertFile(file: TFile) {
        try {
            new Notice('开始转换文件...');
            
            // 读取文件内容
            const content = await this.app.vault.read(file);
            
            // 执行转换
            let convertedContent = this.convertInternalLinks(content);
            convertedContent = this.convertCrossDocumentLinks(convertedContent);
            convertedContent = this.convertImages(convertedContent);
            convertedContent = this.convertNoteCards(convertedContent);
            
            // 添加Hexo前置信息和CSS
            const hexoContent = this.addHexoFrontMatter(file.basename, convertedContent);
            
            // 创建新文件
            const newFileName = `${file.basename}_converted.md`;
            const newFilePath = file.parent ? `${file.parent.path}/${newFileName}` : newFileName;
            
            // 检查文件是否已存在
            const existingFile = this.app.vault.getAbstractFileByPath(newFilePath);
            if (existingFile) {
                await this.app.vault.delete(existingFile);
            }
            
            await this.app.vault.create(newFilePath, hexoContent);
            
            new Notice(`✅ 转换完成：${newFileName}`);
            
        } catch (error) {
            new Notice(`❌ 转换失败：${error.message}`);
            console.error('转换错误:', error);
        }
    }

    async convertAllFiles() {
        const activeFile = this.app.workspace.getActiveFile();
        if (!activeFile) {
            new Notice('请先打开一个文件');
            return;
        }

        const folder = activeFile.parent;
        if (!folder) {
            new Notice('无法确定当前文件夹');
            return;
        }

        const mdFiles = folder.children.filter(file => 
            file instanceof TFile && file.extension === 'md' && !file.name.includes('_converted')
        ) as TFile[];

        if (mdFiles.length === 0) {
            new Notice('当前文件夹中没有找到MD文件');
            return;
        }

        new Notice(`开始批量转换 ${mdFiles.length} 个文件...`);
        
        let successCount = 0;
        for (const file of mdFiles) {
            try {
                await this.convertFile(file);
                successCount++;
            } catch (error) {
                console.error(`转换文件 ${file.name} 失败:`, error);
            }
        }

        new Notice(`✅ 批量转换完成！成功转换 ${successCount}/${mdFiles.length} 个文件`);
    }

    private convertInternalLinks(content: string): string {
        const generateAnchor = (title: string): string => {
            return title
                .replace(/\s+/g, '-')
                .replace(/[^\w\u4e00-\u9fff-]/g, '')
                .toLowerCase();
        };

        // 转换 [[#标题|显示文本]] 格式
        content = content.replace(/\[\[#([^|\]]+)\|([^\]]+)\]\]/g, (match, title, displayText) => {
            const anchor = generateAnchor(title);
            return `[${displayText}](#${anchor})`;
        });

        // 转换 [[#标题]] 格式
        content = content.replace(/\[\[#([^\]]+)\]\]/g, (match, title) => {
            const anchor = generateAnchor(title);
            return `[${title}](#${anchor})`;
        });

        return content;
    }

    private convertCrossDocumentLinks(content: string): string {
        // 转换跨文档链接
        content = content.replace(/\[\[([^#|\]]+)\|([^\]]+)\]\]/g, '[$2]($1.md)');
        content = content.replace(/\[\[([^#\]]+)\]\]/g, '[$1]($1.md)');
        return content;
    }

    private convertImages(content: string): string {
        // 转换图片引用
        content = content.replace(/!\[\[([^\]]+)\]\]/g, '![$1]($1)');
        content = content.replace(/\.(png|jpg|jpeg|gif|webp)\.md\)/g, '.$1)');
        return content;
    }

    private convertNoteCards(content: string): string {
        const lines = content.split('\n');
        const resultLines: string[] = [];
        let i = 0;

        while (i < lines.length) {
            const line = lines[i];
            const noteMatch = line.match(/^>\s*\[!([A-Z]+)\]\s*(.*)/);
            
            if (noteMatch) {
                const noteType = noteMatch[1];
                const noteTitle = noteMatch[2].trim() || noteType;
                const noteConfig = this.noteTypes[noteType] || { class: 'info', icon: '📝' };
                
                // 收集Note内容
                const noteContent: string[] = [];
                i++;
                while (i < lines.length && lines[i].startsWith('>')) {
                    const contentLine = lines[i].substring(1).trim();
                    if (contentLine) {
                        noteContent.push(contentLine);
                    }
                    i++;
                }
                
                // 生成HTML Note卡片
                const htmlNote = this.generateNoteHtml(noteConfig.class, noteConfig.icon, noteTitle, noteContent);
                resultLines.push(htmlNote);
                i--; // 回退一行
            } else {
                resultLines.push(line);
            }
            i++;
        }

        return resultLines.join('\n');
    }

    private generateNoteHtml(cssClass: string, icon: string, title: string, contentLines: string[]): string {
        const contentHtml = contentLines.map(line => {
            // 检查是否是图片语法
            const imgMatch = line.match(/^!\[([^\]]*)\]\(([^\)]+)\)$/);
            if (imgMatch) {
                const altText = imgMatch[1];
                const imgUrl = imgMatch[2];
                return `  <img src="${imgUrl}" alt="${altText}" style="max-width: 100%; height: auto; border-radius: 4px; margin: 0.5em 0;" />`;
            } else {
                return `  <p>${line}</p>`;
            }
        }).join('\n');

        return `<div class="note note-${cssClass}">
      <div class="note-title">
        <span class="note-icon">${icon}</span>
        <span class="note-text">${title}</span>
      </div>
      <div class="note-content">
    ${contentHtml}
      </div>
    </div>`;
    }

    private addHexoFrontMatter(title: string, content: string): string {
        const currentDate = new Date().toISOString().slice(0, 19).replace('T', ' ');
        const css = this.getCyberpunkCSS();
        
        return `---\ntitle: ${title}\ndate: ${currentDate}\ntags: []\ncategories: []\n---\n\n${css}\n\n${content}`;
    }

    private getCyberpunkCSS(): string {
        return `<style>
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
</style>`;
    }

    onunload() {
        console.log('Unloading Obsidian to Hexo Converter Plugin');
    }
}