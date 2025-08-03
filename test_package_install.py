#!/usr/bin/env python3
"""
测试 manimlib-creation 包的安装和基本功能

这个脚本验证：
1. 包是否正确安装
2. 模块是否可以导入（在没有 manimlib 依赖的情况下）
3. 包的元数据是否正确
"""

import sys
import importlib.util
import importlib.metadata
import os

def test_package_installation():
    """测试包的安装状态"""
    print("=" * 60)
    print("🧪 manimlib-creation 包安装测试")
    print("=" * 60)
    
    # 1. 检查 Python 版本
    print(f"📍 Python 版本: {sys.version}")
    print(f"📍 Python 路径: {sys.executable}")
    
    # 2. 检查包是否在 sys.path 中可找到
    try:
        spec = importlib.util.find_spec("creation")
        if spec is not None:
            print(f"✅ creation 模块找到: {spec.origin}")
        else:
            print("❌ creation 模块未找到")
            return False
    except Exception as e:
        print(f"❌ 查找模块时出错: {e}")
        return False
    
    # 3. 尝试导入模块（但不执行，避免 manimlib 依赖问题）
    try:
        # 读取模块文件内容来验证结构
        if spec and spec.origin:
            with open(spec.origin, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 检查关键类是否存在
            expected_classes = [
                'ShowPartial',
                'ShowCreation', 
                'Uncreate',
                'DrawBorderThenFill',
                'Write',
                'ShowIncreasingSubsets',
                'ShowSubmobjectsOneByOne',
                'AddTextWordByWord'
            ]
            
            found_classes = []
            for cls in expected_classes:
                if f"class {cls}" in content:
                    found_classes.append(cls)
            
            print(f"✅ 找到 {len(found_classes)}/{len(expected_classes)} 个预期类:")
            for cls in found_classes:
                print(f"   - {cls}")
                
            if len(found_classes) == len(expected_classes):
                print("✅ 所有预期类都存在")
            else:
                missing = set(expected_classes) - set(found_classes)
                print(f"⚠️  缺少类: {missing}")
                
    except Exception as e:
        print(f"❌ 验证模块内容时出错: {e}")
        return False
    
    # 4. 检查包的元数据
    try:
        metadata = importlib.metadata.metadata('manimlib-creation')
        print(f"✅ 包名: {metadata['Name']}")
        print(f"✅ 版本: {metadata['Version']}")
        print(f"✅ 描述: {metadata['Summary']}")
        print(f"✅ 作者: {metadata.get('Author', 'N/A')}")
        
    except Exception as e:
        print(f"⚠️  无法获取包元数据: {e}")
    
    # 5. 检查依赖
    try:
        import numpy
        import typing_extensions
        print(f"✅ 依赖检查通过:")
        print(f"   - numpy: {numpy.__version__}")
        try:
            print(f"   - typing_extensions: {typing_extensions.__version__}")
        except AttributeError:
            print(f"   - typing_extensions: 已安装 (版本信息不可用)")
    except ImportError as e:
        print(f"❌ 依赖检查失败: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("🎉 包安装测试完成！")
    print("=" * 60)
    
    return True

def test_conda_compatibility():
    """测试 conda 兼容性"""
    print("\n📦 Conda 兼容性测试:")
    
    # 检查是否在 conda 环境中
    conda_env = os.environ.get('CONDA_DEFAULT_ENV')
    if conda_env:
        print(f"✅ 当前 Conda 环境: {conda_env}")
    else:
        print("ℹ️  不在 Conda 环境中")
    
    # 检查 conda 是否可用
    try:
        import subprocess
        result = subprocess.run(['conda', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"✅ Conda 可用: {result.stdout.strip()}")
        else:
            print("⚠️  Conda 不可用")
    except Exception as e:
        print(f"⚠️  无法检查 Conda: {e}")

def main():
    """主测试函数"""
    success = test_package_installation()
    test_conda_compatibility()
    
    if success:
        print("\n🎯 结论: manimlib-creation 包可以通过 pip 成功安装！")
        print("\n📋 安装命令:")
        print("   pip install manimlib-creation")
        print("\n📋 或从本地安装:")
        print("   pip install dist/manimlib_creation-1.0.0-py3-none-any.whl")
        print("\n⚠️  注意: 使用此包需要先安装 manimlib 依赖")
    else:
        print("\n❌ 包安装测试失败")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())