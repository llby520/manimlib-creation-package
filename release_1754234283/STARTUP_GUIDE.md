# ManimLib Creation Package - 启动指南

## 🚀 快速开始

### 方法一：一键启动（推荐）

```bash
# 下载并解压发布包后，运行快速开始脚本
python quick_start.py
```

### 方法二：手动安装

```bash
# 1. 运行自动设置
python auto_setup.py

# 2. 验证安装
python test_installation.py

# 3. 开始使用
python -c "import creation; print('安装成功！')"
```

## 📋 系统要求

- **Python**: 3.8+ （推荐 3.9+）
- **操作系统**: Windows, macOS, Linux
- **内存**: 最少 2GB RAM
- **依赖**: NumPy 1.19+

## 🔧 安装选项

### 选项1：PyPI 安装（推荐）

```bash
pip install manimlib-creation
```

### 选项2：从源码安装

```bash
# 克隆仓库
git clone https://github.com/llby520/manimlib-creation-package.git
cd manimlib-creation

# 安装
pip install -e .
```

### 选项3：Conda 安装

```bash
# 构建本地包
conda-build creationbuild_package

# 安装
conda install --use-local manimlib-creation
```

## 🎯 Manim 依赖安装

本包支持多种 Manim 实现，会自动检测并安装合适的版本：

### 自动安装（推荐）

```bash
# 运行依赖管理器
python dependency_manager.py
```

### 手动安装选项

```bash
# 选项1：ManimCE（社区版，推荐）
pip install manim

# 选项2：ManimGL（OpenGL版本）
pip install manimgl

# 选项3：原版 ManimLib
pip install manimlib
```

## 📖 基本使用

### 导入模块

```python
import creation
from creation import ShowCreation, Write, Uncreate
```

### 简单示例

```python
# 创建一个简单的动画
from creation import ShowCreation

# 假设你有一个 mobject
# animation = ShowCreation(your_mobject)
# self.play(animation)
```

### 完整示例

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例：使用 Creation 模块创建动画
"""

try:
    # 尝试导入 manim
    from manim import *
except ImportError:
    try:
        from manimlib import *
    except ImportError:
        print("请先安装 manim 或 manimlib")
        exit(1)

# 导入 creation 模块
import creation
from creation import ShowCreation, Write, Uncreate

class CreationExample(Scene):
    def construct(self):
        # 创建文本
        title = Text("ManimLib Creation Package")
        
        # 使用 Write 动画
        self.play(Write(title))
        self.wait(1)
        
        # 创建圆形
        circle = Circle(radius=2, color=BLUE)
        
        # 使用 ShowCreation 动画
        self.play(ShowCreation(circle))
        self.wait(1)
        
        # 使用 Uncreate 动画
        self.play(Uncreate(circle))
        self.play(Uncreate(title))
```

## 🧪 测试和验证

### 运行测试套件

```bash
# 完整测试
python test_installation.py

# 快速验证
python -c "import creation; creation._module_self_test()"
```

### 检查依赖

```bash
# 检查所有依赖
python dependency_manager.py --check

# 检查特定包
python -c "import numpy, creation; print('所有依赖正常')"
```

## 🔍 故障排除

### 常见问题

#### 1. 导入错误

```bash
# 问题：ImportError: No module named 'creation'
# 解决：确保正确安装
pip install -e .
```

#### 2. Manim 未找到

```bash
# 问题：No module named 'manim'
# 解决：安装 manim
pip install manim
```

#### 3. NumPy 版本问题

```bash
# 问题：NumPy 版本不兼容
# 解决：升级 NumPy
pip install --upgrade numpy>=1.19
```

#### 4. 编码问题（Windows）

```bash
# 设置环境变量
set PYTHONIOENCODING=utf-8
python your_script.py
```

### 获取帮助

```python
# 查看模块信息
import creation
help(creation)

# 查看特定类
help(creation.ShowCreation)

# 运行自测试
creation._module_self_test()
```

## 📁 项目结构

```
manimlib-creation/
├── creation.py              # 核心模块
├── auto_setup.py           # 自动安装脚本
├── dependency_manager.py   # 依赖管理器
├── quick_start.py          # 快速开始脚本
├── test_installation.py    # 安装验证脚本
├── README.md               # 项目说明
├── STARTUP_GUIDE.md        # 本文档
├── LICENSE                 # 许可证
├── pyproject.toml          # 项目配置
├── requirements_creation.txt # 依赖列表
├── setup_creation.py       # 安装脚本
├── creationbuild_package/  # Conda 构建包
│   ├── meta.yaml
│   ├── build.sh
│   └── environment.yml
└── examples/               # 示例代码
    └── basic_example.py
```

## 🚀 高级用法

### 自定义动画

```python
from creation import ShowCreation

# 自定义参数
animation = ShowCreation(
    mobject,
    run_time=2.0,
    rate_func=smooth
)
```

### 组合动画

```python
from creation import ShowCreation, Write

# 同时播放多个动画
self.play(
    ShowCreation(circle),
    Write(text),
    run_time=3
)
```

### 性能优化

```python
# 对于复杂对象，使用合适的动画类
from creation import ShowSubmobjectsOneByOne

# 逐个显示子对象
animation = ShowSubmobjectsOneByOne(complex_mobject)
```

## 📚 更多资源

- **GitHub 仓库**: [manimlib-creation](https://github.com/llby520/manimlib-creation-package)
- **文档**: 查看 README.md
- **示例**: examples/ 目录
- **问题反馈**: GitHub Issues

## 🤝 贡献

欢迎贡献代码！请查看 CONTRIBUTING.md 了解详情。

## 📄 许可证

本项目采用 MIT 许可证。详见 LICENSE 文件。

---

**祝您使用愉快！** 🎉

如有问题，请查看故障排除部分或提交 Issue。