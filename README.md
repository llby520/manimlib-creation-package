# 🎬 ManimLib Creation Package v1.0.0

[![CI/CD](https://github.com/llby520/manimlib-creation-package/actions/workflows/python-package.yml/badge.svg)](https://github.com/llby520/manimlib-creation-package/actions/workflows/python-package.yml)
[![Conda CI/CD](https://github.com/llby520/manimlib-creation-package/actions/workflows/python-package-conda.yml/badge.svg)](https://github.com/llby520/manimlib-creation-package/actions/workflows/python-package-conda.yml)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/manimlib-creation.svg)](https://badge.fury.io/py/manimlib-creation)
[![Release](https://img.shields.io/github/v/release/llby520/manimlib-creation-package)](https://github.com/llby520/manimlib-creation-package/releases)

**ManimLib Creation Package** - 专为 ManimGL 设计的高级动画创建工具包，提供强大的动画类库、完整的CI/CD支持和优化的开发体验。

> 🎉 **v1.0.0 正式发布！** 这是首个稳定版本，包含完整的动画类库、GitHub Actions CI/CD支持和详细的中文文档。

## 🚀 快速开始

### 安装方式

#### 方式 1: 从 PyPI 安装 (推荐)
```bash
pip install manimlib-creation
```

#### 方式 2: 从 GitHub 安装
```bash
pip install git+https://github.com/llby520/manimlib-creation-package.git
```

#### 方式 3: 使用 Conda
```bash
conda install -c conda-forge manimlib-creation
```

#### 方式 4: 本地开发安装
```bash
git clone https://github.com/llby520/manimlib-creation-package.git
cd manimlib-creation-package/creation_package/creationbuild_package
pip install -e .
```

### 快速验证
```python
import creation
creation._module_self_test()  # 运行自测试
```

## 🎉 v1.0.0 发布亮点

- ✅ **首个稳定版本** - 经过全面测试的稳定API
- ✅ **完整动画类库** - 7个核心动画类，覆盖常用动画需求
- ✅ **GitHub Actions CI/CD** - 自动化测试、构建和部署
- ✅ **Conda支持** - 完整的Conda环境配置和包管理
- ✅ **中文文档** - 详细的中文使用指南和示例
- ✅ **类型安全** - 完整的类型注解，支持IDE智能提示
- ✅ **跨平台兼容** - Windows、macOS、Linux全平台支持

## 📋 v1.0.0 核心特性

### 🎨 动画类库
- **ShowPartial** - 部分显示动画，支持自定义显示比例
- **ShowCreation** - 创建显示动画，模拟绘制过程
- **Uncreate** - 反向创建动画，逐步消除对象
- **Write** - 文字书写动画，逐字符显示文本
- **ShowIncreasingSubsets** - 递增子集显示动画
- **ShowSubmobjectsOneByOne** - 逐个显示子对象动画
- **AddTextWordByWord** - 逐词添加文本动画

### 🛠️ 技术特性
- **🐍 Python 3.8+** - 广泛的Python版本兼容性
- **📦 NumPy 1.19+** - 优化的数值计算支持
- **🔒 类型安全** - 完整的类型注解和 mypy 支持
- **🧪 全面测试** - 完整的测试覆盖和质量保证
- **🌐 CI/CD** - GitHub Actions 自动化工作流
- **📚 中文文档** - 详细的中文使用文档和示例

## 📖 使用示例

### 基本使用
```python
from manimlib import *
from creation import ShowCreation, Write, ShowPartial

class MyScene(Scene):
    def construct(self):
        # 创建几何对象
        circle = Circle(radius=2, color=BLUE)
        square = Square(side_length=2, color=RED)
        text = Text("Hello ManimLib!", font_size=48)
        
        # 使用动画类
        self.play(ShowCreation(circle))  # 显示创建过程
        self.play(Write(text))           # 文字书写动画
        self.play(ShowPartial(square, 0.5))  # 显示一半的正方形
        self.wait()
```

### 高级动画组合
```python
from creation import (
    ShowSubmobjectsOneByOne, 
    ShowIncreasingSubsets,
    AddTextWordByWord,
    Uncreate
)

class AdvancedScene(Scene):
    def construct(self):
        # 创建复杂对象
        group = VGroup(*[Circle(radius=0.5).shift(i*RIGHT) for i in range(5)])
        long_text = Text("这是一个逐词显示的文本示例")
        
        # 高级动画效果
        self.play(ShowSubmobjectsOneByOne(group))  # 逐个显示子对象
        self.play(AddTextWordByWord(long_text))    # 逐词添加文本
        self.play(Uncreate(group))                 # 反向创建动画
        self.wait()
```

## 🏗️ 项目结构

```
creation_package/
├── 📄 creation.py                      # 核心模块文件
├── 📄 README.md                        # 项目说明
├── 📄 PROJECT_OVERVIEW.md              # 详细项目概览
├── 📄 prepare_github_release.py        # GitHub 发布准备脚本
├── 📁 .github/                         # GitHub Actions 工作流
│   ├── 📄 GITHUB_ACTIONS_GUIDE.md     # CI/CD 指南
│   └── 📁 workflows/                   # 自动化工作流
│       ├── 📄 python-package.yml      # Python 包 CI/CD
│       ├── 📄 python-package-conda.yml # Conda 包 CI/CD
│       └── 📄 ...                      # 其他工作流
└── 📁 creationbuild_package/           # 构建和发布目录
    ├── 📄 creation.py                  # 核心实现
    ├── 📄 pyproject.toml               # 项目配置
    ├── 📄 README_creation.md           # 包说明文档
    ├── 📄 LICENSE                      # MIT 许可证
    ├── 📄 CHANGELOG.md                 # 变更日志
    ├── 📄 test_creation.py             # 测试套件
    ├── 📄 requirements_creation.txt    # 依赖列表
    ├── 📄 environment.yml              # Conda 环境
    ├── 📄 meta.yaml                    # Conda 构建配置
    └── 📁 中文输出文档/                 # 中文文档和示例
```

## 🧪 测试

### 运行测试套件
```bash
# 基本测试
python -m pytest creationbuild_package/test_creation.py -v

# 带覆盖率报告
python -m pytest creationbuild_package/test_creation.py --cov=creation --cov-report=html

# 性能基准测试
python -m pytest creationbuild_package/test_creation.py --benchmark-only

# 压力测试
python creationbuild_package/test_creation.py --stress
```

### 中文编码测试
```bash
python creationbuild_package/中文输出文档/test_chinese_encoding.py
```

## 🔧 开发

### 开发环境设置
```bash
# 克隆仓库
git clone https://github.com/llby520/manimlib-creation-package.git
cd manimlib-creation-package/creation_package

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows

# 安装开发依赖
cd creationbuild_package
pip install -e ".[dev]"
```

### 代码质量检查
```bash
# 代码格式化
black creation.py
isort creation.py

# 类型检查
mypy creation.py

# 代码检查
flake8 creation.py
```

### 构建包
```bash
cd creationbuild_package
python -m build
```

## 📦 发布到 GitHub

### 使用发布准备脚本
```bash
python prepare_github_release.py
```

这个脚本会:
- ✅ 检查所有必需文件
- ✅ 验证配置文件
- ✅ 检查 Git 状态
- ✅ 提供发布指导

### 手动发布步骤

1. **准备代码**
   ```bash
   git add .
   git commit -m "Prepare for release v1.0.0"
   ```

2. **创建 GitHub 仓库**
   - 在 GitHub 上创建新仓库
   - 复制仓库 URL

3. **推送代码**
   ```bash
   git remote add origin https://github.com/llby520/manimlib-creation-package.git
   git branch -M main
   git push -u origin main
   ```

4. **创建 Release**
   - 在 GitHub 上创建新的 Release
   - 上传构建的包文件 (可选)

## 🤝 贡献

我们欢迎所有形式的贡献！请查看 [贡献指南](creationbuild_package/README_creation.md#贡献指南) 了解详情。

### 贡献流程
1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](creationbuild_package/LICENSE) 文件了解详情。

## 🆘 支持

- **文档**: [项目 Wiki](https://github.com/llby520/manimlib-creation-package/wiki)
- **问题报告**: [GitHub Issues](https://github.com/llby520/manimlib-creation-package/issues)
- **讨论**: [GitHub Discussions](https://github.com/llby520/manimlib-creation-package/discussions)
- **邮箱**: team@manimlib.org

## 🔗 相关链接

- [PyPI 包页面](https://pypi.org/project/manimlib-creation/)
- [Conda 包页面](https://anaconda.org/conda-forge/manimlib-creation)
- [文档网站](https://github.com/llby520/manimlib-creation-package/wiki)
- [变更日志](creationbuild_package/CHANGELOG.md)
- [项目概览](PROJECT_OVERVIEW.md)

---

**注意**: 请将上述 URL 中的 `llby520/manimLibfuke` 替换为您的实际 GitHub 用户名和仓库名。

<div align="center">
  <strong>🎬 让数学动画创作变得简单而强大！</strong>
</div>