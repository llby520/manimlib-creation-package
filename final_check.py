#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ManimLib Creation Package - 最终完整性检查

这个脚本验证整个项目的完整性，确保所有文件和功能都已就绪，
可以安全地发布到 GitHub。
"""

import sys
import os
import zipfile
from pathlib import Path
from typing import List, Tuple, Dict
import subprocess
import json

class ProjectIntegrityChecker:
    """
    项目完整性检查器
    
    检查项目的所有组件是否完整并正常工作
    """
    
    def __init__(self, project_root: str = None):
        self.project_root = Path(project_root or os.getcwd())
        self.errors = []
        self.warnings = []
        self.success_count = 0
        self.total_checks = 0
    
    def log_success(self, message: str) -> None:
        """记录成功信息"""
        print(f"✅ {message}")
        self.success_count += 1
    
    def log_warning(self, message: str) -> None:
        """记录警告信息"""
        print(f"⚠️ {message}")
        self.warnings.append(message)
    
    def log_error(self, message: str) -> None:
        """记录错误信息"""
        print(f"❌ {message}")
        self.errors.append(message)
    
    def check_required_files(self) -> None:
        """检查必需文件"""
        print("\n📁 检查必需文件...")
        
        required_files = [
            "creation.py",
            "README.md",
            "LICENSE",
            "pyproject.toml",
            "requirements_creation.txt",
            "setup_creation.py",
            "auto_setup.py",
            "dependency_manager.py",
            "STARTUP_GUIDE.md",
            "GITHUB_RELEASE_NOTES.md"
        ]
        
        for file_name in required_files:
            self.total_checks += 1
            file_path = self.project_root / file_name
            if file_path.exists():
                self.log_success(f"找到文件: {file_name}")
            else:
                self.log_error(f"缺少文件: {file_name}")
    
    def check_directories(self) -> None:
        """检查必需目录"""
        print("\n📂 检查必需目录...")
        
        required_dirs = [
            "creationbuild_package",
            "examples",
            "release",
            ".github"
        ]
        
        for dir_name in required_dirs:
            self.total_checks += 1
            dir_path = self.project_root / dir_name
            if dir_path.exists() and dir_path.is_dir():
                self.log_success(f"找到目录: {dir_name}")
            else:
                self.log_error(f"缺少目录: {dir_name}")
    
    def check_creation_module(self) -> None:
        """检查 creation 模块"""
        print("\n🧪 检查 creation 模块...")
        
        try:
            # 添加当前目录到 Python 路径
            sys.path.insert(0, str(self.project_root))
            
            import creation
            self.total_checks += 1
            self.log_success("成功导入 creation 模块")
            
            # 检查版本
            self.total_checks += 1
            if hasattr(creation, '__version__'):
                self.log_success(f"模块版本: {creation.__version__}")
            else:
                self.log_warning("模块缺少版本信息")
            
            # 检查主要类
            required_classes = [
                'ShowCreation', 'Write', 'DrawBorderThenFill',
                'Uncreate', 'ShowSubmobjectsOneByOne', 'ShowPartial'
            ]
            
            for class_name in required_classes:
                self.total_checks += 1
                if hasattr(creation, class_name):
                    self.log_success(f"找到类: {class_name}")
                else:
                    self.log_error(f"缺少类: {class_name}")
            
            # 运行自测试
            self.total_checks += 1
            if hasattr(creation, '_module_self_test'):
                try:
                    creation._module_self_test()
                    self.log_success("模块自测试通过")
                except Exception as e:
                    self.log_error(f"模块自测试失败: {e}")
            else:
                self.log_warning("模块缺少自测试功能")
                
        except ImportError as e:
            self.total_checks += 1
            self.log_error(f"无法导入 creation 模块: {e}")
        except Exception as e:
            self.total_checks += 1
            self.log_error(f"检查 creation 模块时出错: {e}")
    
    def check_scripts(self) -> None:
        """检查脚本文件"""
        print("\n🔧 检查脚本文件...")
        
        scripts = [
            "auto_setup.py",
            "dependency_manager.py",
            "prepare_github_release.py"
        ]
        
        for script_name in scripts:
            self.total_checks += 1
            script_path = self.project_root / script_name
            
            if not script_path.exists():
                self.log_error(f"脚本不存在: {script_name}")
                continue
            
            # 检查语法
            try:
                with open(script_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                compile(content, script_path, 'exec')
                self.log_success(f"脚本语法正确: {script_name}")
            except SyntaxError as e:
                self.log_error(f"脚本语法错误 {script_name}: {e}")
            except Exception as e:
                self.log_warning(f"检查脚本 {script_name} 时出错: {e}")
    
    def check_release_package(self) -> None:
        """检查发布包"""
        print("\n📦 检查发布包...")
        
        # 查找最新的发布目录
        release_dirs = [d for d in self.project_root.iterdir() if d.is_dir() and d.name.startswith('release')]
        if release_dirs:
            release_dir = max(release_dirs, key=lambda x: x.stat().st_mtime)
        else:
            release_dir = self.project_root / "release"
        self.total_checks += 1
        
        if not release_dir.exists():
            self.log_error("发布目录不存在")
            return
        
        self.log_success("发布目录存在")
        
        # 检查发布包中的必需文件
        required_in_release = [
            "creation.py",
            "auto_setup.py",
            "quick_start.py",
            "test_installation.py",
            "README.md",
            "STARTUP_GUIDE.md"
        ]
        
        for file_name in required_in_release:
            self.total_checks += 1
            file_path = release_dir / file_name
            if file_path.exists():
                self.log_success(f"发布包包含: {file_name}")
            else:
                self.log_error(f"发布包缺少: {file_name}")
        
        # 检查 ZIP 文件
        zip_files = list(self.project_root.glob("manimlib-creation-release-*.zip"))
        self.total_checks += 1
        
        if zip_files:
            latest_zip = max(zip_files, key=lambda x: x.stat().st_mtime)
            self.log_success(f"找到发布 ZIP: {latest_zip.name}")
            
            # 检查 ZIP 内容
            try:
                with zipfile.ZipFile(latest_zip, 'r') as zf:
                    zip_contents = zf.namelist()
                    if 'creation.py' in zip_contents:
                        self.log_success("ZIP 包含核心文件")
                    else:
                        self.log_error("ZIP 缺少核心文件")
            except Exception as e:
                self.log_error(f"检查 ZIP 文件时出错: {e}")
        else:
            self.log_warning("未找到发布 ZIP 文件")
    
    def check_conda_build(self) -> None:
        """检查 Conda 构建配置"""
        print("\n🐍 检查 Conda 构建配置...")
        
        conda_dir = self.project_root / "creationbuild_package"
        self.total_checks += 1
        
        if not conda_dir.exists():
            self.log_error("Conda 构建目录不存在")
            return
        
        self.log_success("Conda 构建目录存在")
        
        # 检查 Conda 文件
        conda_files = ["meta.yaml", "environment.yml"]
        
        for file_name in conda_files:
            self.total_checks += 1
            file_path = conda_dir / file_name
            if file_path.exists():
                self.log_success(f"Conda 文件存在: {file_name}")
            else:
                self.log_error(f"Conda 文件缺少: {file_name}")
    
    def check_examples(self) -> None:
        """检查示例代码"""
        print("\n📚 检查示例代码...")
        
        examples_dir = self.project_root / "examples"
        self.total_checks += 1
        
        if not examples_dir.exists():
            self.log_error("示例目录不存在")
            return
        
        self.log_success("示例目录存在")
        
        # 检查示例文件
        example_files = list(examples_dir.glob("*.py"))
        self.total_checks += 1
        
        if example_files:
            self.log_success(f"找到 {len(example_files)} 个示例文件")
            
            # 检查示例语法
            for example_file in example_files:
                self.total_checks += 1
                try:
                    with open(example_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    compile(content, example_file, 'exec')
                    self.log_success(f"示例语法正确: {example_file.name}")
                except SyntaxError as e:
                    self.log_error(f"示例语法错误 {example_file.name}: {e}")
                except Exception as e:
                    self.log_warning(f"检查示例 {example_file.name} 时出错: {e}")
        else:
            self.log_warning("未找到示例文件")
    
    def check_github_integration(self) -> None:
        """检查 GitHub 集成"""
        print("\n🐙 检查 GitHub 集成...")
        
        github_dir = self.project_root / ".github"
        self.total_checks += 1
        
        if github_dir.exists():
            self.log_success("GitHub 目录存在")
            
            # 检查工作流
            workflows_dir = github_dir / "workflows"
            self.total_checks += 1
            
            if workflows_dir.exists():
                workflow_files = list(workflows_dir.glob("*.yml"))
                if workflow_files:
                    self.log_success(f"找到 {len(workflow_files)} 个工作流")
                else:
                    self.log_warning("未找到工作流文件")
            else:
                self.log_warning("工作流目录不存在")
        else:
            self.log_warning("GitHub 目录不存在")
        
        # 检查 .gitignore
        gitignore_path = self.project_root / ".gitignore"
        self.total_checks += 1
        
        if gitignore_path.exists():
            self.log_success(".gitignore 文件存在")
        else:
            self.log_warning(".gitignore 文件不存在")
    
    def test_installation_scripts(self) -> None:
        """测试安装脚本"""
        print("\n🧪 测试安装脚本...")
        
        # 查找最新的发布目录
        release_dirs = [d for d in self.project_root.iterdir() if d.is_dir() and d.name.startswith('release')]
        if release_dirs:
            release_dir = max(release_dirs, key=lambda x: x.stat().st_mtime)
        else:
            release_dir = self.project_root / "release"
        
        if not release_dir.exists():
            self.log_error("发布目录不存在，跳过脚本测试")
            return
        
        # 测试快速开始脚本
        quick_start_path = release_dir / "quick_start.py"
        self.total_checks += 1
        
        if quick_start_path.exists():
            try:
                # 检查语法
                with open(quick_start_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                compile(content, quick_start_path, 'exec')
                self.log_success("快速开始脚本语法正确")
            except Exception as e:
                self.log_error(f"快速开始脚本有问题: {e}")
        else:
            self.log_error("快速开始脚本不存在")
        
        # 测试安装验证脚本
        test_script_path = release_dir / "test_installation.py"
        self.total_checks += 1
        
        if test_script_path.exists():
            try:
                # 检查语法
                with open(test_script_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                compile(content, test_script_path, 'exec')
                self.log_success("安装验证脚本语法正确")
            except Exception as e:
                self.log_error(f"安装验证脚本有问题: {e}")
        else:
            self.log_error("安装验证脚本不存在")
    
    def generate_report(self) -> Dict:
        """生成检查报告"""
        total_issues = len(self.errors) + len(self.warnings)
        success_rate = (self.success_count / self.total_checks * 100) if self.total_checks > 0 else 0
        
        report = {
            "total_checks": self.total_checks,
            "success_count": self.success_count,
            "warning_count": len(self.warnings),
            "error_count": len(self.errors),
            "success_rate": round(success_rate, 2),
            "errors": self.errors,
            "warnings": self.warnings,
            "ready_for_release": len(self.errors) == 0
        }
        
        return report
    
    def run_all_checks(self) -> Dict:
        """运行所有检查"""
        print("🔍 ManimLib Creation Package - 完整性检查")
        print("=" * 60)
        
        # 运行各项检查
        self.check_required_files()
        self.check_directories()
        self.check_creation_module()
        self.check_scripts()
        self.check_release_package()
        self.check_conda_build()
        self.check_examples()
        self.check_github_integration()
        self.test_installation_scripts()
        
        # 生成报告
        report = self.generate_report()
        
        # 显示总结
        print("\n" + "=" * 60)
        print("📊 检查总结")
        print("=" * 60)
        print(f"总检查项: {report['total_checks']}")
        print(f"成功: {report['success_count']} ✅")
        print(f"警告: {report['warning_count']} ⚠️")
        print(f"错误: {report['error_count']} ❌")
        print(f"成功率: {report['success_rate']}%")
        
        if report['ready_for_release']:
            print("\n🎉 项目已准备好发布到 GitHub！")
        else:
            print("\n⚠️ 请先解决以下错误再发布:")
            for error in self.errors:
                print(f"  ❌ {error}")
        
        if self.warnings:
            print("\n⚠️ 警告项目:")
            for warning in self.warnings:
                print(f"  ⚠️ {warning}")
        
        return report

def main():
    """主函数"""
    print("🚀 启动项目完整性检查...")
    
    # 检查当前目录
    current_dir = Path.cwd()
    creation_file = current_dir / "creation.py"
    
    if not creation_file.exists():
        print("❌ 当前目录不是项目根目录")
        print("请在包含 creation.py 的目录中运行此脚本")
        return 1
    
    # 运行检查
    checker = ProjectIntegrityChecker(current_dir)
    report = checker.run_all_checks()
    
    # 保存报告
    report_file = current_dir / "integrity_check_report.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 详细报告已保存到: {report_file}")
    
    # 返回状态码
    return 0 if report['ready_for_release'] else 1

if __name__ == "__main__":
    sys.exit(main())