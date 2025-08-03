#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub Release Preparation Script
ManimLib Creation Package - Enhanced Version

This script prepares the project for GitHub release by:
1. Checking all required files
2. Validating configurations
3. Running tests
4. Creating release artifacts
5. Providing release guidance
6. Auto-installing dependencies
7. Creating complete startup environment
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import shutil
import zipfile
from datetime import datetime
import importlib.util


class GitHubReleasePreparator:
    """GitHub 发布准备器 - 增强版"""
    
    def __init__(self, project_root: str = None):
        self.project_root = Path(project_root or os.getcwd())
        self.package_dir = self.project_root / "creationbuild_package"
        self.errors = []
        self.warnings = []
        self.success_items = []
        self.dependency_manager = None
        
    def log_error(self, message: str):
        """记录错误"""
        self.errors.append(message)
        print(f"❌ 错误: {message}")
        
    def log_warning(self, message: str):
        """记录警告"""
        self.warnings.append(message)
        print(f"⚠️  警告: {message}")
        
    def log_success(self, message: str):
        """记录成功"""
        self.success_items.append(message)
        print(f"✅ {message}")
    
    def initialize_dependency_manager(self) -> bool:
        """初始化依赖管理器"""
        try:
            # 尝试导入依赖管理器
            spec = importlib.util.spec_from_file_location(
                "dependency_manager", 
                self.project_root / "dependency_manager.py"
            )
            if spec and spec.loader:
                dm_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(dm_module)
                self.dependency_manager = dm_module.DependencyManager(verbose=False)
                self.log_success("依赖管理器初始化成功")
                return True
        except Exception as e:
            self.log_warning(f"依赖管理器初始化失败: {e}")
        return False
    
    def check_and_install_dependencies(self) -> None:
        """检查并安装依赖"""
        print("\n🔍 检查项目依赖...")
        
        if not self.initialize_dependency_manager():
            self.log_warning("无法初始化依赖管理器，跳过依赖检查")
            return
        
        try:
            # 检查核心依赖
            core_deps = ['manim', 'numpy', 'matplotlib', 'pillow']
            missing_deps = []
            
            for dep in core_deps:
                try:
                    __import__(dep)
                    self.log_success(f"依赖 {dep} 已安装")
                except ImportError:
                    missing_deps.append(dep)
                    self.log_warning(f"缺少依赖: {dep}")
            
            # 自动安装缺失的依赖
            if missing_deps and self.dependency_manager:
                print(f"\n🔧 尝试自动安装缺失的依赖: {missing_deps}")
                for dep in missing_deps:
                    if self.dependency_manager.install_package(dep):
                        self.log_success(f"成功安装依赖: {dep}")
                    else:
                        self.log_error(f"安装依赖失败: {dep}")
            
        except Exception as e:
            self.log_error(f"依赖检查过程出错: {e}")
    
    def check_python_environment(self) -> None:
        """检查 Python 环境"""
        print("\n🔍 检查 Python 环境...")
        
        # 检查 Python 版本
        python_version = sys.version_info
        if python_version >= (3, 8):
            self.log_success(f"Python 版本: {python_version.major}.{python_version.minor}.{python_version.micro}")
        else:
            self.log_error(f"Python 版本过低: {python_version.major}.{python_version.minor}，需要 3.8+")
        
        # 检查虚拟环境
        if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
            self.log_success("运行在虚拟环境中")
        else:
            self.log_warning("未使用虚拟环境，建议使用虚拟环境")
        
        # 检查包管理工具
        try:
            import pip
            self.log_success(f"pip 版本: {pip.__version__}")
        except ImportError:
            self.log_error("pip 未安装")
        
        # 检查构建工具
        try:
            import build
            self.log_success("build 工具已安装")
        except ImportError:
            self.log_warning("build 工具未安装，运行: pip install build")
    
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
            "git remote add origin https://github.com/llby520/manimlib-creation-package.git",
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
    
    def create_release_package(self) -> None:
        """创建完整发布包"""
        print("\n📦 创建完整发布包...")
        
        # 创建发布目录
        import time
        timestamp = int(time.time())
        release_dir = self.project_root / f"release_{timestamp}"
        
        # 确保目录不存在冲突
        counter = 0
        while release_dir.exists():
            counter += 1
            release_dir = self.project_root / f"release_{timestamp}_{counter}"
        
        release_dir.mkdir(exist_ok=True)
        print(f"✅ 创建发布目录: {release_dir.name}")
        
        # 复制核心文件
        core_files = [
            "creation.py",
            "README.md",
            "LICENSE",
            "pyproject.toml",
            "requirements_creation.txt",
            "setup_creation.py",
            "auto_setup.py",
            "dependency_manager.py",
            "STARTUP_GUIDE.md"
        ]
        
        for file_name in core_files:
            src_file = self.project_root / file_name
            if src_file.exists():
                shutil.copy2(src_file, release_dir / file_name)
                self.log_success(f"复制文件: {file_name}")
            else:
                self.log_warning(f"文件不存在: {file_name}")
        
        # 复制构建包目录
        build_dir = self.project_root / "creationbuild_package"
        if build_dir.exists():
            shutil.copytree(build_dir, release_dir / "creationbuild_package")
            self.log_success("复制构建包目录")
        
        # 复制GitHub工作流
        github_dir = self.project_root / ".github"
        if github_dir.exists():
            shutil.copytree(github_dir, release_dir / ".github")
            self.log_success("复制GitHub工作流")
        
        # 创建示例目录
        examples_dir = release_dir / "examples"
        examples_dir.mkdir(exist_ok=True)
        
        # 创建快速开始脚本
        self.create_quick_start_script(release_dir)
        
        # 创建安装验证脚本
        self.create_installation_test(release_dir)
        
        # 创建压缩包
        zip_path = self.project_root / f"manimlib-creation-release-{datetime.now().strftime('%Y%m%d')}.zip"
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in release_dir.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(release_dir)
                    zipf.write(file_path, arcname)
        
        self.log_success(f"创建发布包: {zip_path.name}")
    
    def create_quick_start_script(self, release_dir: Path) -> None:
        """创建快速开始脚本"""
        quick_start_content = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ManimLib Creation Package - 快速开始脚本

这个脚本帮助您快速开始使用 ManimLib Creation Package。
它会自动检查环境、安装依赖并运行示例。
"""

import sys
import subprocess
from pathlib import Path

def main():
    print("🚀 ManimLib Creation Package - 快速开始")
    print("=" * 50)
    
    # 检查Python版本
    if sys.version_info < (3, 8):
        print("❌ Python版本过低，需要3.8+")
        return 1
    
    print(f"✅ Python版本: {sys.version_info.major}.{sys.version_info.minor}")
    
    # 运行自动设置
    print("\n🔧 运行自动设置...")
    try:
        result = subprocess.run([sys.executable, "auto_setup.py"], check=True)
        print("✅ 自动设置完成")
    except subprocess.CalledProcessError:
        print("⚠️ 自动设置遇到问题，但可以继续")
    
    # 测试导入
    print("\n🧪 测试模块导入...")
    try:
        import creation
        print("✅ creation 模块导入成功")
        
        # 运行自测试
        if hasattr(creation, '_module_self_test'):
            creation._module_self_test()
            print("✅ 模块自测试通过")
    except Exception as e:
        print(f"❌ 模块测试失败: {e}")
        return 1
    
    print("\n🎉 快速开始完成！")
    print("\n下一步:")
    print("1. 查看 STARTUP_GUIDE.md 了解详细使用方法")
    print("2. 运行 examples/ 目录下的示例")
    print("3. 开始创建您的动画！")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
'''
        
        quick_start_path = release_dir / "quick_start.py"
        with open(quick_start_path, "w", encoding="utf-8") as f:
            f.write(quick_start_content)
        self.log_success("创建快速开始脚本")
    
    def create_installation_test(self, release_dir: Path) -> None:
        """创建安装验证脚本"""
        test_content = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ManimLib Creation Package - 安装验证脚本

这个脚本验证包是否正确安装并可以正常使用。
"""

import sys
import traceback
from typing import List, Tuple

def test_basic_imports() -> Tuple[bool, str]:
    """测试基本导入"""
    try:
        import numpy
        import creation
        return True, "基本导入测试通过"
    except Exception as e:
        return False, f"基本导入失败: {e}"

def test_manim_availability() -> Tuple[bool, str]:
    """测试Manim可用性"""
    manim_packages = ['manimlib', 'manim', 'manimce', 'manimgl']
    available = []
    
    for package in manim_packages:
        try:
            __import__(package)
            available.append(package)
        except ImportError:
            continue
    
    if available:
        return True, f"找到Manim包: {', '.join(available)}"
    else:
        return False, "未找到任何Manim包"

def test_creation_functions() -> Tuple[bool, str]:
    """测试creation模块功能"""
    try:
        import creation
        
        # 检查主要类是否存在
        required_classes = [
            'ShowCreation', 'Write', 'DrawBorderThenFill',
            'Uncreate', 'ShowSubmobjectsOneByOne'
        ]
        
        missing = []
        for cls_name in required_classes:
            if not hasattr(creation, cls_name):
                missing.append(cls_name)
        
        if missing:
            return False, f"缺少类: {', '.join(missing)}"
        
        # 运行自测试
        if hasattr(creation, '_module_self_test'):
            creation._module_self_test()
        
        return True, "creation模块功能测试通过"
    except Exception as e:
        return False, f"creation模块测试失败: {e}"

def run_all_tests() -> None:
    """运行所有测试"""
    print("🧪 ManimLib Creation Package - 安装验证")
    print("=" * 50)
    
    tests = [
        ("基本导入测试", test_basic_imports),
        ("Manim可用性测试", test_manim_availability),
        ("Creation功能测试", test_creation_functions)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 {test_name}...")
        try:
            success, message = test_func()
            if success:
                print(f"✅ {message}")
                passed += 1
            else:
                print(f"❌ {message}")
        except Exception as e:
            print(f"❌ 测试异常: {e}")
            traceback.print_exc()
    
    print(f"\n📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！安装成功！")
        return 0
    else:
        print("⚠️ 部分测试失败，请检查安装")
        return 1

if __name__ == "__main__":
    sys.exit(run_all_tests())
'''
        
        test_path = release_dir / "test_installation.py"
        with open(test_path, "w", encoding="utf-8") as f:
            f.write(test_content)
        self.log_success("创建安装验证脚本")
    
    def run_checks(self) -> None:
        """运行所有检查"""
        print("🎯 Manimlib Creation Package - GitHub 发布准备 (增强版)")
        print("="*60)
        
        self.check_python_environment()
        self.check_and_install_dependencies()
        self.check_directory_structure()
        self.check_pyproject_toml()
        self.check_git_status()
        self.check_package_build()
        self.create_release_package()
        
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