#!/usr/bin/env python3
"""
GitHub 发布准备脚本

这个脚本帮助准备 manimlib-creation 包的 GitHub 发布。
它会检查所有必要的文件，验证配置，并提供发布指导。

使用方法:
    python prepare_github_release.py
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import List, Dict, Any


class GitHubReleasePreparator:
    """GitHub 发布准备器"""
    
    def __init__(self, project_root: str = None):
        self.project_root = Path(project_root or os.getcwd())
        self.package_dir = self.project_root / "creationbuild_package"
        self.errors = []
        self.warnings = []
        self.success_items = []
    
    def check_file_exists(self, file_path: Path, description: str) -> bool:
        """检查文件是否存在"""
        if file_path.exists():
            self.success_items.append(f"✅ {description}: {file_path}")
            return True
        else:
            self.errors.append(f"❌ 缺少 {description}: {file_path}")
            return False
    
    def check_directory_structure(self) -> None:
        """检查目录结构"""
        print("🔍 检查项目目录结构...")
        
        # 必需的文件
        required_files = [
            (self.project_root / "creation.py", "根目录核心模块"),
            (self.project_root / "PROJECT_OVERVIEW.md", "项目概览文档"),
            (self.package_dir / "creation.py", "包目录核心模块"),
            (self.package_dir / "pyproject.toml", "项目配置文件"),
            (self.package_dir / "README_creation.md", "包说明文档"),
            (self.package_dir / "LICENSE", "许可证文件"),
            (self.package_dir / "CHANGELOG.md", "变更日志"),
            (self.package_dir / "test_creation.py", "测试文件"),
            (self.package_dir / "requirements_creation.txt", "依赖文件"),
            (self.package_dir / "environment.yml", "Conda 环境文件"),
            (self.package_dir / "meta.yaml", "Conda 构建文件"),
        ]
        
        # GitHub Actions 文件
        github_files = [
            (self.project_root / ".github" / "workflows" / "python-package.yml", "Python 包 CI/CD"),
            (self.project_root / ".github" / "workflows" / "python-package-conda.yml", "Conda 包 CI/CD"),
            (self.project_root / ".github" / "GITHUB_ACTIONS_GUIDE.md", "GitHub Actions 指南"),
        ]
        
        for file_path, description in required_files + github_files:
            self.check_file_exists(file_path, description)
    
    def check_pyproject_toml(self) -> None:
        """检查 pyproject.toml 配置"""
        print("\n🔍 检查 pyproject.toml 配置...")
        
        pyproject_file = self.package_dir / "pyproject.toml"
        if not pyproject_file.exists():
            self.errors.append("❌ pyproject.toml 文件不存在")
            return
        
        try:
            import tomllib
        except ImportError:
            try:
                import tomli as tomllib
            except ImportError:
                self.warnings.append("⚠️  无法导入 tomllib/tomli，跳过 TOML 验证")
                return
        
        try:
            with open(pyproject_file, 'rb') as f:
                config = tomllib.load(f)
            
            # 检查项目基本信息
            project = config.get('project', {})
            if project.get('name') == 'manimlib-creation':
                self.success_items.append("✅ 项目名称配置正确")
            else:
                self.errors.append(f"❌ 项目名称错误: {project.get('name')}")
            
            # 检查 URL 配置
            urls = project.get('urls', {})
            github_url = urls.get('Homepage', '')
            if 'github.com' in github_url:
                if 'YOUR_USERNAME' in github_url or 'example.com' in github_url:
                    self.warnings.append("⚠️  GitHub URL 仍为示例地址，请更新为您的实际仓库地址")
                else:
                    self.success_items.append(f"✅ GitHub URL 已配置: {github_url}")
            else:
                self.errors.append("❌ GitHub URL 未正确配置")
            
            # 检查依赖
            dependencies = project.get('dependencies', [])
            if dependencies:
                self.success_items.append(f"✅ 依赖配置: {len(dependencies)} 个包")
            else:
                self.warnings.append("⚠️  未配置依赖包")
                
        except Exception as e:
            self.errors.append(f"❌ 解析 pyproject.toml 失败: {e}")
    
    def check_git_status(self) -> None:
        """检查 Git 状态"""
        print("\n🔍 检查 Git 状态...")
        
        try:
            # 检查是否在 Git 仓库中
            result = subprocess.run(['git', 'status'], 
                                  capture_output=True, text=True, cwd=self.project_root)
            if result.returncode == 0:
                self.success_items.append("✅ 项目已初始化为 Git 仓库")
                
                # 检查是否有未提交的更改
                if 'nothing to commit' in result.stdout:
                    self.success_items.append("✅ 工作目录干净，无未提交更改")
                else:
                    self.warnings.append("⚠️  有未提交的更改，建议先提交")
                
                # 检查远程仓库
                remote_result = subprocess.run(['git', 'remote', '-v'], 
                                             capture_output=True, text=True, cwd=self.project_root)
                if remote_result.returncode == 0 and remote_result.stdout.strip():
                    self.success_items.append("✅ 已配置远程仓库")
                else:
                    self.warnings.append("⚠️  未配置远程 GitHub 仓库")
            else:
                self.warnings.append("⚠️  项目未初始化为 Git 仓库")
                
        except FileNotFoundError:
            self.warnings.append("⚠️  Git 未安装或不在 PATH 中")
        except Exception as e:
            self.warnings.append(f"⚠️  检查 Git 状态时出错: {e}")
    
    def check_package_build(self) -> None:
        """检查包构建"""
        print("\n🔍 检查包构建...")
        
        dist_dir = self.package_dir / "dist"
        if dist_dir.exists():
            wheel_files = list(dist_dir.glob("*.whl"))
            tar_files = list(dist_dir.glob("*.tar.gz"))
            
            if wheel_files:
                self.success_items.append(f"✅ 找到 wheel 文件: {len(wheel_files)} 个")
            if tar_files:
                self.success_items.append(f"✅ 找到 tar.gz 文件: {len(tar_files)} 个")
            
            if not wheel_files and not tar_files:
                self.warnings.append("⚠️  dist 目录存在但无构建文件")
        else:
            self.warnings.append("⚠️  未找到 dist 目录，需要先构建包")
    
    def generate_release_checklist(self) -> None:
        """生成发布检查清单"""
        print("\n📋 GitHub 发布检查清单:")
        print("="*50)
        
        checklist = [
            "1. 确保所有代码已提交到 Git",
            "2. 更新版本号 (pyproject.toml)",
            "3. 更新 CHANGELOG.md",
            "4. 运行所有测试确保通过",
            "5. 构建包: cd creationbuild_package && python -m build",
            "6. 测试包安装: pip install dist/*.whl",
            "7. 创建 GitHub 仓库 (如果还没有)",
            "8. 推送代码到 GitHub",
            "9. 创建 GitHub Release",
            "10. 上传构建的包到 PyPI (可选)",
        ]
        
        for item in checklist:
            print(f"  □ {item}")
    
    def generate_github_commands(self) -> None:
        """生成 GitHub 操作命令"""
        print("\n🚀 GitHub 操作命令:")
        print("="*50)
        
        commands = [
            "# 1. 初始化 Git 仓库 (如果还没有)",
            "git init",
            "git add .",
            'git commit -m "Initial commit: Manimlib Creation Package"',
            "",
            "# 2. 添加远程仓库",
            "git remote add origin https://github.com/llby520/manimLibfuke.git",
            "",
            "# 3. 推送到 GitHub",
            "git branch -M main",
            "git push -u origin main",
            "",
            "# 4. 构建包",
            "cd creationbuild_package",
            "python -m build",
            "",
            "# 5. 测试包",
            "pip install dist/*.whl",
            "python -c 'import creation; creation._module_self_test()'",
        ]
        
        for cmd in commands:
            print(f"  {cmd}")
    
    def run_checks(self) -> None:
        """运行所有检查"""
        print("🎯 Manimlib Creation Package - GitHub 发布准备")
        print("="*60)
        
        self.check_directory_structure()
        self.check_pyproject_toml()
        self.check_git_status()
        self.check_package_build()
        
        # 显示结果
        print("\n📊 检查结果:")
        print("="*30)
        
        if self.success_items:
            print("\n✅ 成功项目:")
            for item in self.success_items:
                print(f"  {item}")
        
        if self.warnings:
            print("\n⚠️  警告项目:")
            for warning in self.warnings:
                print(f"  {warning}")
        
        if self.errors:
            print("\n❌ 错误项目:")
            for error in self.errors:
                print(f"  {error}")
        
        # 生成指导
        self.generate_release_checklist()
        self.generate_github_commands()
        
        # 总结
        print("\n📈 总结:")
        print("="*20)
        print(f"✅ 成功: {len(self.success_items)}")
        print(f"⚠️  警告: {len(self.warnings)}")
        print(f"❌ 错误: {len(self.errors)}")
        
        if self.errors:
            print("\n❗ 请先解决所有错误再进行发布")
            return False
        elif self.warnings:
            print("\n⚠️  建议解决警告项目以获得更好的发布体验")
        else:
            print("\n🎉 项目已准备好发布到 GitHub!")
        
        return True


def main():
    """主函数"""
    preparator = GitHubReleasePreparator()
    success = preparator.run_checks()
    
    if success:
        print("\n🎯 下一步: 按照上面的检查清单和命令进行 GitHub 发布")
    else:
        print("\n🔧 请先修复错误，然后重新运行此脚本")
        sys.exit(1)


if __name__ == "__main__":
    main()