#!/usr/bin/env python3
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
