#!/usr/bin/env python3
"""
GitHub URL 更新脚本

这个脚本帮助更新 pyproject.toml 中的 GitHub URL 为您的实际仓库地址。

使用方法:
    python update_github_urls.py YOUR_USERNAME YOUR_REPO_NAME
    
示例:
    python update_github_urls.py myusername my-manimlib-creation
"""

import sys
import re
from pathlib import Path


def update_github_urls(username: str, repo_name: str, project_root: str = None) -> bool:
    """更新 GitHub URLs
    
    Args:
        username: GitHub 用户名
        repo_name: 仓库名称
        project_root: 项目根目录路径
    
    Returns:
        bool: 更新是否成功
    """
    if not project_root:
        project_root = Path.cwd()
    else:
        project_root = Path(project_root)
    
    # 文件路径
    pyproject_file = project_root / "creationbuild_package" / "pyproject.toml"
    readme_file = project_root / "README.md"
    
    if not pyproject_file.exists():
        print(f"❌ 错误: 找不到 {pyproject_file}")
        return False
    
    # 新的 GitHub URLs
    new_base_url = f"https://github.com/{username}/{repo_name}"
    new_urls = {
        'Homepage': new_base_url,
        'Documentation': f"{new_base_url}/wiki",
        'Repository': f"{new_base_url}.git",
        'Bug Tracker': f"{new_base_url}/issues",
        'Changelog': f"{new_base_url}/blob/main/CHANGELOG.md"
    }
    
    print(f"🔄 更新 GitHub URLs 为: {new_base_url}")
    
    # 更新 pyproject.toml
    try:
        with open(pyproject_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 替换 URL 部分
        url_section_pattern = r'(\[project\.urls\][\s\S]*?)(?=\n\[|\Z)'
        
        def replace_urls(match):
            section = match.group(1)
            new_section = "[project.urls]\n"
            for key, url in new_urls.items():
                new_section += f'{key} = "{url}"\n'
            return new_section
        
        new_content = re.sub(url_section_pattern, replace_urls, content)
        
        with open(pyproject_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✅ 已更新 {pyproject_file}")
        
    except Exception as e:
        print(f"❌ 更新 pyproject.toml 失败: {e}")
        return False
    
    # 更新 README.md
    if readme_file.exists():
        try:
            with open(readme_file, 'r', encoding='utf-8') as f:
                readme_content = f.read()
            
            # 替换 README 中的示例 URLs
            old_url_pattern = r'https://github\.com/llby520/manimLibfuke'
            new_readme_content = re.sub(old_url_pattern, new_base_url, readme_content)
            
            # 替换 badge URLs
            badge_patterns = [
                (r'\(https://github\.com/llby520/manimLibfuke/actions/workflows/([^)]+)\)', 
                 f'({new_base_url}/actions/workflows/\\1)'),
                (r'https://github\.com/llby520/manimLibfuke\.git', 
                 f'{new_base_url}.git')
            ]
            
            for pattern, replacement in badge_patterns:
                new_readme_content = re.sub(pattern, replacement, new_readme_content)
            
            with open(readme_file, 'w', encoding='utf-8') as f:
                f.write(new_readme_content)
            
            print(f"✅ 已更新 {readme_file}")
            
        except Exception as e:
            print(f"⚠️  更新 README.md 失败: {e}")
    
    # 显示更新后的 URLs
    print("\n📋 更新后的 URLs:")
    print("=" * 40)
    for key, url in new_urls.items():
        print(f"  {key}: {url}")
    
    print("\n🎉 GitHub URLs 更新完成!")
    print("\n📝 下一步:")
    print("  1. 检查更新后的文件")
    print("  2. 提交更改: git add . && git commit -m 'Update GitHub URLs'")
    print(f"  3. 创建 GitHub 仓库: {new_base_url}")
    print("  4. 推送代码: git push -u origin main")
    
    return True


def main():
    """主函数"""
    if len(sys.argv) != 3:
        print("❌ 用法: python update_github_urls.py USERNAME REPO_NAME")
        print("\n示例:")
        print("  python update_github_urls.py myusername my-manimlib-creation")
        print("  python update_github_urls.py john-doe manimlib-creation-fork")
        sys.exit(1)
    
    username = sys.argv[1]
    repo_name = sys.argv[2]
    
    # 验证输入
    if not re.match(r'^[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?$', username):
        print("❌ 错误: 无效的 GitHub 用户名")
        sys.exit(1)
    
    if not re.match(r'^[a-zA-Z0-9._-]+$', repo_name):
        print("❌ 错误: 无效的仓库名称")
        sys.exit(1)
    
    print(f"🎯 更新 GitHub URLs")
    print(f"   用户名: {username}")
    print(f"   仓库名: {repo_name}")
    print("=" * 50)
    
    success = update_github_urls(username, repo_name)
    
    if not success:
        print("\n❌ 更新失败")
        sys.exit(1)


if __name__ == "__main__":
    main()