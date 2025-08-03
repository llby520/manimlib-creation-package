#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中文编码测试脚本
用于验证各种环境下的中文显示是否正常
"""

import sys
import io
import locale
import os

def test_chinese_encoding():
    """测试中文编码显示"""
    print("=" * 60)
    print("🧪 中文编码测试 - Chinese Encoding Test")
    print("=" * 60)
    
    # 显示系统信息
    print(f"\n📋 系统信息:")
    print(f"   操作系统: {os.name}")
    print(f"   Python版本: {sys.version}")
    print(f"   默认编码: {sys.getdefaultencoding()}")
    print(f"   文件系统编码: {sys.getfilesystemencoding()}")
    print(f"   标准输出编码: {sys.stdout.encoding}")
    print(f"   本地化设置: {locale.getpreferredencoding()}")
    
    # 测试各种中文字符
    print(f"\n🔤 中文字符测试:")
    test_strings = [
        "简体中文：你好世界！",
        "繁體中文：你好世界！",
        "数学符号：α β γ δ ε ζ η θ",
        "特殊字符：★ ☆ ♠ ♥ ♦ ♣",
        "emoji表情：😀 😃 😄 😁 😆 😅",
        "箭头符号：→ ← ↑ ↓ ↔ ↕",
        "几何图形：■ □ ● ○ ▲ △",
        "货币符号：¥ $ € £ ¢ ₹"
    ]
    
    for i, test_str in enumerate(test_strings, 1):
        try:
            print(f"   {i:2d}. {test_str}")
        except UnicodeEncodeError as e:
            print(f"   {i:2d}. [编码错误] {e}")
    
    # 测试Manim相关的中文术语
    print(f"\n🎬 Manim相关术语:")
    manim_terms = [
        "动画 (Animation)",
        "场景 (Scene)", 
        "对象 (Mobject)",
        "变换 (Transform)",
        "渲染 (Render)",
        "帧率 (Frame Rate)",
        "时间轴 (Timeline)",
        "插值 (Interpolation)"
    ]
    
    for i, term in enumerate(manim_terms, 1):
        try:
            print(f"   {i}. {term}")
        except UnicodeEncodeError as e:
            print(f"   {i}. [编码错误] {e}")
    
    print(f"\n" + "=" * 60)
    print("✅ 中文编码测试完成！")
    print("如果以上所有文字都能正常显示，说明编码配置正确。")
    print("=" * 60)

def fix_encoding_if_needed():
    """如果需要，修复编码问题"""
    if sys.stdout.encoding.lower() not in ['utf-8', 'utf8']:
        print(f"⚠️  检测到非UTF-8编码: {sys.stdout.encoding}")
        print("正在尝试修复...")
        
        try:
            # 尝试重新包装stdout为UTF-8
            sys.stdout = io.TextIOWrapper(
                sys.stdout.buffer, 
                encoding='utf-8',
                errors='replace'
            )
            print("✅ 编码修复成功！")
        except Exception as e:
            print(f"❌ 编码修复失败: {e}")
            
        # Windows系统特殊处理
        if os.name == 'nt':
            try:
                os.system('chcp 65001 > nul')
                print("✅ Windows控制台编码已设置为UTF-8")
            except:
                print("⚠️  无法设置Windows控制台编码")

if __name__ == "__main__":
    # 首先尝试修复编码
    fix_encoding_if_needed()
    
    # 然后运行测试
    test_chinese_encoding()