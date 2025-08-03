#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ManimLib Creation Package - 基本示例

这个示例展示了如何使用 creation 模块中的各种动画类。
"""

import sys
from pathlib import Path

# 添加父目录到路径，以便导入 creation 模块
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    # 尝试导入 manim（优先级顺序）
    try:
        from manim import *
        print("✅ 使用 manim (ManimCE)")
    except ImportError:
        try:
            from manimlib import *
            print("✅ 使用 manimlib")
        except ImportError:
            try:
                from manimgl import *
                print("✅ 使用 manimgl")
            except ImportError:
                print("❌ 未找到任何 Manim 包")
                print("请安装以下包之一:")
                print("  pip install manim")
                print("  pip install manimlib")
                print("  pip install manimgl")
                sys.exit(1)
except Exception as e:
    print(f"❌ 导入 Manim 时出错: {e}")
    sys.exit(1)

# 导入 creation 模块
try:
    import creation
    from creation import (
        ShowCreation, Write, DrawBorderThenFill,
        Uncreate, ShowSubmobjectsOneByOne, ShowPartial
    )
    print("✅ 成功导入 creation 模块")
except ImportError as e:
    print(f"❌ 导入 creation 模块失败: {e}")
    print("请确保 creation.py 在正确的位置")
    sys.exit(1)

class BasicCreationExample(Scene):
    """
    基本 Creation 动画示例
    
    展示各种 creation 动画的使用方法
    """
    
    def construct(self):
        """构建场景"""
        # 设置背景色（如果支持）
        try:
            self.camera.background_color = "#1e1e1e"
        except:
            pass
        
        # 1. 标题动画
        self.show_title()
        
        # 2. 基本形状动画
        self.show_basic_shapes()
        
        # 3. 文本动画
        self.show_text_animations()
        
        # 4. 复杂对象动画
        self.show_complex_animations()
        
        # 5. 结束
        self.show_ending()
    
    def show_title(self):
        """显示标题"""
        try:
            title = Text("ManimLib Creation Package", font_size=48)
        except:
            # 兼容性处理
            title = TextMobject("ManimLib Creation Package")
        
        title.set_color(YELLOW)
        
        # 使用 Write 动画
        self.play(Write(title), run_time=2)
        self.wait(1)
        
        # 移动到顶部
        self.play(title.animate.to_edge(UP), run_time=1)
        self.wait(0.5)
    
    def show_basic_shapes(self):
        """展示基本形状动画"""
        # 创建形状
        circle = Circle(radius=1.5, color=BLUE)
        square = Square(side_length=2, color=RED)
        triangle = Triangle(color=GREEN)
        
        # 排列形状
        shapes = VGroup(circle, square, triangle)
        shapes.arrange(RIGHT, buff=1.5)
        
        # 使用不同的 creation 动画
        self.play(
            ShowCreation(circle),
            DrawBorderThenFill(square),
            ShowPartial(triangle, 0, 1),
            run_time=3
        )
        self.wait(1)
        
        # 添加标签
        try:
            labels = VGroup(
                Text("ShowCreation", font_size=24),
                Text("DrawBorderThenFill", font_size=24),
                Text("ShowPartial", font_size=24)
            )
        except:
            labels = VGroup(
                TextMobject("ShowCreation"),
                TextMobject("DrawBorderThenFill"),
                TextMobject("ShowPartial")
            )
        
        for label, shape in zip(labels, shapes):
            label.next_to(shape, DOWN)
        
        self.play(Write(labels), run_time=2)
        self.wait(2)
        
        # 清除
        self.play(
            *[Uncreate(obj) for obj in [*shapes, labels]],
            run_time=2
        )
        self.wait(0.5)
    
    def show_text_animations(self):
        """展示文本动画"""
        try:
            text1 = Text("Hello, World!", font_size=36)
            text2 = Text("ManimLib Creation", font_size=36)
        except:
            text1 = TextMobject("Hello, World!")
            text2 = TextMobject("ManimLib Creation")
        
        text1.set_color(ORANGE)
        text2.set_color(PURPLE)
        
        # Write 动画
        self.play(Write(text1), run_time=2)
        self.wait(1)
        
        # 变换到新文本
        self.play(Transform(text1, text2), run_time=2)
        self.wait(1)
        
        # Uncreate 动画
        self.play(Uncreate(text1), run_time=1.5)
        self.wait(0.5)
    
    def show_complex_animations(self):
        """展示复杂对象动画"""
        # 创建复杂对象
        try:
            # 数学公式
            formula = MathTex(r"\sum_{n=1}^{\infty} \frac{1}{n^2} = \frac{\pi^2}{6}")
        except:
            try:
                formula = TexMobject(r"\sum_{n=1}^{\infty} \frac{1}{n^2} = \frac{\pi^2}{6}")
            except:
                formula = Text("Mathematical Formula", font_size=36)
        
        formula.set_color(TEAL)
        
        # 使用 ShowSubmobjectsOneByOne
        if hasattr(formula, 'submobjects') and len(formula.submobjects) > 1:
            self.play(ShowSubmobjectsOneByOne(formula), run_time=3)
        else:
            self.play(Write(formula), run_time=2)
        
        self.wait(2)
        
        # 创建装饰
        decoration = VGroup(
            Circle(radius=0.1, color=YELLOW).move_to(formula.get_corner(UL)),
            Circle(radius=0.1, color=YELLOW).move_to(formula.get_corner(UR)),
            Circle(radius=0.1, color=YELLOW).move_to(formula.get_corner(DL)),
            Circle(radius=0.1, color=YELLOW).move_to(formula.get_corner(DR))
        )
        
        self.play(ShowCreation(decoration), run_time=1)
        self.wait(1)
        
        # 清除所有
        self.play(
            Uncreate(formula),
            Uncreate(decoration),
            run_time=2
        )
        self.wait(0.5)
    
    def show_ending(self):
        """显示结束"""
        try:
            ending_text = Text("Thanks for using\nManimLib Creation!", font_size=36)
        except:
            ending_text = TextMobject("Thanks for using\\\\ManimLib Creation!")
        
        ending_text.set_color(GOLD)
        
        self.play(Write(ending_text), run_time=2)
        self.wait(2)
        
        # 最终效果
        self.play(
            ending_text.animate.scale(1.2),
            run_time=1
        )
        self.wait(1)
        
        self.play(Uncreate(ending_text), run_time=1.5)
        self.wait(1)

class SimpleCreationDemo(Scene):
    """
    简单演示场景
    
    适合快速测试和验证
    """
    
    def construct(self):
        """构建简单演示"""
        # 创建简单对象
        circle = Circle(color=BLUE)
        
        try:
            text = Text("Creation Demo", font_size=32)
        except:
            text = TextMobject("Creation Demo")
        
        text.next_to(circle, DOWN)
        
        # 简单动画序列
        self.play(ShowCreation(circle), run_time=2)
        self.play(Write(text), run_time=1.5)
        self.wait(1)
        
        # 组合动画
        group = VGroup(circle, text)
        self.play(group.animate.scale(1.5), run_time=1)
        self.wait(1)
        
        # 结束
        self.play(Uncreate(group), run_time=2)
        self.wait(0.5)

def main():
    """
    主函数 - 运行示例
    """
    print("🎬 ManimLib Creation Package - 基本示例")
    print("=" * 50)
    
    # 检查 creation 模块
    try:
        import creation
        print(f"✅ Creation 模块版本: {getattr(creation, '__version__', '未知')}")
        
        # 运行自测试
        if hasattr(creation, '_module_self_test'):
            print("🧪 运行模块自测试...")
            creation._module_self_test()
            print("✅ 自测试通过")
    except Exception as e:
        print(f"❌ Creation 模块测试失败: {e}")
        return 1
    
    print("\n📝 使用说明:")
    print("1. 确保已安装 manim 或相关包")
    print("2. 运行以下命令渲染动画:")
    print(f"   manim {__file__} BasicCreationExample")
    print(f"   manim {__file__} SimpleCreationDemo")
    print("\n🎯 如果遇到问题，请检查:")
    print("- Manim 是否正确安装")
    print("- creation.py 是否在正确位置")
    print("- Python 版本是否 >= 3.8")
    
    return 0

if __name__ == "__main__":
    # 如果直接运行，显示使用说明
    sys.exit(main())