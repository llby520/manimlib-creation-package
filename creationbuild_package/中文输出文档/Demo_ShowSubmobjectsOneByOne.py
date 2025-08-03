#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo_ShowSubmobjectsOneByOne.py
演示 ShowIncreasingSubsets 和 ShowSubmobjectsOneByOne 类的使用

确保中文输出正常显示的演示脚本
"""

from __future__ import annotations
import math   # 仅用于 ceil / floor / round
import sys
import io

# 确保标准输出使用UTF-8编码
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ========= 父类：累积显示 =========
class ShowIncreasingSubsets:
    def __init__(self, items, int_func=round):
        self.items = items
        self.int_func = int_func

    def frame(self, alpha: float) -> list[str]:
        n = len(self.items)
        idx = int(self.int_func(alpha * n))
        return self.items[:idx]           # 累积列表

# ========= 子类：聚光灯单灯 =========
class ShowSubmobjectsOneByOne(ShowIncreasingSubsets):
    def frame(self, alpha: float) -> list[str]:
        n = len(self.items)
        idx = int(math.ceil(alpha * n))
        if idx == 0:
            return []
        return [self.items[idx - 1]]      # 只保留当前一个

def main():
    """主函数 - 演示动画类的使用"""
    # 确保控制台能正确显示中文
    try:
        # 设置控制台编码为UTF-8（Windows系统）
        import os
        if os.name == 'nt':  # Windows系统
            os.system('chcp 65001 > nul')
    except:
        pass
    
    # 演示数据
    dots = ['🔴A', '🟡B', '🟢C', '🔵D']  # 使用emoji增强可视化效果
    alpha_steps = [0.0, 0.25, 0.5, 0.75, 1.0]
    
    print("=" * 60)
    print("📊 Manim动画类演示 - ShowIncreasingSubsets vs ShowSubmobjectsOneByOne")
    print("=" * 60)
    
    print("\n🔄 父类 ShowIncreasingSubsets (累积显示):")
    print("   特点：逐步累积显示所有元素")
    print("-" * 40)
    anim1 = ShowIncreasingSubsets(dots)
    for a in alpha_steps:
        result = anim1.frame(a)
        print(f"   α={a:.2f} -> {result}")
    
    print("\n💡 子类 ShowSubmobjectsOneByOne (单个聚光灯):")
    print("   特点：每次只显示一个元素（聚光灯效果）")
    print("-" * 40)
    anim2 = ShowSubmobjectsOneByOne(dots)
    for a in alpha_steps:
        result = anim2.frame(a)
        print(f"   α={a:.2f} -> {result}")
    
    print("\n" + "=" * 60)
    print("✅ 演示完成！中文显示正常 ✨")
    print("=" * 60)

# ========= 演示执行 =========
if __name__ == "__main__":
    main()