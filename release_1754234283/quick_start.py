#!/usr/bin/env python3
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
