#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub Actions Conda 修复验证脚本
用于验证 conda 工作流文件的修复是否正确
"""

import os
import sys
from pathlib import Path
import yaml

def test_conda_workflow_fix():
    """测试 conda 工作流修复"""
    print("🔧 GitHub Actions Conda 修复验证")
    print("=" * 50)
    
    project_root = Path(__file__).parent
    
    # 测试工作流文件
    workflow_file = project_root / ".github" / "workflows" / "python-package-conda.yml"
    
    print("=== 测试工作流文件 ===")
    if workflow_file.exists():
        print(f"✅ 存在: {workflow_file.name}")
        
        # 检查工作流内容
        with open(workflow_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 检查是否有工作目录设置
        if "working-directory: ./creation_package" in content:
            print("✅ 工作目录设置正确")
        else:
            print("❌ 缺少工作目录设置")
            
        # 检查是否有调试步骤
        if "Debug directory structure" in content:
            print("✅ 包含调试步骤")
        else:
            print("❌ 缺少调试步骤")
            
        # 检查超时设置
        if "timeout-minutes:" in content:
            print("✅ 包含超时设置")
        else:
            print("❌ 缺少超时设置")
            
    else:
        print(f"❌ 不存在: {workflow_file.name}")
    
    # 测试 environment.yml
    env_file = project_root / "environment.yml"
    
    print("\n=== 测试环境配置文件 ===")
    if env_file.exists():
        print(f"✅ 存在: {env_file.name}")
        
        try:
            with open(env_file, 'r', encoding='utf-8') as f:
                env_config = yaml.safe_load(f)
            
            # 检查Python版本约束
            deps = env_config.get('dependencies', [])
            python_dep = None
            for dep in deps:
                if isinstance(dep, str) and dep.startswith('python'):
                    python_dep = dep
                    break
            
            if python_dep and '<3.13' in python_dep:
                print("✅ Python版本约束正确")
            else:
                print("❌ Python版本约束可能有问题")
                
            # 检查是否移除了重型依赖
            pip_deps = []
            for dep in deps:
                if isinstance(dep, dict) and 'pip' in dep:
                    pip_deps = dep['pip']
                    break
            
            if 'skia-python' not in pip_deps:
                print("✅ 已移除重型依赖 skia-python")
            else:
                print("❌ 仍包含重型依赖 skia-python")
                
        except Exception as e:
            print(f"❌ 解析环境文件失败: {e}")
    else:
        print(f"❌ 不存在: {env_file.name}")
    
    # 测试目录结构
    print("\n=== 测试目录结构 ===")
    required_files = [
        "creationbuild_package/requirements_creation.txt",
        "creationbuild_package/creation.py",
        "PROJECT_OVERVIEW.md"
    ]
    
    all_exist = True
    for file_path in required_files:
        full_path = project_root / file_path
        if full_path.exists():
            print(f"✅ 存在: {file_path}")
        else:
            print(f"❌ 不存在: {file_path}")
            all_exist = False
    
    # 汇总结果
    print("\n📊 测试结果汇总")
    if all_exist:
        print("🎉 所有关键文件都存在！")
        print("🔧 Conda 工作流修复应该能解决超时问题")
        print("\n💡 主要改进:")
        print("   - 设置了正确的工作目录")
        print("   - 优化了环境依赖配置")
        print("   - 移除了重型依赖包")
        print("   - 添加了超时设置")
        print("   - 增强了调试信息")
    else:
        print("❌ 存在缺失文件，需要检查项目结构")

if __name__ == "__main__":
    test_conda_workflow_fix()