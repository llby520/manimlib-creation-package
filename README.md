# Manimlib Creation Package

[![CI/CD](https://github.com/llby520/manimLibfuke/actions/workflows/python-package.yml/badge.svg)](https://github.com/llby520/manimLibfuke/actions/workflows/python-package.yml)
[![Conda CI/CD](https://github.com/llby520/manimLibfuke/actions/workflows/python-package-conda.yml/badge.svg)](https://github.com/llby520/manimLibfuke/actions/workflows/python-package-conda.yml)
[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/manimlib-creation.svg)](https://badge.fury.io/py/manimlib-creation)

**Manimlib Creation Module** - 高级数学动画创建工具包，提供强大的动画创建、对象操作和渲染优化功能。

## 🚀 快速开始

### 安装方式

#### 方式 1: 从 PyPI 安装 (推荐)
```bash
pip install manimlib-creation
```

#### 方式 2: 从 GitHub 安装
```bash
pip install git+https://github.com/llby520/manimLibfuke.git
```

#### 方式 3: 使用 Conda
```bash
conda install -c conda-forge manimlib-creation
```

#### 方式 4: 本地开发安装
```bash
git clone https://github.com/llby520/manimLibfuke.git
cd manimLibfuke/creation_package/creationbuild_package
pip install -e .
```

### 快速验证
```python
import creation
creation._module_self_test()  # 运行自测试
```

## 📋 功能特性

- **🎨 丰富的动画类型**: 支持多种动画效果和过渡
- **⚡ 高性能渲染**: 优化的渲染引擎，提升动画生成速度
- **🔧 灵活的对象操作**: 强大的数学对象创建和操作工具
- **📊 性能分析**: 内置性能监控和优化建议
- **🧪 全面测试**: 完整的测试覆盖和质量保证
- **🔒 类型安全**: 完整的类型注解和 mypy 支持

## 📖 使用示例

```python
import creation

# 创建基本动画对象
animator = creation.AnimationCreator()

# 添加数学对象
circle = animator.create_circle(radius=2, color="blue")
text = animator.create_text("Hello Manim!", font_size=48)

# 创建动画序列
animation = animator.create_animation_sequence([
    creation.FadeIn(circle),
    creation.Write(text),
    creation.Transform(circle, text)
])

# 渲染动画
animator.render(animation, output_file="my_animation.mp4")
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
git clone https://github.com/llby520/manimLibfuke.git
cd manimLibfuke/creation_package

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
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
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

- **文档**: [项目 Wiki](https://github.com/llby520/manimLibfuke/wiki)
- **问题报告**: [GitHub Issues](https://github.com/llby520/manimLibfuke/issues)
- **讨论**: [GitHub Discussions](https://github.com/llby520/manimLibfuke/discussions)
- **邮箱**: team@manimlib.org

## 🔗 相关链接

- [PyPI 包页面](https://pypi.org/project/manimlib-creation/)
- [Conda 包页面](https://anaconda.org/conda-forge/manimlib-creation)
- [文档网站](https://github.com/llby520/manimLibfuke/wiki)
- [变更日志](creationbuild_package/CHANGELOG.md)
- [项目概览](PROJECT_OVERVIEW.md)

---

**注意**: 请将上述 URL 中的 `llby520/manimLibfuke` 替换为您的实际 GitHub 用户名和仓库名。

<div align="center">
  <strong>🎬 让数学动画创作变得简单而强大！</strong>
</div>