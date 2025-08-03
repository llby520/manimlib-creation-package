#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量更新项目中的GitHub URL到实际仓库地址
将所有旧的URL替换为: https://github.com/llby520/manimlib-creation-package
"""

import os
import re
from pathlib import Path
from typing import List, Tuple

class GitHubURLUpdater:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.new_repo_url = "https://github.com/llby520/manimlib-creation-package"
        self.new_repo_git = "https://github.com/llby520/manimlib-creation-package.git"
        self.updated_files = []
        self.errors = []
        
    def get_url_replacements(self) -> List[Tuple[str, str]]:
        """获取需要替换的URL模式"""
        return [
            # 旧仓库URL替换
            (r'https://github\.com/llby520/manimLibfuke', self.new_repo_url),
            (r'https://github\.com/llby520/manimLibfuke\.git', self.new_repo_git),
            
            # 占位符URL替换
            (r'https://github\.com/your-username/manimlib-creation', self.new_repo_url),
            (r'https://github\.com/YOUR_USERNAME/YOUR_REPO', self.new_repo_url),
            (r'https://github\.com/manimlib/creation', self.new_repo_url),
            
            # 特定路径替换
            (r'https://github\.com/llby520/manimLibfuke/actions/workflows/', 
             f'{self.new_repo_url}/actions/workflows/'),
            (r'https://github\.com/llby520/manimLibfuke/issues', 
             f'{self.new_repo_url}/issues'),
            (r'https://github\.com/llby520/manimLibfuke/releases', 
             f'{self.new_repo_url}/releases'),
            (r'https://github\.com/llby520/manimLibfuke/wiki', 
             f'{self.new_repo_url}/wiki'),
            (r'https://github\.com/llby520/manimLibfuke/blob/main/', 
             f'{self.new_repo_url}/blob/main/'),
            (r'https://github\.com/llby520/manimLibfuke/discussions', 
             f'{self.new_repo_url}/discussions'),
            
            # Git clone 命令替换
            (r'git clone https://github\.com/llby520/manimLibfuke\.git', 
             f'git clone {self.new_repo_git}'),
            (r'cd manimlib-creation-package/', 'cd manimlib-creation-package/'),
            
            # 其他占位符
            (r'git remote add origin https://github\.com/YOUR_USERNAME/YOUR_REPO\.git',
             f'git remote add origin {self.new_repo_git}'),
        ]
    
    def should_skip_file(self, file_path: Path) -> bool:
        """检查是否应该跳过某个文件"""
        skip_patterns = [
            '__pycache__',
            '.git',
            '.pyc',
            '.egg-info',
            'build',
            'dist',
            '.zip',
            'node_modules',
            '.venv',
            'venv',
        ]
        
        file_str = str(file_path)
        return any(pattern in file_str for pattern in skip_patterns)
    
    def update_file(self, file_path: Path) -> bool:
        """更新单个文件中的URL"""
        if self.should_skip_file(file_path):
            return False
            
        try:
            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            original_content = content
            replacements = self.get_url_replacements()
            
            # 执行替换
            for pattern, replacement in replacements:
                content = re.sub(pattern, replacement, content)
            
            # 如果内容有变化，写回文件
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return True
                
        except Exception as e:
            self.errors.append(f"处理文件 {file_path} 时出错: {e}")
            return False
        
        return False
    
    def update_all_files(self) -> None:
        """更新所有文件"""
        print(f"🔄 开始更新项目中的GitHub URL...")
        print(f"📁 项目根目录: {self.project_root}")
        print(f"🎯 新仓库地址: {self.new_repo_url}")
        print()
        
        # 遍历所有文件
        for file_path in self.project_root.rglob('*'):
            if file_path.is_file():
                if self.update_file(file_path):
                    self.updated_files.append(str(file_path.relative_to(self.project_root)))
                    print(f"✅ 已更新: {file_path.relative_to(self.project_root)}")
        
        # 输出结果
        print(f"\n📊 更新完成!")
        print(f"✅ 成功更新 {len(self.updated_files)} 个文件")
        
        if self.errors:
            print(f"❌ 处理过程中出现 {len(self.errors)} 个错误:")
            for error in self.errors:
                print(f"   {error}")
        
        if self.updated_files:
            print("\n📝 已更新的文件列表:")
            for file in self.updated_files:
                print(f"   - {file}")
        
        print(f"\n🎉 所有GitHub URL已更新为: {self.new_repo_url}")
        print("\n📋 后续步骤:")
        print("1. 检查更新结果")
        print("2. 提交更改到Git")
        print("3. 推送到GitHub仓库")
        print("4. 验证所有链接是否正常工作")

def main():
    """主函数"""
    project_root = Path(__file__).parent
    updater = GitHubURLUpdater(str(project_root))
    updater.update_all_files()

if __name__ == "__main__":
    main()