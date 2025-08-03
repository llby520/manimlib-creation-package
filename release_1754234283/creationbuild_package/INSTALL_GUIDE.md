# ManimLib Creation 安装指南

## 📦 项目信息

- **项目名称**: ManimLib Creation Animation Module
- **GitHub仓库**: https://github.com/llby520/manimLibfuke
- **版本**: v2.0.0 (长期支持版本)
- **许可证**: MIT License

## 🚀 安装方法

### 方法一：直接从GitHub安装 (推荐)

```bash
# 1. 克隆仓库
git clone https://github.com/llby520/manimLibfuke.git

# 2. 进入项目目录
cd manimLibfuke/creation_package/creationbuild_package

# 3. 安装依赖
pip install -r requirements_creation.txt

# 4. 安装包
pip install .
```

### 方法二：开发模式安装

如果您想要修改代码或参与开发：

```bash
# 1. 克隆仓库
git clone https://github.com/llby520/manimLibfuke.git

# 2. 进入项目目录
cd manimLibfuke/creation_package/creationbuild_package

# 3. 开发模式安装
pip install -e .
```

### 方法三：使用pip直接安装 (如果已发布到PyPI)

```bash
# 从PyPI安装 (待发布)
pip install manimlib-creation
```

## 🔧 系统要求

### 必需环境
- **Python**: 3.8 或更高版本
- **NumPy**: 1.19 或更高版本
- **ManimLib**: 已安装的ManimLib环境

### 依赖包
所有依赖包都在 `requirements_creation.txt` 中定义，安装时会自动处理。

## ✅ 安装验证

### 1. 运行自测试
```bash
python -c "import creation; creation._module_self_test()"
```

### 2. 基本功能测试
```python
# 测试导入
from creation import ShowCreation, Write, AddTextWordByWord
print("✅ 导入成功！")

# 测试基本功能
from creation import _module_self_test
_module_self_test()
```

### 3. 运行演示脚本
```bash
# 运行中文输出演示
python 中文输出文档/Demo_ShowSubmobjectsOneByOne.py

# 运行编码测试
python 中文输出文档/test_chinese_encoding.py
```

## 🎯 快速开始

安装完成后，您可以在Manim场景中使用：

```python
from manimlib import *
from creation import ShowCreation, Write, AddTextWordByWord

class MyScene(Scene):
    def construct(self):
        # 创建显示动画
        circle = Circle()
        self.play(ShowCreation(circle))
        
        # 书写动画
        text = Text("Hello ManimLib!")
        self.play(Write(text))
        
        # 逐词显示
        quote = Text("数学之美，动画之魅")
        self.play(AddTextWordByWord(quote))
```

## 🐛 常见问题

### Q: 安装时出现权限错误
A: 尝试使用 `pip install --user .` 或在虚拟环境中安装。

### Q: 导入时出现ModuleNotFoundError
A: 确保已正确安装ManimLib，并且Python路径配置正确。

### Q: 运行时出现pkg_resources警告
A: 这些警告已被自动过滤，不影响功能使用。

### Q: 中文显示异常
A: 运行 `python 中文输出文档/test_chinese_encoding.py` 检测编码环境。

## 🔄 更新和卸载

### 更新到最新版本
```bash
# 拉取最新代码
cd manimLibfuke
git pull origin main

# 重新安装
cd creation_package/creationbuild_package
pip install --upgrade .
```

### 卸载
```bash
pip uninstall manimlib-creation
```

## 📞 获取帮助

如果遇到安装问题：

1. **查看文档**: https://github.com/llby520/manimLibfuke/wiki
2. **提交Issue**: https://github.com/llby520/manimLibfuke/issues
3. **查看发布页面**: https://github.com/llby520/manimLibfuke/releases
4. **运行诊断**: `python creation.py` (自测试模式)

## 🎉 安装成功！

恭喜您成功安装了ManimLib Creation模块！现在您可以：

- ✅ 使用现代化的动画创建功能
- ✅ 享受完整的中文支持
- ✅ 体验长期稳定的API
- ✅ 参与开源社区贡献

开始您的数学动画创作之旅吧！🚀