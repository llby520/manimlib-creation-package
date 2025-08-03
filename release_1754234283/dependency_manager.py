#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ManimLib Creation Package - 智能依赖管理器
版本: 1.0.0
作者: ManimLib Community

这个模块提供智能的依赖检查和安装功能，确保项目可以在不同环境下正常运行。
支持自动检测和安装 manimlib、manim 等依赖。
"""

import sys
import subprocess
import importlib
import warnings
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import json
import time

# 抑制警告
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

class DependencyManager:
    """智能依赖管理器"""
    
    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.installed_packages = {}
        self.failed_packages = []
        self.alternative_packages = {
            'manimlib': ['manim', 'manimce', 'manimgl'],
            'manim': ['manimlib', 'manimce', 'manimgl'],
        }
        
    def log(self, message: str, level: str = "INFO") -> None:
        """记录日志"""
        if self.verbose:
            timestamp = time.strftime("%H:%M:%S")
            prefix = f"[{timestamp}] [{level}]"
            print(f"{prefix} {message}")
    
    def check_package(self, package_name: str) -> Tuple[bool, Optional[str]]:
        """检查包是否已安装并返回版本信息"""
        try:
            module = importlib.import_module(package_name)
            version = getattr(module, '__version__', 'unknown')
            self.installed_packages[package_name] = version
            return True, version
        except ImportError:
            return False, None
    
    def install_package(self, package_name: str, pip_name: Optional[str] = None) -> bool:
        """安装Python包"""
        pip_name = pip_name or package_name
        self.log(f"正在安装 {pip_name}...")
        
        try:
            # 使用pip安装
            cmd = [sys.executable, "-m", "pip", "install", pip_name, "--upgrade"]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            # 验证安装
            installed, version = self.check_package(package_name)
            if installed:
                self.log(f"{pip_name} 安装成功 (版本: {version})", "SUCCESS")
                return True
            else:
                self.log(f"{pip_name} 安装后验证失败", "ERROR")
                return False
                
        except subprocess.CalledProcessError as e:
            self.log(f"{pip_name} 安装失败: {e.stderr}", "ERROR")
            self.failed_packages.append(pip_name)
            return False
        except Exception as e:
            self.log(f"{pip_name} 安装异常: {e}", "ERROR")
            self.failed_packages.append(pip_name)
            return False
    
    def find_alternative(self, package_name: str) -> Optional[str]:
        """寻找可用的替代包"""
        alternatives = self.alternative_packages.get(package_name, [])
        
        for alt in alternatives:
            installed, version = self.check_package(alt)
            if installed:
                self.log(f"找到替代包: {alt} (版本: {version})", "SUCCESS")
                return alt
        
        return None
    
    def install_with_alternatives(self, package_name: str) -> bool:
        """尝试安装包，如果失败则尝试替代包"""
        # 首先检查是否已安装
        installed, version = self.check_package(package_name)
        if installed:
            self.log(f"{package_name} 已安装 (版本: {version})", "SUCCESS")
            return True
        
        # 尝试安装主包
        if self.install_package(package_name):
            return True
        
        # 尝试替代包
        alternatives = self.alternative_packages.get(package_name, [])
        for alt in alternatives:
            self.log(f"尝试安装替代包: {alt}")
            if self.install_package(alt):
                return True
        
        return False
    
    def check_core_dependencies(self) -> Dict[str, bool]:
        """检查核心依赖"""
        core_deps = {
            'numpy': 'numpy>=1.20.0',
            'typing_extensions': 'typing-extensions>=4.0.0'
        }
        
        results = {}
        
        for package, pip_name in core_deps.items():
            installed, version = self.check_package(package)
            if not installed:
                self.log(f"缺少核心依赖: {package}")
                success = self.install_package(package, pip_name)
                results[package] = success
            else:
                self.log(f"核心依赖已安装: {package} (版本: {version})", "SUCCESS")
                results[package] = True
        
        return results
    
    def check_manim_dependencies(self) -> Dict[str, Any]:
        """检查Manim相关依赖"""
        manim_packages = ['manimlib', 'manim', 'manimce', 'manimgl']
        results = {
            'available': [],
            'installed': {},
            'recommended': None
        }
        
        for package in manim_packages:
            installed, version = self.check_package(package)
            if installed:
                results['available'].append(package)
                results['installed'][package] = version
                self.log(f"发现 {package} (版本: {version})", "SUCCESS")
        
        # 如果没有找到任何Manim包，尝试安装
        if not results['available']:
            self.log("未找到任何Manim包，尝试自动安装...")
            
            # 按优先级尝试安装
            priority_order = ['manim', 'manimce', 'manimlib', 'manimgl']
            
            for package in priority_order:
                self.log(f"尝试安装 {package}...")
                if self.install_package(package):
                    results['available'].append(package)
                    installed, version = self.check_package(package)
                    results['installed'][package] = version
                    results['recommended'] = package
                    break
        else:
            # 推荐使用优先级最高的可用包
            priority_map = {'manimlib': 4, 'manim': 3, 'manimce': 2, 'manimgl': 1}
            best_package = max(results['available'], 
                             key=lambda x: priority_map.get(x, 0))
            results['recommended'] = best_package
        
        return results
    
    def generate_import_helper(self, manim_results: Dict[str, Any]) -> str:
        """生成导入辅助代码"""
        if not manim_results['available']:
            return ""
        
        recommended = manim_results['recommended']
        available = manim_results['available']
        
        helper_code = f'''# -*- coding: utf-8 -*-
"""
ManimLib Creation Package - 自动导入辅助
自动生成于: {time.strftime("%Y-%m-%d %H:%M:%S")}

检测到的Manim包: {', '.join(available)}
推荐使用: {recommended}
"""

import warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

# 尝试导入可用的Manim包
MANIM_PACKAGE = None
MANIM_VERSION = None

# 按优先级尝试导入
package_priority = {available}
try_order = ['manimlib', 'manim', 'manimce', 'manimgl']

for package_name in try_order:
    if package_name in package_priority:
        try:
            if package_name == 'manimlib':
                import manimlib
                from manimlib import *
                MANIM_PACKAGE = 'manimlib'
                MANIM_VERSION = getattr(manimlib, '__version__', 'unknown')
                print(f"✅ 使用 manimlib (版本: {{MANIM_VERSION}})")
                break
            elif package_name == 'manim':
                import manim
                from manim import *
                MANIM_PACKAGE = 'manim'
                MANIM_VERSION = getattr(manim, '__version__', 'unknown')
                print(f"✅ 使用 manim (版本: {{MANIM_VERSION}})")
                break
            elif package_name == 'manimce':
                import manimce
                from manimce import *
                MANIM_PACKAGE = 'manimce'
                MANIM_VERSION = getattr(manimce, '__version__', 'unknown')
                print(f"✅ 使用 manimce (版本: {{MANIM_VERSION}})")
                break
            elif package_name == 'manimgl':
                import manimgl
                from manimgl import *
                MANIM_PACKAGE = 'manimgl'
                MANIM_VERSION = getattr(manimgl, '__version__', 'unknown')
                print(f"✅ 使用 manimgl (版本: {{MANIM_VERSION}})")
                break
        except ImportError:
            continue

if MANIM_PACKAGE is None:
    raise ImportError(
        "未找到可用的Manim包。请安装以下包之一:\n"
        "- pip install manim\n"
        "- pip install manimce\n"
        "- pip install manimgl\n"
        "- 或从源码安装 manimlib"
    )

# 导入creation模块
try:
    import creation
    print("✅ creation 模块导入成功")
except ImportError as e:
    print(f"❌ creation 模块导入失败: {{e}}")
    print("请确保 creation.py 文件在当前目录或Python路径中")

def get_manim_info():
    """获取当前使用的Manim包信息"""
    return {{
        'package': MANIM_PACKAGE,
        'version': MANIM_VERSION,
        'available_packages': {available}
    }}

if __name__ == "__main__":
    info = get_manim_info()
    print(f"\n当前Manim环境信息:")
    print(f"包名: {{info['package']}}")
    print(f"版本: {{info['version']}}")
    print(f"可用包: {{', '.join(info['available_packages'])}}")
'''
        
        return helper_code
    
    def create_config_file(self, manim_results: Dict[str, Any]) -> bool:
        """创建配置文件"""
        config = {
            'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
            'python_version': f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            'installed_packages': self.installed_packages,
            'failed_packages': self.failed_packages,
            'manim_packages': manim_results,
            'recommended_import': manim_results.get('recommended', 'manim')
        }
        
        try:
            config_path = Path('dependency_config.json')
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            self.log(f"配置文件已保存: {config_path}", "SUCCESS")
            return True
        except Exception as e:
            self.log(f"保存配置文件失败: {e}", "ERROR")
            return False
    
    def run_full_check(self) -> bool:
        """运行完整的依赖检查和安装"""
        self.log("开始完整依赖检查...", "INFO")
        
        # 检查Python版本
        if sys.version_info < (3, 8):
            self.log(f"Python版本过低: {sys.version_info.major}.{sys.version_info.minor}", "ERROR")
            self.log("需要Python 3.8或更高版本", "ERROR")
            return False
        
        self.log(f"Python版本: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}", "SUCCESS")
        
        # 检查核心依赖
        core_results = self.check_core_dependencies()
        if not all(core_results.values()):
            self.log("核心依赖安装失败", "ERROR")
            return False
        
        # 检查Manim依赖
        manim_results = self.check_manim_dependencies()
        
        # 生成导入辅助文件
        if manim_results['available']:
            helper_code = self.generate_import_helper(manim_results)
            try:
                helper_path = Path('manim_import_helper.py')
                with open(helper_path, 'w', encoding='utf-8') as f:
                    f.write(helper_code)
                self.log(f"导入辅助文件已生成: {helper_path}", "SUCCESS")
            except Exception as e:
                self.log(f"生成导入辅助文件失败: {e}", "ERROR")
        
        # 保存配置
        self.create_config_file(manim_results)
        
        # 总结
        success = len(manim_results['available']) > 0
        if success:
            self.log("依赖检查完成，环境准备就绪", "SUCCESS")
            if manim_results['recommended']:
                self.log(f"推荐使用: {manim_results['recommended']}", "INFO")
        else:
            self.log("依赖检查完成，但未找到可用的Manim包", "ERROR")
        
        return success

def main():
    """主函数"""
    print("ManimLib Creation Package - 智能依赖管理器")
    print("=" * 50)
    
    manager = DependencyManager(verbose=True)
    success = manager.run_full_check()
    
    if success:
        print("\n✅ 依赖管理完成！")
        print("\n下一步:")
        print("1. 使用 'import manim_import_helper' 来自动导入Manim")
        print("2. 查看 dependency_config.json 了解环境详情")
        print("3. 运行示例脚本测试环境")
    else:
        print("\n❌ 依赖管理未完全成功")
        print("请检查错误信息并手动安装缺失的包")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())