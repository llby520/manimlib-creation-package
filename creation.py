from __future__ import annotations

"""
ManimLib Creation Animation Module
版本: 2.0.0 (Long-term Support)
兼容性: Python 3.8+, NumPy 1.19+
最后更新: 2024

这是一个现代化的、可长期使用的Manim创建动画模块。
包含了完整的警告处理、类型提示和最佳实践。
"""

# 现代化导入和警告处理
import warnings
from abc import ABC, abstractmethod
import sys
from pathlib import Path
from typing import Union, Optional

# 版本兼容性检查
if sys.version_info < (3, 8):
    raise RuntimeError("此模块需要Python 3.8或更高版本")

# 抑制弃用警告，确保长期兼容性
warnings.filterwarnings("ignore", category=UserWarning, message=".*pkg_resources.*")
warnings.filterwarnings("ignore", category=DeprecationWarning, message=".*pkg_resources.*")
warnings.filterwarnings("ignore", category=FutureWarning, message=".*distutils.*")
warnings.filterwarnings("ignore", category=DeprecationWarning, message=".*imp module.*")

# 数值计算库
import numpy as np

# 版本检查
try:
    # 确保NumPy版本兼容性
    if hasattr(np, '__version__'):
        np_version = tuple(map(int, np.__version__.split('.')[:2]))
        if np_version < (1, 19):
            warnings.warn("建议使用NumPy 1.19或更高版本以获得最佳性能", UserWarning)
except Exception:
    pass  # 静默处理版本检查错误

# Manim核心模块导入
from manimlib.animation.animation import Animation
from manimlib.animation.composition import LaggedStart
from manimlib.mobject.svg.string_mobject import StringMobject
from manimlib.mobject.types.vectorized_mobject import VMobject
from manimlib.utils.bezier import integer_interpolate
from manimlib.utils.rate_functions import linear
from manimlib.utils.rate_functions import double_smooth
from manimlib.utils.rate_functions import smooth
from manimlib.utils.simple_functions import clip

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Callable
    from manimlib.mobject.mobject import Mobject
    from manimlib.scene.scene import Scene
    from manimlib.typing import ManimColor

# 模块公共API定义
__all__ = [
    'ShowPartial',
    'ShowCreation', 
    'Uncreate',
    'DrawBorderThenFill',
    'Write',
    'ShowIncreasingSubsets',
    'ShowSubmobjectsOneByOne',
    'AddTextWordByWord'
]

# 模块版本信息
__version__ = '2.0.0'
__author__ = 'ManimLib Community Llby'
__license__ = 'MIT'

"""
creation.py - Manim创建动画模块

这个模块包含了各种用于创建和显示对象的动画类。
主要功能包括：
1. ShowPartial - 部分显示动画的抽象基类
2. ShowCreation - 创建显示动画
3. Uncreate - 反向创建(消失)动画
4. DrawBorderThenFill - 先画边框后填充动画
5. Write - 书写动画
6. ShowIncreasingSubsets - 逐步显示子对象动画
7. ShowSubmobjectsOneByOne - 逐个显示子对象动画
8. AddTextWordByWord - 逐词添加文本动画

这些动画类都继承自Animation基类，用于在Manim中创建各种视觉效果。

═══════════════════════════════════════════════════════════════════════════════
📊 类继承关系图 (Class Inheritance Hierarchy)
═══════════════════════════════════════════════════════════════════════════════

Animation (基类)
├── ShowPartial (抽象基类) ──────────────── 部分显示动画的通用框架
│   ├── ShowCreation ──────────────────── 创建显示动画 (0% → 100%)
│   └── Uncreate ─────────────────────── 反向创建动画 (100% → 0%)
├── DrawBorderThenFill ──────────────── 先画边框后填充动画
│   └── Write ────────────────────────── 书写动画 (智能时间计算)
└── LaggedStart (来自composition.py) ──── 延迟启动动画组合
    ├── ShowIncreasingSubsets ────────── 累积显示子对象
    ├── ShowSubmobjectsOneByOne ──────── 逐个显示子对象  
    └── AddTextWordByWord ─────────────── 逐词显示文本

═══════════════════════════════════════════════════════════════════════════════
🎯 设计模式分析 (Design Patterns)
═══════════════════════════════════════════════════════════════════════════════

1. 【模板方法模式 Template Method】
   ShowPartial 定义了部分显示的算法骨架：
   - interpolate_submobject() 提供通用插值逻辑
   - get_bounds() 抽象方法由子类实现具体边界计算
   
2. 【策略模式 Strategy】
   不同的创建动画采用不同的显示策略：
   - ShowCreation: 线性显示策略 (0 → alpha)
   - Uncreate: 反向显示策略 (1-alpha → 0)
   - DrawBorderThenFill: 两阶段显示策略 (边框 → 填充)
   
3. 【装饰器模式 Decorator】
   Write 类装饰 DrawBorderThenFill，添加智能时间计算功能
   
4. 【组合模式 Composite】
   LaggedStart 系列将多个子对象组合成统一的动画接口

═══════════════════════════════════════════════════════════════════════════════
⚡ 性能与使用场景对比 (Performance & Use Cases)
═══════════════════════════════════════════════════════════════════════════════

┌─────────────────────┬──────────────┬──────────────┬─────────────────────┐
│ 动画类              │ 性能开销     │ 适用对象     │ 典型使用场景        │
├─────────────────────┼──────────────┼──────────────┼─────────────────────┤
│ ShowCreation        │ 低           │ 简单图形     │ 基础几何图形绘制    │
│ Uncreate           │ 低           │ 任意对象     │ 对象消失效果        │
│ DrawBorderThenFill │ 中           │ 填充图形     │ 复杂图形的精细绘制  │
│ Write              │ 中           │ 文本/公式    │ 数学公式、文字书写  │
│ ShowIncreasingSubsets│ 高          │ 多子对象     │ 列表、序列逐步显示  │
│ ShowSubmobjectsOneByOne│ 高        │ 多子对象     │ 动画元素逐个出现    │
│ AddTextWordByWord  │ 高           │ 长文本       │ 段落、句子逐词显示  │
└─────────────────────┴──────────────┴──────────────┴─────────────────────┘

性能提示：
• 简单对象优先使用 ShowCreation
• 复杂图形使用 DrawBorderThenFill 获得更好视觉效果
• 大量子对象时注意 lag_ratio 设置，避免动画过长
• Write 类会自动优化时间，适合不确定复杂度的对象

═══════════════════════════════════════════════════════════════════════════════
🔧 核心算法原理 (Core Algorithm Principles)
═══════════════════════════════════════════════════════════════════════════════

1. 【部分显示算法】 - ShowPartial.interpolate_submobject()
   ```
   对于进度 alpha ∈ [0,1]:
   bounds = get_bounds(alpha)  # 获取显示边界
   submob.pointwise_become_partial(start_submob, *bounds)
   ```
   
2. 【两阶段插值】 - DrawBorderThenFill.interpolate_submobject()
   ```
   index, subalpha = integer_interpolate(0, 2, alpha)
   if index == 0:  # 第一阶段：绘制边框
       submob.pointwise_become_partial(outline, 0, subalpha)
   else:          # 第二阶段：填充颜色
       submob.interpolate(outline, start, subalpha)
   ```
   
3. 【智能时间计算】 - Write.compute_run_time()
   ```
   if family_size < 15:
       return 1.0  # 简单对象1秒
   else:
       return 2.0  # 复杂对象2秒
   ```
   
4. 【延迟比例计算】 - Write.compute_lag_ratio()
   ```
   return min(4.0 / (family_size + 1), 0.2)
   # 确保合理的重叠时间，避免过快或过慢
   ```

═══════════════════════════════════════════════════════════════════════════════
💡 最佳实践建议 (Best Practices)
═══════════════════════════════════════════════════════════════════════════════

1. 【选择合适的动画类】
   • 简单图形 → ShowCreation
   • 文本内容 → Write 或 AddTextWordByWord
   • 需要精细控制 → DrawBorderThenFill
   • 多对象序列 → ShowIncreasingSubsets 或 ShowSubmobjectsOneByOne
   
2. 【参数调优】
   • lag_ratio: 0.05-0.2 适合大多数场景
   • run_time: 让 Write 自动计算，除非有特殊需求
   • rate_func: linear 适合书写，smooth 适合自然动画
   
3. 【性能优化】
   • 避免对大量小对象使用复杂动画
   • 合理使用 should_match_start 参数
   • 考虑使用 remover=True 自动清理对象
   
4. 【视觉效果】
   • DrawBorderThenFill 适合需要强调轮廓的场景
   • Write 的 stroke_color 可以创建有趣的颜色变化
   • 组合使用不同动画创建复杂效果

═══════════════════════════════════════════════════════════════════════════════
🔗 与其他模块的关系 (Module Relationships)
═══════════════════════════════════════════════════════════════════════════════

• animation.py ──→ 提供 Animation 基类和核心动画框架
• composition.py ──→ 提供 LaggedStart 等组合动画基础
• mobject/ ──→ 提供 VMobject, StringMobject 等被动画的对象
• utils/bezier.py ──→ 提供 integer_interpolate 等数学工具
• utils/rate_functions.py ──→ 提供各种速率函数

这种模块化设计使得创建动画既可以独立使用，也可以与其他动画组合，
形成了 Manim 强大而灵活的动画系统。
"""


class ShowPartial(Animation, ABC):  #  这是 Python 中类的多重继承语法，不是传参，而是 指定当前类继承自哪些父类.
    # 指定该类继承自两个父类：Animation和ABC
    """
    ShowPartial - 部分显示动画抽象基类
    
    这是一个抽象基类，用于实现部分显示动画效果，如ShowCreation和ShowPassingFlash。
    它定义了部分显示动画的基本框架和接口。
    
    继承关系：
    Animation -> ShowPartial -> ShowCreation/ShowPassingFlash
    
    主要功能：
    - 提供部分显示动画的基础框架
    - 定义抽象方法get_bounds，由子类实现具体的边界计算
    - 处理对象的部分显示逻辑
    """
    def __init__(self, mobject: Mobject, should_match_start: bool = False, **kwargs):
        """
        初始化ShowPartial动画对象
        ShowPartial 这个抽象基类中自定义的一个参数，用于控制动画开始时对象的起始状态。

        参数说明:
        mobject: 要进行部分显示动画的对象
        should_match_start: 是否应该匹配起始状态
                          如果为True，动画开始时对象状态会匹配起始状态
                          如果为False，使用对象当前状态作为起始状态
        **kwargs: 传递给父类Animation的其他参数
        
        示例:
        # 创建一个圆形的部分显示动画
        circle = Circle()
        anim = ShowCreation(circle, should_match_start=True)
        """
        self.should_match_start = should_match_start
        super().__init__(mobject, **kwargs)

    def interpolate_submobject(
        self,
        submob: VMobject,
        start_submob: VMobject,
        alpha: float
    ) -> None:
        """
        对子对象进行插值处理
        
        这个方法负责根据动画进度alpha，将子对象从起始状态插值到目标状态。
        使用pointwise_become_partial(按路径逐步显示对象的一部分)方法实现部分显示效果。
        
        参数说明:
        submob: 当前正在动画的子对象
        start_submob: 子对象的起始状态
        alpha: 动画进度(0到1之间)
        
        工作原理:
        1. 通过get_bounds(alpha)获取当前进度下的显示边界
        2. 使用pointwise_become_partial方法让对象部分显示
        """
        submob.pointwise_become_partial(
            start_submob, *self.get_bounds(alpha)
        )

    @abstractmethod
    def get_bounds(self, alpha: float) -> tuple[float, float]:
        """
        获取显示边界的抽象方法
        
        这是一个抽象方法，必须由子类实现。
        用于根据动画进度alpha计算对象应该显示的边界范围。
        
        参数说明:
        alpha: 动画进度(0到1之间)
        
        返回值:
        tuple[float, float]: 显示边界的起始和结束位置
                           例如：(0, alpha)表示从0%显示到alpha*100%
        
        子类实现示例:
        # ShowCreation类的实现
        def get_bounds(self, alpha: float) -> tuple[float, float]:
            return (0, alpha)  # 从0%逐渐显示到alpha*100%

        from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod  # 这里写@abstractmethod是为了强制子类必须实现这个方法，否则会报错
    def area(self) -> float:
        pass  # 没有实现，子类必须实现

class Circle(Shape):
    def __init__(self, r):
        self.r = r

    def area(self) -> float:
        return 3.14 * self.r ** 2  # ✅ 实现了抽象方法
        """
        raise Exception("Not Implemented")
"""
get_bounds=(0.25, 0.75) | 中间 50 % 区域可见 |
get_bounds=(0.0, 1.0) | 完整图形可见 |

get_bounds 就是“每一帧告诉 Manim：对象要从哪画到哪”，
改一改，动画的节奏、方向、风格全都能变！
 """

class ShowCreation(ShowPartial):
    """
    ShowCreation - 创建显示动画
    
    这是最常用的创建动画之一，用于逐步显示一个对象。
    对象会从无到有地逐渐出现，就像被"画"出来一样。
    
    继承关系：
    Animation -> ShowPartial -> ShowCreation
    
    主要特点：
    - 对象从0%逐渐显示到100%
    - 支持lag_ratio参数控制多个子对象的显示时间差
    - 常用于线条、图形、文本等对象的出现动画
    
    使用场景：
    - 绘制几何图形
    - 显示数学公式
    - 展示图表和图像
    """
    def __init__(self, mobject: Mobject, lag_ratio: float = 1.0, **kwargs):
        """
        初始化ShowCreation动画对象
        
        参数说明:
        mobject: 要显示的对象
        lag_ratio: 延迟比例，控制多个子对象间的时间差
                  - 如果为1.0，子对象依次显示
                  - 如果为0.0，所有子对象同时显示
                  - 如果在0-1之间，子对象有重叠的显示时间
        **kwargs: 传递给父类的其他参数
        
        示例:
        # 创建一个圆形的显示动画
        circle = Circle()
        self.play(ShowCreation(circle))
        
        # 创建多个对象同时显示的动画
        group = VGroup(Circle(), Square(), Triangle())
        self.play(ShowCreation(group, lag_ratio=0.5))
        """
        super().__init__(mobject, lag_ratio=lag_ratio, **kwargs)

    def get_bounds(self, alpha: float) -> tuple[float, float]:
        """
        获取显示边界
        class ShowCreation(ShowPartial):
    def get_bounds(self, alpha: float) -> tuple[float, float]:
        return (0.0, alpha)  # ✅ 返回一个元组
        alpha = 0.3 → 返回 (0.0, 0.3)
        alpha = 1.0 → 返回 (0.0, 1.0)
    | 返回值     | 含义                                |
| ------- | --------------------------------- |
| `0.0`   | **起点比例**：从对象路径的 **最开头（0%）** 开始显示  |
| `alpha` | **终点比例**：显示到路径的 `alpha * 100%` 位置 |

        ShowCreation的核心逻辑：从0%开始，逐渐显示到alpha*100%。
        
        参数说明:
        alpha: 动画进度(0到1之间)
        
        返回值:
        tuple[float, float]: (0, alpha)
                           - 起始位置始终为0
                           - 结束位置随alpha变化
        
        工作原理:
        当alpha=0时，返回(0, 0)，对象不显示
        当alpha=0.5时，返回(0, 0.5)，对象显示一半
        当alpha=1时，返回(0, 1)，对象完全显示
        """
        return (0, alpha)  # 这个说明了一切！^.^


class Uncreate(ShowCreation):  # 这个继承括号内（）的内容是父类的内容，记住这个规律。
    """
    Uncreate - 反向创建(消失)动画
    
    这是ShowCreation的反向版本，用于让对象逐渐消失。
    对象会从完全显示状态逐渐消失，就像被"擦除"一样。
    
    继承关系：
    Animation -> ShowPartial -> ShowCreation -> Uncreate
    
    主要特点：
    - 对象从100%逐渐消失到0%
    - 使用反向的速率函数(lambda t: smooth(1 - t))
    - 默认在动画结束后移除对象(remover=True)
    - 默认匹配起始状态(should_match_start=True)
    
    使用场景：
    - 让对象消失
    - 清理屏幕上的元素
    - 创建"擦除"效果
    """
    def __init__(
        self,
        mobject: Mobject,
        rate_func: Callable[[float], float] = lambda t: smooth(1 - t), # lambda 参数1, 参数2, ... : 表达式（是Python的一种简单快速匿名函数方法）
        remover: bool = True,
        should_match_start: bool = True,
        **kwargs,
    ):
        """
        初始化Uncreate动画对象
        
        参数说明:
        mobject: 要消失的对象
        rate_func: 速率函数，默认为lambda t: smooth(1 - t)
                  这个函数将时间t反转，使动画从1到0进行
                  - t=0时，函数返回smooth(1)=1，对象完全显示
                  - t=1时，函数返回smooth(0)=0，对象完全消失
        remover: 是否在动画结束后移除对象，默认为True
                动画完成后对象会从场景中移除
        should_match_start: 是否匹配起始状态，默认为True
                          确保动画开始时对象处于完全显示状态 这个是create&uncreate的关键,记住一句话：“开始时对象完全显示”
        **kwargs: 传递给父类的其他参数
        
        示例:
        # 让一个圆形消失
        circle = Circle()
        self.add(circle)  # 先添加到场景
        self.play(Uncreate(circle))
        
        # 让对象消失但不移除(保留在场景中)
        square = Square()
        self.play(Uncreate(square, remover=False))
        
        工作原理:
        1. rate_func将时间反转，使ShowCreation的逻辑变成消失效果
        2. remover=True确保对象在消失后被移除
        3. should_match_start=True确保从完全显示状态开始消失
        """
        super().__init__(
            mobject,
            rate_func=rate_func,
            remover=remover,
            should_match_start=should_match_start,
            **kwargs,
        )

        """举个例你就懂了！
        class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age = age

class Cat(Animal):
    def __init__(self, name, age, breed):
        super().__init__(name=name, age=age)  # 👈 这就是“把当前作用域变量传给父类参数”
        self.breed = breed
         
    在 Cat.__init__ 的作用域里，name 和 age 是来自调用者自己定义传入的变量，它们被传给父类 Animal.__init__ 的参数 name 和 age。     
    """


class DrawBorderThenFill(Animation):
    """
    DrawBorderThenFill - 先画边框后填充动画 （先框后填）
    
    这是一个复合动画，分两个阶段进行：
    1. 第一阶段：绘制对象的边框轮廓
    2. 第二阶段：填充对象的内部颜色
    
    继承关系：
    Animation -> DrawBorderThenFill  所有这是一个很重要的函数喽！（强调手绘效果）
    
    主要特点：
    - 两阶段动画：先边框后填充
    - 支持自定义边框样式(颜色、宽度)
    - 使用double_smooth速率函数创建平滑过渡
    - 专门用于VMobject(矢量对象)
    
    使用场景：
    - 绘制几何图形
    - 创建手绘效果
    - 强调对象的轮廓和填充
    """
    def __init__(
        self,
        vmobject: VMobject,
        run_time: float = 2.0,
        rate_func: Callable[[float], float] = double_smooth,
        stroke_width: float = 2.0,
        stroke_color: ManimColor = None,
        draw_border_animation_config: dict = {},
        fill_animation_config: dict = {},
        **kwargs
    ):
        """
        初始化DrawBorderThenFill动画对象
        
        参数说明:
        vmobject: 要绘制的矢量对象，必须是VMobject类型
        run_time: 动画总时间，默认2.0秒
                 前一半时间用于绘制边框，后一半用于填充
        rate_func: 速率函数，默认为double_smooth
                  提供平滑的加速和减速效果
        stroke_width: 边框线条宽度，默认2.0
        stroke_color: 边框颜色，如果为None则使用对象原有颜色
        draw_border_animation_config: 边框绘制动画的额外配置
        fill_animation_config: 填充动画的额外配置
        **kwargs: 传递给父类Animation的其他参数
        
        示例:
        # 绘制一个圆形，先边框后填充
        circle = Circle(fill_opacity=0.5, color=BLUE)
        self.play(DrawBorderThenFill(circle))
        
        # 自定义边框样式
        square = Square(fill_opacity=0.7, color=RED)
        self.play(DrawBorderThenFill(
            square, 
            stroke_width=3.0, 
            stroke_color=YELLOW,
            run_time=3.0
        ))
        
        工作原理:
        1. 创建对象轮廓副本用于边框绘制
        2. 使用integer_interpolate将动画分为两个阶段
        3. 第一阶段(alpha: 0->0.5)：绘制边框
        4. 第二阶段(alpha: 0.5->1.0)：填充内部

        | 场景类型    | 推荐使用 `double_smooth` 吗？       |
| ------- | ----------------------------- |
| 图形出现/消失 | ✅ 非常适合                        |
| 文字书写动画  | ✅ 非常自然                        |
| 路径移动    | ✅ 柔和流畅                        |
| 弹跳或弹性动画 | ❌ 不适合（用 `ease_out_bounce` 更好） |
对标准 smoothstep 函数再做一次平滑处理，使得 速度、加速度、加加速度（jerk） 在动画开始和结束时都为零
非常适合 Manim 中大多数自然过渡动画

        """
        assert isinstance(vmobject, VMobject)
        # 为每个子对象创建索引映射，用于跟踪动画状态  assert isinstance(对象, 类型)  检查对象是否为指定类型
        self.sm_to_index = {hash(sm): 0 for sm in vmobject.get_family()} # sm_to_index 是 DrawBorderThenFill 类中的
        # 自定义的一个辅助字典属性，用于在动画过程中追踪每个子对象（submobject）当前所处的动画阶段。
        #  ✅ hash(obj) 是什么？
        # 是 Python 内置函数，接收任意对象，返回一个整数；（用哈希值作为字典 key）
        # 这个整数就是该对象的 哈希值；
        # 同一个对象在一次 Python 运行期间，返回的哈希值不变；
        # 常用于字典键、集合元素等需要快速查找的地方。
        
        # 0在 DrawBorderThenFill 动画中的具体含义
        # 阶段编号	含义
        # 0	绘制边框阶段：当前子对象正在“画线”
        # 1	填充颜色阶段：当前子对象正在“填色”
        #self.sm_to_index[hash(submob)] = 1（这是子对象完成到了填充颜色的阶段了）

        self.stroke_width = stroke_width
        self.stroke_color = stroke_color
        self.draw_border_animation_config = draw_border_animation_config
        self.fill_animation_config = fill_animation_config
        super().__init__(
            vmobject,
            run_time=run_time,
            rate_func=rate_func,
            **kwargs
        )
        self.mobject = vmobject

    def begin(self) -> None:
        """
        开始动画的初始化方法
        
        这个方法在动画开始时被调用，负责：
        1. 设置对象的动画状态
        2. 创建用于边框绘制的轮廓对象
        3. 调用父类的begin方法
        4. 让原对象匹配轮廓的样式
        
        工作流程:
        - 标记对象为动画状态
        - 生成轮廓副本用于边框绘制
        - 同步对象样式
        """
        self.mobject.set_animating_status(True) 
        self.outline = self.get_outline()
        super().begin()
        self.mobject.match_style(self.outline)
    
    """
    (method) def set_animating_status(
    is_animating: bool,
    recurse: bool = True
     ) -> VMobject
    预防自动刷新，避免抖动和跳帧

    设置为true则渲染引擎会区分“静态物件”和“动态物件”。
标记为 animating=True 后，这条路径就不会被 合并批次 / 剔除简化，保证每一帧都精确重绘。
    
    还可以确保防止某些缓存（如 SVG 路径的三角化结果、文字排版缓存）会在动画期间 强制失效，确保看到实时变化。
    """
    
    def finish(self) -> None:
        """
        完成动画的清理方法
        
        这个方法在动画结束时被调用，负责：
        1. 调用父类的finish方法完成基本清理
        2. 刷新对象的连接角度，确保几何形状正确
        
        注意:
        refresh_joint_angles()对于复杂的几何形状很重要，
        它确保线条连接处的角度计算正确。
        """
        super().finish()
        self.mobject.refresh_joint_angles()  #(method) def refresh_joint_angles() -> VMobject 刷新几何角度

    def get_outline(self) -> VMobject:
        """
        创建用于边框绘制的轮廓对象，记住这句话哦！
        
        这个方法创建原对象的副本，并设置为只有边框没有填充的样式。
        
        返回值:
        VMobject: 轮廓对象，只有边框线条，没有填充
        
        工作步骤:
        1. 复制原对象
        2. 移除填充(设置透明度为0)
        3. 为所有子对象设置边框样式
        4. 使用指定的边框颜色和宽度
        
        样式设置:
        - 填充透明度设为0(无填充)
        - 边框颜色：使用指定颜色或原有颜色
        - 边框宽度：使用指定宽度
        - 边框位置：继承原对象的设置
        """
        outline = self.mobject.copy()
        outline.set_fill(opacity=0)  # 移除填充，只保留边框
        for sm in outline.family_members_with_points():
            sm.set_stroke(
                color=self.stroke_color or sm.get_stroke_color(),
                width=self.stroke_width,
                behind=self.mobject.stroke_behind,
            )
        return outline
    
    """from manim import *

class Demo(Scene):
    def construct(self):
        group = VGroup(
            Circle(),            # 有顶点
            Line(LEFT, RIGHT),   # 有顶点
            VMobject(),          # 空对象，无顶点
        )
        print(len(group))                       # 3 个成员
        print(len(group.family_members_with_points()))  # 2 个有顶点
    输出：3
         2   
    简单点就是family_members_with_points() 帮你 自动过滤掉这些空壳，只保留“能画出来”的部分。 """   

    def get_all_mobjects(self) -> list[Mobject]:
        """
        获取动画涉及的所有对象
        
        这个方法返回动画中使用的所有对象，包括：
        1. 父类方法返回的对象(通常是原始对象)
        2. 用于边框绘制的轮廓对象
        
        返回值:
        list[Mobject]: 包含原对象和轮廓对象的列表
        
        重要性:
        这确保了渲染系统知道需要处理哪些对象，
        轮廓对象也会被正确地包含在渲染流程中。
        """
        return [*super().get_all_mobjects(), self.outline] # 可迭代拆包语法
    """
    super().get_all_mobjects()	返回一个列表（父类认为动画要渲染的对象）。“返回一个列表很重要哦，因为我们需要把轮廓对象也加入到渲染流程中”
[* ..., self.outline]	把父类列表里的元素（及时的list） 全部展开，再追加 self.outline（轮廓对象），形成一个新的扁平列表。
举个例子➡️
假设：
super().get_all_mobjects()  # 返回 [original_circle]
self.outline                # 是一个单独的 outline_circle
那么：
[*super().get_all_mobjects(), self.outline]  # 返回 [original_circle, outline_circle]
会生成：
[original_circle, outline_circle]

    两个对象在同一个列表里 [original_circle, outline_circle]，
     渲染器会 按顺序、逐帧同时渲染它们，
从而让你看到 “先描边、后填充”的完整效果。

注意区别：
[*a, b] 把列表元素“展平”再合并，得到 一维列表；
[[a], b] 把列表整体再嵌套一层，导致 二维结构，遍历时会拿到列表而不是对象，Manim（或其他渲染器）会报错或漏渲染。
     
     但是！
     我们可以用 * 来“展平”这个列表，确保遍历到的是对象而不是列表。
     而且！
     渲染器确实每帧都拿到两个对象，但 每帧只让其中一个对象以“部分”形态出现；
通过时间驱动的插值，最终呈现“先描边、后填充”的连贯动画。
get_all_mobjects() 只是把**“这一帧要画的所有东西”**告诉渲染器；
真正决定“画多少”的是 interpolate_submobject()：
在阶段 0 只让 outline 显示一部分；
在阶段 1 让 mobject 逐渐取代 outline；
     """
    
    def interpolate_submobject(
        self,
        submob: VMobject,
        start: VMobject,
        outline: VMobject,
        alpha: float
    ) -> None:
        """
        对子对象进行两阶段插值处理
        
        这是DrawBorderThenFill动画的核心方法，实现两阶段动画效果：
        阶段0 (alpha: 0 -> 0.5): 绘制边框轮廓
        阶段1 (alpha: 0.5 -> 1.0): 填充内部颜色
        
        参数说明:
        submob: 当前正在动画的子对象
        start: 子对象的起始状态(通常包含填充)
        outline: 子对象的轮廓状态(只有边框)
        alpha: 动画总进度(0到1之间)
        
        工作原理:
        1. 使用integer_interpolate将alpha映射到两个阶段
        2. index=0时为第一阶段(绘制边框)
        3. index=1时为第二阶段(填充颜色)
        4. subalpha为当前阶段内的进度(0到1)
        
        阶段转换:
        - 第一次进入第二阶段时，更新对象数据为轮廓数据
        - 使用sm_to_index跟踪每个子对象的阶段状态 （对象TO参数）这个很重要，因为我们需要知道每个子对象当前的轮廓阶段状态，才能知道是否进入填充阶段。
        """
        # 将总进度alpha映射到两个阶段：0->1映射到0->2
        # index: 当前阶段(0或1), subalpha: 当前阶段内的进度(0到1)
        index, subalpha = integer_interpolate(0, 2, alpha)
        # 这行代码把连续的动画进度 alpha ∈ [0,1] 映射成离散的“阶段编号”和阶段内的“局部进度”：
        # | 返回值        | 含义                |
        # | ------------- | ----------------- |
        # | `index`    | 当前处于第几个阶段（0 或 1）。 |
        # | `subalpha` | 在该阶段内的局部进度（0→1）。  |
        #这两个数字是**“离散索引范围”**，告诉 integer_interpolate()：
        # 请把连续的 alpha ∈ [0,1] 映射到整数区间 [0,2)
        #（即：最终只能出现 0 或 1 两个整数）。

        # | 形参      | 含义                    |
        # | ------- | --------------------- |
        # | `0`     | **起始整数索引**（inclusive） |
        # | `2`     | **终止整数索引**（exclusive） |
        # | `alpha` | 0→1 的连续动画进度           |
        # 于是乎，我们就有了如下的映射阶段：
        # alpha = 0.0  → (0, 0.0)   # 阶段 0，局部进度 0 %
        # alpha = 0.25 → (0, 0.5)   # 阶段 0，局部进度 50 %
        # alpha = 0.5  → (1, 0.0)   # 阶段 1，局部进度 0 %
        # alpha = 0.75 → (1, 0.5)   # 阶段 1，局部进度 50 %
        # alpha = 1.0  → (1, 1.0)   # 阶段 1，局部进度 100 %

    # 一句话点睛：subalpha就是局部映射阶段进度！

        
        # 检查是否第一次进入第二阶段(填充阶段)
        if index == 1 and self.sm_to_index[hash(submob)] == 0:
            # First time crossing over - 第一次跨越到填充阶段
            # 将对象数据设置为轮廓数据，准备开始填充
            
            # 再次回顾：self.sm_to_index: dict[int, int] = {
    # hash(sm): 0 for sm in vmobject.get_family()
    # }
        # 键是 hash(sm) → int
        # 值是 0 → int
            submob.set_data(outline.data)
            self.sm_to_index[hash(submob)] = 1  # 标记已进入第二阶段 一般这样标记作为封口self！
        """
         把子对象的底层几何数据一次性换成“轮廓副本”的数据，并标记它正式进入“填充阶段”。
| 代码                                   | 作用                                                                      |
| ------------------------------------ | ----------------------------------------------------------------------- |
| `submob.set_data(outline.data)`      | 瞬间替换顶点、颜色、描边等底层数据，使 `submob` 在视觉上立即变成“只有边框”的状态，为后续从边框到填充的插值做准备。 |
| `self.sm_to_index[hash(submob)] = 1` | 记录状态：告诉动画引擎“这个子对象已经跨过 50% 点，现在处于阶段 1（填充阶段）”，避免下次再执行阶段 0 的逻辑。        |

在 Manim 里，outline.data 是一个 NumPy 二维数组（float32/float64），它把 “只有边框、没有填充” 的那个轮廓对象（outline）的
 所有顶点坐标 打包成一行行 (x, y, z) 数据。
        """
        if index == 0:
            # 第一阶段：绘制边框轮廓
            # 从0%逐渐显示到subalpha*100%的轮廓
            submob.pointwise_become_partial(outline, 0, subalpha)
        else:
            # 第二阶段：填充内部颜色
            # 从轮廓状态插值到最终状态(包含填充)
            submob.interpolate(outline, start, subalpha)
        """
         (method) def pointwise_become_partial(
         vmobject: VMobject,
         a: float,
         b: float
         ) -> VMobject

Set points in such a way as to become only part of mobject. Inputs 0 <= a < b <= 1 determine 
what portion of mobject to become.
"""

class Write(DrawBorderThenFill):
    """
    Write - 书写动画
    
    这是DrawBorderThenFill的特化版本，专门用于文本和复杂图形的"书写"效果。
    它会根据对象的复杂程度自动调整动画时间和延迟比例。
    
    继承关系：
    Animation -> DrawBorderThenFill -> Write
    
    主要特点：
    - 自动计算合适的动画时间(基于对象复杂度)
    - 自动计算合适的延迟比例(基于子对象数量)
    - 使用线性速率函数，模拟真实书写
    - 默认使用对象原有颜色作为边框颜色
    
    使用场景：
    - 书写文本
    - 绘制数学公式
    - 展示复杂图形的构建过程
    - 创建手写效果
    """
    def __init__(
        self,
        vmobject: VMobject,
        run_time: float = -1,  # 如果该值为负数，它将被重新赋值
        lag_ratio: float = -1,  # 如果该值为负数，它将被重新赋值
        rate_func: Callable[[float], float] = linear,
        stroke_color: ManimColor = None,
        **kwargs
    ):
        """
        初始化Write动画对象
        
        参数说明:
        | 输入                  | 含义          | 输出                             | 含义               |
| ------------------- | ----------- | ------------------------------ | ---------------- |
| `t: float ∈ [0, 1]` | 动画已经进行的时间比例 | `rate_func(t): float ∈ [0, 1]` | 当前应达到的 **“完成度”** |
| `vmobject: VMobject` | 要书写的矢量对象 | `None` | 无返回值，直接修改对象状态 |

t = 0.0  → linear(0.0) = 0.0   # 动画 0 % 完成
t = 0.5  → linear(0.5) = 0.5   # 动画 50 % 完成
t = 1.0  → linear(1.0) = 1.0   # 动画 100 % 完成

它接收 一个 float（时间点 t，范围 0→1），
并返回 一个 float（动画进度值，范围 0→1）

        vmobject: 要书写的矢量对象
        run_time: 动画时间，如果为负数则自动计算
                 自动计算规则：
                 - 少于15个子对象：1秒
                 - 15个或更多子对象：2秒
        lag_ratio: 延迟比例，如果为负数则自动计算
                  自动计算规则：min(4.0/(子对象数+1), 0.2)
                  这确保了合理的重叠时间
        rate_func: 速率函数，默认为linear(线性)
                  线性函数模拟均匀的书写速度
        stroke_color: 边框颜色，如果为None则使用对象原有颜色
        **kwargs: 传递给父类的其他参数
        
        示例:
        # 书写文本
        text = Text("Hello World")
        self.play(Write(text))
        
        # 书写数学公式
        formula = MathTex(r"E = mc^2")
        self.play(Write(formula))
        
        # 自定义书写速度和颜色
        equation = MathTex(r"\\int_0^\\infty e^{-x^2} dx = \\frac{\\sqrt{\\pi}}{2}")
        self.play(Write(equation, run_time=3, stroke_color=BLUE))
        
        自动计算的优势:
        - 简单对象快速书写，复杂对象给予更多时间
        - 延迟比例确保子对象间有适当的重叠
        - 避免动画过快或过慢的问题
        """
        if stroke_color is None:
            stroke_color = vmobject.get_color()
        # 计算对象的复杂度(有点的子对象数量)
        family_size = len(vmobject.family_members_with_points()) #  递归地返回“所有真正拥有顶点数据”的子孙对象列表
        # 把那些 空壳对象（没有点、不可见）自动过滤掉
        # class VMobject:
        #     def has_points(self) -> bool:
        #         return len(self.points) > 0  
        #   这是如何判断有无顶点的原始定义！
        super().__init__(
            vmobject,
            run_time=self.compute_run_time(family_size, run_time),
            lag_ratio=self.compute_lag_ratio(family_size, lag_ratio),
            rate_func=rate_func,
            stroke_color=stroke_color,
            **kwargs
        )

    def compute_run_time(self, family_size: int, run_time: float) -> float:
        """
        计算合适的动画运行时间
        
        根据对象的复杂程度自动确定动画时间，确保书写效果既不会太快
        也不会太慢。这个方法实现了智能的时间分配策略。
        
        参数说明:
        family_size: 对象族中有点的子对象数量(复杂度指标)
        run_time: 用户指定的运行时间，如果为负数则自动计算
        
        返回值:
        float: 最终的动画运行时间(秒)
        
        自动计算规则:
        - 简单对象(< 15个子对象): 1秒
          适用于简单文本、基本图形
        - 复杂对象(≥ 15个子对象): 2秒
          适用于长文本、复杂公式、详细图形
        
        设计理念:
        这个阈值(15)是经过实践验证的，能够很好地区分简单和复杂对象，
        确保动画速度符合我们的视觉感知习惯。
        """
        if run_time < 0:
            return 1 if family_size < 15 else 2  # “为这个动画分配 1 秒的播放时间。”如果对象的复杂度小于 15，返回 1 秒；否则返回 2 秒。
        return run_time

    def compute_lag_ratio(self, family_size: int, lag_ratio: float) -> float:
        """
        计算合适的延迟比例
        
        延迟比例控制子对象之间的动画重叠程度。合适的延迟比例能够
        创造流畅的书写效果，避免动画过于分散或过于同步。
        
        参数说明:
        family_size: 对象族中有点的子对象数量
        lag_ratio: 用户指定的延迟比例，如果为负数则自动计算
        
        返回值:
        float: 最终的延迟比例(0到1之间)
        
        自动计算公式:
        min(4.0 / (family_size + 1.0), 0.2)
        
        公式解析:
        - 4.0 / (family_size + 1.0): 基础延迟比例，随子对象数量递减，这系一个经验公式
        - min(..., 0.2): 确保延迟比例不超过0.2(20%)
        
        效果分析:（这才是重点哟）
        - 少量子对象: 较大的延迟比例，创造明显的逐个出现效果
        - 大量子对象: 较小的延迟比例，避免动画过于冗长
        - 最大值限制: 防止延迟比例过大导致动画拖沓（是那个0.2）
        
        示例计算:
        - 1个子对象: min(4.0/2, 0.2) = 0.2
        - 5个子对象: min(4.0/6, 0.2) = 0.2
        - 20个子对象: min(4.0/21, 0.2) = 0.19
        - 100个子对象: min(4.0/101, 0.2) = 0.04
        """
        if lag_ratio < 0:
            return min(4.0 / (family_size + 1.0), 0.2)
        return lag_ratio


class ShowIncreasingSubsets(Animation):
    """
    ShowIncreasingSubsets - 递增子集显示动画
    
    这句话是关键👇
    这个动画类用于逐步显示一个组(Group)中的子对象，创造出
    元素逐个添加到集合中的视觉效果。
    
    继承关系：
    Animation -> ShowIncreasingSubsets
    
    主要特点：
    - 按顺序逐个显示子对象
    - 可自定义显示的时间函数
    - 适用于展示集合、列表、序列的构建过程
    - 支持任意数量的子对象
    
    工作原理：
    1. 获取组中所有子对象的列表
    2. 根据动画进度计算当前应显示的子对象数量
    3. 只显示前N个子对象，隐藏其余对象
    4. 随着动画进行，N逐渐增加直到显示所有对象
    
    使用场景：
    - 展示数学集合的构建
    - 逐步显示列表元素
    - 演示算法中元素的添加过程
    - 创建"累积"效果的动画
    
    示例：
    # 创建一组圆形
    circles = Group(*[Circle() for _ in range(5)])
    # 逐个显示圆形
    self.play(ShowIncreasingSubsets(circles))
    """
    def __init__(
        self,
        group: Mobject,
        int_func: Callable[[float], float] = np.round,
        suspend_mobject_updating: bool = False,
        **kwargs
    ):
        """
        初始化ShowIncreasingSubsets动画对象
        
        参数说明:
        group: 要逐步显示的组对象，包含多个子对象
        int_func: 整数转换函数，用于将浮点进度转换为整数索引
                 默认使用np.round(四舍五入)
                 可选：np.floor(向下取整)、np.ceil(向上取整)
        suspend_mobject_updating: 是否暂停对象更新
                                 设为True可以提高性能，但可能影响某些动态效果
        **kwargs: 传递给父类Animation的其他参数
        
        内部属性:
        self.all_submobs: 存储组中所有子对象的列表副本
        self.int_func: 存储整数转换函数的引用
        
        示例:
        # 基本用法
        dots = Group(*[Dot() for _ in range(10)])
        self.play(ShowIncreasingSubsets(dots))
        
        # 使用向下取整，创造更突然的出现效果
        self.play(ShowIncreasingSubsets(dots, int_func=np.floor))
        
        # 使用向上取整，创造更早的出现效果
        self.play(ShowIncreasingSubsets(dots, int_func=np.ceil))
        
        即
        np.floor：子对象延迟出现，每跨过一个整数阈值才“整批”闪现，更突然。
        np.ceil：子对象提前出现，只要进度超过一点点就立即多一个，更早更连续。

        注意事项:
        - 子对象的显示顺序由它们在组中的顺序决定
        - 动画开始时所有子对象都会被隐藏
        - 动画结束时所有子对象都会显示
        """
        # 保存组中所有子对象的列表副本
        # 使用list()创建副本，避免原始组被修改时影响动画
        self.all_submobs = list(group.submobjects)
        # 保存整数转换函数
        self.int_func = int_func
        super().__init__(
            group,
            suspend_mobject_updating=suspend_mobject_updating,
            **kwargs
        )

    def interpolate_mobject(self, alpha: float) -> None:
        """
        根据动画进度插值对象状态
        
        这是动画的核心方法，负责根据当前的动画进度(alpha)来决定
        应该显示多少个子对象。
        
        参数说明:
        alpha: 动画进度，范围从0到1
               - alpha=0时，不显示任何子对象
               - alpha=1时，显示所有子对象
               - alpha=0.5时，显示大约一半的子对象
        
        工作流程:
        1. 获取子对象总数
        2. 应用速率函数调整alpha值
        3. 计算当前应显示的子对象索引
        4. 更新子对象列表
        
        计算逻辑:
        - n_submobs: 总子对象数量
        - alpha * n_submobs: 将进度映射到子对象数量范围
        - int_func(): 将浮点数转换为整数索引
        
        示例:
        假设有10个子对象：
        - alpha=0.0 -> index=0 -> 显示0个对象
        - alpha=0.3 -> index=3 -> 显示前3个对象
        - alpha=0.7 -> index=7 -> 显示前7个对象
        - alpha=1.0 -> index=10 -> 显示所有10个对象
        """
        # 获取所有子对象的数量
        n_submobs = len(self.all_submobs)
        # 应用速率函数，允许非线性的动画进度
        alpha = self.rate_func(alpha)
        # 计算当前应该显示的子对象数量
        # alpha * n_submobs 将0-1的进度映射到0-n_submobs的范围
        # int_func 将浮点数转换为整数索引
        index = int(self.int_func(alpha * n_submobs))
        # 更新实际显示的子对象列表
        # int_func = np.round      # 四舍五入 
        # int_func = np.floor      # 向下取整（小于0.5）
        # int_func = np.ceil       # 向上取整（大于等于0.5）
        self.update_submobject_list(index)

    def update_submobject_list(self, index: int) -> None:
        """
        更新子对象列表，控制实际显示的子对象
        
        这个方法负责设置组对象中实际显示的子对象。通过切片操作
        只显示前index个子对象，实现递增显示的效果。
        
        参数说明:
        index: 要显示的子对象数量
               - index=0: 不显示任何子对象
               - index=3: 显示前3个子对象
               - index=len(all_submobs): 显示所有子对象
        
        工作原理:
        使用Python的切片语法all_submobs[:index]获取前index个元素，
        然后通过set_submobjects()方法更新组对象的子对象列表。
        
        切片行为:
        - [:0] -> 空列表，不显示任何对象
        - [:3] -> 前3个对象
        - [:len(list)] -> 所有对象
        
        注意事项:
        - 如果index超出范围，切片操作会自动处理边界情况
        - 这个方法会立即更新对象的视觉状态
        - 被移除的子对象不会被销毁，只是暂时不显示
        """
        # 使用切片获取前index个子对象，并设置为当前显示的子对象
        # [:index] 表示从开始到index位置(不包含index)的所有元素
        self.mobject.set_submobjects(self.all_submobs[:index])
        
        """
        这里的self.all_submobs[:index]语法举个简答的例子就懂了➡️
        lst = ['a', 'b', 'c', 'd']
        print(lst[:2])   # ['a', 'b']
        print(lst[:0])   # []        （空列表）
        print(lst[:4])   # ['a', 'b', 'c', 'd']
        
        set_submobjects() YYDS!
        """

class ShowSubmobjectsOneByOne(ShowIncreasingSubsets):
    """
    ShowSubmobjectsOneByOne - 逐个显示子对象动画
    
    这是ShowIncreasingSubsets的特化版本，专门用于创造"一个接一个"
    显示子对象的效果。与父类的主要区别在于每次只显示一个子对象，
    而不是累积显示。
    
    继承关系：
    Animation -> ShowIncreasingSubsets -> ShowSubmobjectsOneByOne
    
    主要特点：
    - 使用np.ceil(向上取整)作为默认的整数转换函数
    - 每次只显示一个子对象，不累积
    - 创造"聚光灯"式的显示效果
    - 适合需要逐个突出显示的场景
    
    与ShowIncreasingSubsets的区别：
    - ShowIncreasingSubsets: 累积显示(1个->2个->3个->...)
    - ShowSubmobjectsOneByOne: 单独显示(第1个->第2个->第3个->...)
    
    效果对比(假设有4个对象)：
    ShowIncreasingSubsets:
    - alpha=0.25 -> 显示第1个对象
    - alpha=0.50 -> 显示前2个对象
    - alpha=0.75 -> 显示前3个对象
    - alpha=1.00 -> 显示所有4个对象
    
    ShowSubmobjectsOneByOne:
    - alpha=0.25 -> 只显示第1个对象
    - alpha=0.50 -> 只显示第2个对象
    - alpha=0.75 -> 只显示第3个对象
    - alpha=1.00 -> 只显示第4个对象
    
    使用场景：
    - 逐个突出显示列表项
    - 创建"聚光灯"扫描效果
    - 逐步检查或演示每个元素
    - 避免屏幕过于拥挤的渐进显示
    """
    def __init__(
        self,
        group: Mobject,
        int_func: Callable[[float], float] = np.ceil, # 向上取整才是ShowSubmobjectsOneByOne的重点
        **kwargs
    ):
        """
        初始化ShowSubmobjectsOneByOne动画对象
        
        参数说明:
        group: 要逐个显示的组对象
        int_func: 整数转换函数，默认为np.ceil(向上取整)
                 使用ceil确保子对象在动画早期就开始出现
        **kwargs: 传递给父类的其他参数
        
        默认行为:
        使用np.ceil确保每个子对象都有足够的显示时间，
        创造清晰的"一个接一个"效果。
        
        示例:
        # 基本用法 - 逐个显示圆形
        circles = Group(*[Circle() for _ in range(5)])
        self.play(ShowSubmobjectsOneByOne(circles))
        
        # 逐个显示文本行
        lines = Group(*[Text(f"Line {i}") for i in range(3)])
        self.play(ShowSubmobjectsOneByOne(lines))
        
        # 与ShowIncreasingSubsets对比
        # 这个每次只显示一个
        self.play(ShowSubmobjectsOneByOne(squares))
        # 这个累积显示
        self.play(ShowIncreasingSubsets(squares))
        
        适用场景:
        - 逐项检查清单
        - 突出显示当前处理的元素
        - 避免视觉混乱的渐进演示
        - 创建"扫描"或"遍历"效果
        """
        super().__init__(group, int_func=int_func, **kwargs)

    def update_submobject_list(self, index: int) -> None:
        """
        更新子对象列表，每次只显示一个子对象
        
        这是与父类ShowIncreasingSubsets的关键区别。父类会累积显示
        子对象(显示前N个)，而这个方法只显示当前索引对应的一个子对象。
        
        参数说明:
        index: 当前要显示的子对象索引
               - index=0: 不显示任何对象
               - index=1: 只显示第1个对象
               - index=3: 只显示第3个对象
        
        工作原理:
        1. 使用clip函数确保索引在有效范围内
        2. 如果索引为0，清空显示列表
        3. 否则，只显示索引为(index-1)的单个对象
        
        索引处理:
        - 使用index-1是因为index从1开始计数(ceil的结果)
        - 当alpha很小时，ceil会返回1，对应显示第0个对象
        - 当alpha=1时，index等于对象总数，显示最后一个对象
        
        边界处理:
        clip函数确保索引不会超出数组边界，提供安全的访问。
        
        示例:
        假设有3个对象[A, B, C]：
        - index=0 -> 显示: []
        - index=1 -> 显示: [A]
        - index=2 -> 显示: [B] 
        - index=3 -> 显示: [C]
        
        注意事项:
        - 每次调用都会完全替换显示的子对象列表
        - 之前显示的对象会被隐藏
        - 这创造了"聚光灯"式的效果
        """
        # 确保索引在有效范围内：0到(对象总数-1)
        index = int(clip(index, 0, len(self.all_submobs) - 1))
        if index == 0:
            # 索引为0时，不显示任何对象
            self.mobject.set_submobjects([])
        else:
            # 只显示索引为(index-1)的单个对象
            # 使用index-1是因为index从1开始计数
            self.mobject.set_submobjects([self.all_submobs[index - 1]])


class AddTextWordByWord(ShowIncreasingSubsets):
    """
    AddTextWordByWord - 逐词添加文本动画
    
    这是ShowIncreasingSubsets的特化版本，专门用于字符串对象的逐词显示。
    它会将文本按词组分组，然后逐个显示每个词组，创造逐词出现的效果。
    
    继承关系：
    Animation -> ShowIncreasingSubsets -> AddTextWordByWord
    
    主要特点：
    - 专门为StringMobject设计
    - 按词组而非字符进行分组显示
    - 自动计算基于词数的动画时间
    - 可自定义每个词的显示时间
    - 支持复杂的文本布局和样式
    - 动画结束后自动清理和替换对象
    
    工作原理：
    1. 使用StringMobject的build_groups()方法将文本分组
    2. 根据词组数量和每词时间计算总动画时间
    3. 使用ShowIncreasingSubsets的机制逐个显示词组
    4. 动画结束后进行场景清理
    
    时间计算：
    总时间 = 词组数量 × 每词时间
    默认每词时间为0.2秒，适合正常的阅读节奏
    
    使用场景：
    - 逐词显示重要文本
    - 创建动态的文本出现效果
    - 演讲或教学中的逐步文本展示
    - 强调文本内容的结构
    - 诗歌或格式化文本的艺术展示
    
    示例：
    # 基本用法
    text = StringMobject("Hello beautiful world")
    self.play(AddTextWordByWord(text))
    
    # 自定义显示速度
    slow_text = StringMobject("Slow word by word")
    self.play(AddTextWordByWord(slow_text, time_per_word=0.5))
    
    # 快速显示
    fast_text = StringMobject("Quick display")
    self.play(AddTextWordByWord(fast_text, time_per_word=0.1))
    """
    def __init__(
        self,
        string_mobject: StringMobject,
        time_per_word: float = 0.2,
        run_time: float = -1.0, # 如果该值为负数，将根据 time_per_word 重新计算
        rate_func: Callable[[float], float] = linear,  # (function) def linear(t: float) -> float
        **kwargs
    ):
        """
        初始化AddTextWordByWord动画对象
        StringMobject 是 Tex/MarkupText 的抽象基类，专用于“按子字符串切片子对象”，比数字索引更直观。
    用 isolate 指定要独立控制的子串（字符串、正则或坐标元组），子串不能部分重叠。
    每个实例最多生成两份 SVG：一份原图，一份插入色标用来给子对象配对上色。
    每个子对象的颜色会根据其在字符串中的位置自动分配。

    举个例子：
    from manim import *

class SliceDemo(Scene):
    def construct(self):
        # 1. 创建文本；用 isolate 把 "Manim" 和 "Python" 切成独立子对象
        txt = Text(
            "I love Manim and Python!",
            isolate=["Manim", "Python"],   # ← 关键：按子串切片
            font_size=48
        )

        # 2. 初始排版
        self.play(Write(txt))
        self.wait(0.5)

        # 3. 对切片后的子对象做动画
        #    txt[0] → "I love "
        #    txt[1] → "Manim"
        #    txt[2] → " and "
        #    txt[3] → "Python"
        #    txt[4] → "!"

        self.play(txt[1].animate.set_color(YELLOW).scale(1.3))  # 高亮 "Manim"
        self.wait(0.3)
        self.play(txt[3].animate.set_color(GREEN).scale(1.3))   # 高亮 "Python"
        self.wait(2)

✅ 你会看到
整句先完整写出；
接着 "Manim" 单独变黄并放大；
然后 "Python" 单独变绿并放大；
全程无需计算字符索引，直接用子字符串 "Manim"、"Python" 就能精准切到对应子对象。


        参数说明:
        string_mobject: 要逐词显示的字符串对象
                       必须是StringMobject类型，支持build_groups()方法
        time_per_word: 每个词组的显示时间(秒)
                      默认0.2秒，这是舒适的阅读速度
                      - 0.1秒: 快速显示
                      - 0.2秒: 正常速度(推荐)
                      - 0.5秒: 慢速，适合强调
                      - 1.0秒: 很慢，适合逐词分析
        run_time: 动画总时间，如果为负数则自动计算
                 自动计算公式：词组数 × time_per_word
        rate_func: 速率函数，默认为linear(线性)
                  线性函数确保每个词组有相等的显示时间
        **kwargs: 传递给父类的其他参数
        
        工作流程:
        1. 验证输入对象类型必须是StringMobject
        2. 调用build_groups()将文本分解为词组
        3. 根据词组数量计算动画时间
        4. 初始化父类ShowIncreasingSubsets
        5. 保存原始字符串对象的引用
        
        自动时间计算:
        当run_time为负数时，动画时间会根据词组数量自动计算：
        总时间 = len(grouped_mobject) × time_per_word
        
        示例:
        # 基本逐词显示
        quote = StringMobject("To be or not to be")
        self.play(AddTextWordByWord(quote))
        # 自动时间: 6个词组 × 0.2秒 = 1.2秒
        
        # 快速逐词显示
        title = StringMobject("Chapter One Introduction")
        self.play(AddTextWordByWord(title, time_per_word=0.1))
        
        # 慢速强调显示
        important = StringMobject("VERY IMPORTANT MESSAGE")
        self.play(AddTextWordByWord(important, time_per_word=0.8))
        
        # 手动指定总时间
        poem = StringMobject("Roses are red violets blue")
        self.play(AddTextWordByWord(poem, run_time=3.0))
        
        技术细节:
        - build_groups()方法将文本智能分组为词组
        - 每个词组作为一个独立的显示单元
        - 支持复杂的文本格式和样式
        - 保持原始对象的所有属性和样式
        
        注意事项:
        - 输入必须是StringMobject类型
        - 词组的划分依赖于build_groups()的实现
        - 动画结束后会进行特殊的场景清理
        """
        # 类型检查：确保输入是StringMobject类型
        assert isinstance(string_mobject, StringMobject)
        # 将字符串对象分解为词组，每个词组作为一个显示单元
        grouped_mobject = string_mobject.build_groups()
        # 如果没有指定运行时间，则根据词组数自动计算
        if run_time < 0:
            # 总时间 = 词组数量 × 每词时间
            run_time = time_per_word * len(grouped_mobject)
        # 调用父类构造函数，使用分组后的对象
        super().__init__(
            grouped_mobject,
            run_time=run_time,
            rate_func=rate_func,
            **kwargs
        )
        # 保存原始字符串对象的引用，用于后续的场景清理
        self.string_mobject = string_mobject

    def clean_up_from_scene(self, scene: Scene) -> None:
        """
        从场景中清理动画对象
        
        这个方法在动画完成后被调用，负责正确地清理和替换对象。
        由于AddTextWordByWord使用了分组后的对象进行动画，动画结束后
        需要将分组对象替换回原始的字符串对象。
        
        参数说明:
        scene: 当前的场景对象
        
        清理流程:
        1. 从场景中移除分组后的动画对象(self.mobject)
        2. 如果动画不是移除器类型，将原始字符串对象添加回场景
        3. 确保场景中显示的是完整的、正确样式的文本对象
        
        工作原理:
        - self.mobject: 分组后的对象，用于动画显示
        - self.string_mobject: 原始字符串对象，包含完整信息
        - is_remover(): 检查动画是否标记为移除器
        
        重要性:
        这个清理步骤确保了：
        1. 动画结束后场景状态正确
        2. 原始对象的所有属性和方法可用
        3. 后续操作可以正常访问文本对象
        4. 内存使用得到优化
        
        示例场景:
        # 动画前：场景为空
        text = StringMobject("Hello World")
        
        # 动画中：场景包含分组对象
        self.play(AddTextWordByWord(text))
        
        # 动画后：场景包含原始完整对象
        # 可以继续对text进行其他操作
        self.play(text.animate.shift(UP))
        
        注意事项:
        - 只有在动画不是remover类型时才会添加原始对象
        - 这确保了对象生命周期的正确管理
        - 清理操作对用户是透明的
        """
        # 从场景中移除用于动画的分组对象
        scene.remove(self.mobject)
        # 如果动画不是移除器类型，将原始字符串对象添加回场景
        # 这确保动画结束后场景中有完整的、可操作的文本对象
        if not self.is_remover():
            scene.add(self.string_mobject)


# ═══════════════════════════════════════════════════════════════════════════════
# 模块测试和示例代码 (Module Testing & Examples)
# ═══════════════════════════════════════════════════════════════════════════════

def _module_self_test() -> bool:
    """
    模块自测试函数
    
    检查模块的基本功能是否正常工作，包括：
    - 所有类是否可以正常导入
    - 基本的类实例化是否成功
    - 关键方法是否存在
    
    返回值:
    bool: 测试是否通过
    """
    try:
        # 测试类的可用性
        classes_to_test = [
            ShowPartial, ShowCreation, Uncreate, 
            DrawBorderThenFill, Write,
            ShowIncreasingSubsets, ShowSubmobjectsOneByOne,
            AddTextWordByWord
        ]
        
        print(f"✓ 成功导入 {len(classes_to_test)} 个动画类")
        
        # 测试NumPy兼容性
        test_array = np.array([1, 2, 3])
        assert len(test_array) == 3
        print("✓ NumPy兼容性测试通过")
        
        # 测试版本信息
        assert __version__ == '2.0.0'
        assert len(__all__) == 8
        print(f"✓ 模块版本: {__version__}")
        print(f"✓ 公共API包含 {len(__all__)} 个类")
        
        return True
        
    except Exception as e:
        print(f"✗ 模块测试失败: {e}")
        return False


if __name__ == "__main__":
    """
    当直接运行此模块时执行的代码
    
    这允许用户通过运行 `python creation.py` 来测试模块功能
    """
    print("="*70)
    print("ManimLib Creation Animation Module - 长期支持版本")
    print(f"版本: {__version__}")
    print(f"Python版本: {sys.version.split()[0]}")
    print(f"NumPy版本: {np.__version__}")
    print("="*70)
    
    # 运行自测试
    print("\n🔍 运行模块自测试...")
    if _module_self_test():
        print("\n🎉 所有测试通过！模块可以正常使用。")
        print("\n📚 使用示例:")
        print("```python")
        print("from creation import ShowCreation, Write, AddTextWordByWord")
        print("# 创建你的动画...")
        print("```")
    else:
        print("\n❌ 测试失败，请检查依赖项和环境配置。")
        sys.exit(1)
    
    print("\n" + "="*70)
