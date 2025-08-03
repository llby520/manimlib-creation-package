#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ManimLib Creation Package - 自动安装和启动脚本
版本: 1.0.0
作者: ManimLib Community

这个脚本会自动检查和安装所需的依赖，确保项目可以正常运行。
如果缺少manimlib，会自动尝试安装manim作为替代。
"""

import sys
import subprocess
import importlib
import os
from pathlib import Path
from typing import List, Optional, Tuple

# 颜色输出支持
class Colors:
    """终端颜色代码"""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def print_colored(text: str, color: str = Colors.WHITE) -> None:
    """打印彩色文本"""
    print(f"{color}{text}{Colors.END}")

def print_header(text: str) -> None:
    """打印标题"""
    print_colored(f"\n{'='*60}", Colors.CYAN)
    print_colored(f"{text:^60}", Colors.BOLD + Colors.CYAN)
    print_colored(f"{'='*60}", Colors.CYAN)

def print_step(step: str, status: str = "INFO") -> None:
    """打印步骤信息"""
    color_map = {
        "INFO": Colors.BLUE,
        "SUCCESS": Colors.GREEN,
        "WARNING": Colors.YELLOW,
        "ERROR": Colors.RED
    }
    color = color_map.get(status, Colors.WHITE)
    print_colored(f"[{status}] {step}", color)

def check_python_version() -> bool:
    """检查Python版本"""
    print_step("检查Python版本...")
    if sys.version_info < (3, 8):
        print_step(f"Python版本过低: {sys.version_info.major}.{sys.version_info.minor}", "ERROR")
        print_step("需要Python 3.8或更高版本", "ERROR")
        return False
    print_step(f"Python版本: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}", "SUCCESS")
    return True

def run_command(cmd: List[str], capture_output: bool = True) -> Tuple[bool, str]:
    """运行命令并返回结果"""
    try:
        if capture_output:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return True, result.stdout
        else:
            result = subprocess.run(cmd, check=True)
            return True, ""
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr if hasattr(e, 'stderr') and e.stderr else str(e)
        return False, error_msg
    except FileNotFoundError:
        return False, f"命令未找到: {' '.join(cmd)}"

def check_package_installed(package_name: str) -> bool:
    """检查包是否已安装"""
    try:
        importlib.import_module(package_name)
        return True
    except ImportError:
        return False

def install_package(package_name: str, pip_name: Optional[str] = None) -> bool:
    """安装Python包"""
    pip_name = pip_name or package_name
    print_step(f"正在安装 {pip_name}...")
    
    # 尝试使用pip安装
    success, output = run_command([sys.executable, "-m", "pip", "install", pip_name], capture_output=False)
    
    if success:
        print_step(f"{pip_name} 安装成功", "SUCCESS")
        return True
    else:
        print_step(f"{pip_name} 安装失败", "ERROR")
        return False

def check_and_install_dependencies() -> bool:
    """检查并安装依赖"""
    print_header("检查和安装依赖")
    
    # 基础依赖
    basic_deps = [
        ("numpy", "numpy>=1.20.0"),
        ("typing_extensions", "typing-extensions>=4.0.0")
    ]
    
    # 检查基础依赖
    for package, pip_name in basic_deps:
        if not check_package_installed(package):
            print_step(f"缺少依赖: {package}")
            if not install_package(package, pip_name):
                return False
        else:
            print_step(f"依赖已安装: {package}", "SUCCESS")
    
    # 检查manimlib
    if check_package_installed("manimlib"):
        print_step("manimlib 已安装", "SUCCESS")
        return True
    
    # 尝试安装manim作为替代
    print_step("未找到 manimlib，尝试安装 manim 作为替代", "WARNING")
    
    # 尝试不同的manim安装选项
    manim_options = [
        "manim",
        "manimce",
        "manimgl"
    ]
    
    for manim_pkg in manim_options:
        print_step(f"尝试安装 {manim_pkg}...")
        if install_package("manim", manim_pkg):
            print_step(f"{manim_pkg} 安装成功，可以作为 manimlib 的替代", "SUCCESS")
            return True
    
    # 如果都失败了，提供手动安装指导
    print_step("自动安装失败，请手动安装 manimlib 或 manim", "WARNING")
    print_colored("\n手动安装选项:", Colors.YELLOW)
    print_colored("1. pip install manim", Colors.WHITE)
    print_colored("2. pip install manimce", Colors.WHITE)
    print_colored("3. pip install manimgl", Colors.WHITE)
    print_colored("4. 从源码安装: https://github.com/3b1b/manim", Colors.WHITE)
    
    return False

def setup_project_structure() -> bool:
    """设置项目结构"""
    print_header("设置项目结构")
    
    current_dir = Path.cwd()
    
    # 创建必要的目录
    directories = [
        "output",
        "media",
        "media/images",
        "media/videos",
        "media/texts",
        "logs",
        "examples"
    ]
    
    for dir_name in directories:
        dir_path = current_dir / dir_name
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
            print_step(f"创建目录: {dir_name}", "SUCCESS")
        else:
            print_step(f"目录已存在: {dir_name}", "INFO")
    
    return True

def create_example_script() -> bool:
    """创建示例脚本"""
    print_header("创建示例脚本")
    
    example_content = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ManimLib Creation Package - 示例脚本
这个脚本演示了如何使用 creation 模块创建动画
"""

try:
    # 尝试导入 manimlib
    from manimlib import *
    print("✅ 使用 manimlib")
except ImportError:
    try:
        # 如果 manimlib 不可用，尝试使用 manim
        from manim import *
        print("✅ 使用 manim 作为替代")
    except ImportError:
        print("❌ 未找到 manimlib 或 manim，请先安装")
        exit(1)

# 导入我们的 creation 模块
try:
    import creation
    print("✅ creation 模块导入成功")
except ImportError as e:
    print(f"❌ creation 模块导入失败: {e}")
    exit(1)

class ExampleScene(Scene):
    """示例场景"""
    
    def construct(self):
        # 创建文本
        title = Text("ManimLib Creation Demo", font_size=48)
        subtitle = Text("动画创建模块演示", font_size=24)
        
        # 使用 creation 模块的动画
        self.play(creation.Write(title))
        self.wait(1)
        
        subtitle.next_to(title, DOWN, buff=0.5)
        self.play(creation.Write(subtitle))
        self.wait(1)
        
        # 创建几何图形
        circle = Circle(radius=1, color=BLUE)
        square = Square(side_length=2, color=RED)
        
        # 使用不同的创建动画
        self.play(creation.ShowCreation(circle))
        self.wait(0.5)
        
        square.next_to(circle, RIGHT, buff=1)
        self.play(creation.DrawBorderThenFill(square))
        self.wait(1)
        
        # 清理
        self.play(
            creation.Uncreate(title),
            creation.Uncreate(subtitle),
            creation.Uncreate(circle),
            creation.Uncreate(square)
        )
        self.wait(1)

if __name__ == "__main__":
    # 运行场景
    print("\n🎬 开始渲染示例动画...")
    print("如果这是第一次运行，可能需要一些时间来设置环境")
    
    try:
        # 这里可以添加场景渲染代码
        print("\n✅ 示例脚本准备就绪")
        print("要渲染动画，请运行: manim example_scene.py ExampleScene")
    except Exception as e:
        print(f"\n❌ 运行示例时出错: {e}")
'''
    
    example_path = Path("examples/example_scene.py")
    try:
        with open(example_path, "w", encoding="utf-8") as f:
            f.write(example_content)
        print_step(f"创建示例脚本: {example_path}", "SUCCESS")
        return True
    except Exception as e:
        print_step(f"创建示例脚本失败: {e}", "ERROR")
        return False

def test_creation_module() -> bool:
    """测试 creation 模块"""
    print_header("测试 Creation 模块")
    
    try:
        import creation
        print_step("导入 creation 模块", "SUCCESS")
        
        # 运行自测试
        if hasattr(creation, '_module_self_test'):
            creation._module_self_test()
            print_step("模块自测试通过", "SUCCESS")
        else:
            print_step("模块自测试函数不存在", "WARNING")
        
        return True
    except Exception as e:
        print_step(f"测试失败: {e}", "ERROR")
        return False

def create_startup_guide() -> bool:
    """创建启动指南"""
    print_header("创建启动指南")
    
    guide_content = '''# ManimLib Creation Package - 启动指南

## 🚀 快速开始

### 1. 环境检查
运行自动设置脚本：
```bash
python auto_setup.py
```

### 2. 运行示例
```bash
cd examples
python example_scene.py
```

### 3. 渲染动画
```bash
# 使用 manimlib
manim example_scene.py ExampleScene

# 或使用 manim
manim -pql example_scene.py ExampleScene
```

## 📚 模块使用

### 导入模块
```python
import creation

# 或导入特定类
from creation import ShowCreation, Write, DrawBorderThenFill
```

### 基本动画
```python
# 创建显示动画
self.play(creation.ShowCreation(my_object))

# 书写动画
self.play(creation.Write(text_object))

# 先画边框后填充
self.play(creation.DrawBorderThenFill(shape))

# 反向创建（消失）
self.play(creation.Uncreate(my_object))
```

### 高级动画
```python
# 逐个显示子对象
self.play(creation.ShowSubmobjectsOneByOne(group))

# 逐词显示文本
self.play(creation.AddTextWordByWord(long_text))

# 累积显示子集
self.play(creation.ShowIncreasingSubsets(object_list))
```

## 🔧 故障排除

### 常见问题

1. **ImportError: No module named 'manimlib'**
   - 运行 `python auto_setup.py` 自动安装
   - 或手动安装: `pip install manim`

2. **编码错误**
   - 确保文件使用 UTF-8 编码
   - 设置环境变量: `PYTHONIOENCODING=utf-8`

3. **渲染失败**
   - 检查 FFmpeg 是否安装
   - 检查输出目录权限

### 获取帮助

- GitHub Issues: https://github.com/llby520/manimlib-creation-package/issues
- 文档: https://github.com/llby520/manimlib-creation-package/wiki
- 示例: examples/ 目录

## 📦 项目结构

```
creation_package/
├── creation.py              # 核心模块
├── auto_setup.py           # 自动安装脚本
├── examples/               # 示例代码
│   └── example_scene.py    # 基础示例
├── output/                 # 渲染输出
├── media/                  # 媒体文件
├── logs/                   # 日志文件
└── STARTUP_GUIDE.md        # 本文件
```

## 🎯 下一步

1. 查看 `examples/example_scene.py` 了解基本用法
2. 阅读 `creation.py` 中的详细文档
3. 尝试创建自己的动画场景
4. 参考 ManimLib 官方文档学习更多功能

祝您使用愉快！🎉
'''
    
    guide_path = Path("STARTUP_GUIDE.md")
    try:
        with open(guide_path, "w", encoding="utf-8") as f:
            f.write(guide_content)
        print_step(f"创建启动指南: {guide_path}", "SUCCESS")
        return True
    except Exception as e:
        print_step(f"创建启动指南失败: {e}", "ERROR")
        return False

def main() -> int:
    """主函数"""
    print_header("ManimLib Creation Package 自动设置")
    print_colored("这个脚本将帮助您设置完整的开发环境\n", Colors.CYAN)
    
    # 检查步骤
    steps = [
        ("检查Python版本", check_python_version),
        ("检查和安装依赖", check_and_install_dependencies),
        ("设置项目结构", setup_project_structure),
        ("创建示例脚本", create_example_script),
        ("测试Creation模块", test_creation_module),
        ("创建启动指南", create_startup_guide)
    ]
    
    success_count = 0
    total_steps = len(steps)
    
    for step_name, step_func in steps:
        try:
            if step_func():
                success_count += 1
            else:
                print_step(f"{step_name} 失败", "ERROR")
        except Exception as e:
            print_step(f"{step_name} 出现异常: {e}", "ERROR")
    
    # 总结
    print_header("设置完成")
    print_colored(f"成功完成: {success_count}/{total_steps} 步骤", Colors.GREEN if success_count == total_steps else Colors.YELLOW)
    
    if success_count == total_steps:
        print_colored("\n🎉 所有设置已完成！", Colors.GREEN)
        print_colored("\n下一步:", Colors.CYAN)
        print_colored("1. 查看 STARTUP_GUIDE.md 了解使用方法", Colors.WHITE)
        print_colored("2. 运行示例: python examples/example_scene.py", Colors.WHITE)
        print_colored("3. 开始创建您的动画！", Colors.WHITE)
        return 0
    else:
        print_colored("\n⚠️  部分设置未完成，请检查错误信息", Colors.YELLOW)
        print_colored("您仍然可以尝试使用已安装的组件", Colors.WHITE)
        return 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print_colored("\n\n用户中断设置过程", Colors.YELLOW)
        sys.exit(1)
    except Exception as e:
        print_colored(f"\n\n设置过程中出现未预期的错误: {e}", Colors.RED)
        sys.exit(1)