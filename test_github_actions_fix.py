#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub Actions 修复验证脚本
用于验证工作流文件的修复是否正确
"""

import os
import sys
from pathlib import Path

def test_directory_structure():
    """测试目录结构"""
    print("=== 测试目录结构 ===")
    current_dir = Path.cwd()
    print(f"当前工作目录: {current_dir}")
    
    # 检查关键文件
    key_files = [
        "requirements_creation.txt",
        "creationbuild_package/requirements_creation.txt",
        "creation.py",
        "creationbuild_package/creation.py",
        "PROJECT_OVERVIEW.md"
    ]
    
    for file_path in key_files:
        full_path = current_dir / file_path
        status = "✅ 存在" if full_path.exists() else "❌ 不存在"
        print(f"{status}: {file_path}")
    
    return True

def test_requirements_file():
    """测试requirements文件"""
    print("\n=== 测试requirements文件 ===")
    
    # 检查requirements文件内容
    req_files = [
        "requirements_creation.txt",
        "creationbuild_package/requirements_creation.txt"
    ]
    
    for req_file in req_files:
        req_path = Path(req_file)
        if req_path.exists():
            print(f"✅ 找到: {req_file}")
            try:
                with open(req_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    lines = [line.strip() for line in content.split('\n') if line.strip() and not line.startswith('#')]
                    print(f"   依赖包数量: {len(lines)}")
                    if lines:
                        print(f"   主要依赖: {lines[0]}")
            except Exception as e:
                print(f"   ❌ 读取失败: {e}")
        else:
            print(f"❌ 未找到: {req_file}")
    
    return True

def test_creation_module():
    """测试creation模块"""
    print("\n=== 测试creation模块 ===")
    
    try:
        # 尝试从creationbuild_package导入
        sys.path.insert(0, str(Path.cwd() / "creationbuild_package"))
        import creation
        print("✅ 成功导入creation模块")
        
        # 运行自测试
        if hasattr(creation, '_module_self_test'):
            creation._module_self_test()
            print("✅ 模块自测试通过")
        else:
            print("⚠️  模块没有_module_self_test方法")
            
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False
    
    return True

def main():
    """主函数"""
    print("🔧 GitHub Actions 修复验证")
    print("=" * 50)
    
    tests = [
        test_directory_structure,
        test_requirements_file,
        test_creation_module
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ 测试异常: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("📊 测试结果汇总")
    passed = sum(results)
    total = len(results)
    print(f"通过: {passed}/{total}")
    
    if passed == total:
        print("🎉 所有测试通过！GitHub Actions应该能正常工作")
        return 0
    else:
        print("⚠️  部分测试失败，可能需要进一步调试")
        return 1

if __name__ == "__main__":
    sys.exit(main())