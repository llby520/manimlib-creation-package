# GitHub 发布完整指南

本指南将帮助您将 Manimlib Creation Package 发布到 GitHub，并制作成可安装的 Python 包。

## 📋 发布前检查清单

### 1. 运行发布准备脚本
```bash
python prepare_github_release.py
```

这个脚本会检查:
- ✅ 所有必需文件是否存在
- ✅ 配置文件是否正确
- ✅ 包是否已构建
- ✅ Git 状态

### 2. 更新 GitHub URLs
如果您的 GitHub 用户名和仓库名与示例不同，请运行:
```bash
python update_github_urls.py YOUR_USERNAME YOUR_REPO_NAME
```

例如:
```bash
python update_github_urls.py john-doe my-manimlib-creation
```

## 🚀 发布步骤

### 步骤 1: 准备 Git 仓库

#### 1.1 初始化 Git (如果还没有)
```bash
cd /c/Users/aym11/Desktop/huanjing/复刻manimlib/creation_package
git init
```

#### 1.2 添加所有文件
```bash
git add .
```

#### 1.3 创建初始提交
```bash
git commit -m "Initial commit: Manimlib Creation Package v1.0.0

- 完整的动画创建模块
- 支持 Python 3.9+
- 包含完整的测试套件
- 支持 PyPI 和 Conda 发布
- 完整的 CI/CD 流程"
```

### 步骤 2: 创建 GitHub 仓库

#### 2.1 在 GitHub 上创建新仓库
1. 访问 [GitHub](https://github.com)
2. 点击右上角的 "+" 按钮
3. 选择 "New repository"
4. 填写仓库信息:
   - **Repository name**: `manimlib-creation` (或您选择的名称)
   - **Description**: `Manimlib Creation Module - Advanced animation creation utilities`
   - **Visibility**: Public (推荐) 或 Private
   - **不要** 勾选 "Add a README file" (我们已经有了)
   - **不要** 勾选 "Add .gitignore" (我们已经配置了)
   - **License**: 选择 MIT License

#### 2.2 获取仓库 URL
创建后，GitHub 会显示仓库 URL，类似:
```
https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
```

### 步骤 3: 连接本地仓库到 GitHub

#### 3.1 添加远程仓库
```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
```

#### 3.2 设置主分支
```bash
git branch -M main
```

#### 3.3 推送代码
```bash
git push -u origin main
```

### 步骤 4: 验证包构建

#### 4.1 构建包
```bash
cd creationbuild_package
python -m build
```

#### 4.2 测试包安装
```bash
# 在新的虚拟环境中测试
python -m venv test_env
test_env\Scripts\activate  # Windows
# 或
source test_env/bin/activate  # Linux/Mac

# 安装构建的包
pip install dist/*.whl

# 测试导入和功能
python -c "import creation; creation._module_self_test()"

# 退出测试环境
deactivate
```

### 步骤 5: 配置 GitHub Actions

#### 5.1 设置 PyPI 令牌 (可选)
如果您想自动发布到 PyPI:

1. 在 [PyPI](https://pypi.org) 创建账户
2. 生成 API 令牌
3. 在 GitHub 仓库设置中添加 Secret:
   - Name: `PYPI_API_TOKEN`
   - Value: 您的 PyPI API 令牌

#### 5.2 设置 Conda 令牌 (可选)
如果您想发布到 Conda:

1. 在 [Anaconda Cloud](https://anaconda.org) 创建账户
2. 在 GitHub 仓库设置中添加 Secrets:
   - `ANACONDA_USERNAME`: 您的 Anaconda 用户名
   - `ANACONDA_PASSWORD`: 您的 Anaconda 密码
   - `ANACONDA_API_TOKEN`: 您的 Anaconda API 令牌

### 步骤 6: 创建 GitHub Release

#### 6.1 在 GitHub 上创建 Release
1. 在您的 GitHub 仓库页面，点击 "Releases"
2. 点击 "Create a new release"
3. 填写 Release 信息:
   - **Tag version**: `v1.0.0`
   - **Release title**: `Manimlib Creation Package v1.0.0`
   - **Description**: 复制以下内容:

```markdown
# Manimlib Creation Package v1.0.0

🎉 首次发布！这是 Manimlib Creation Module 的第一个稳定版本。

## ✨ 主要功能

- 🎨 **丰富的动画类型**: 支持多种动画效果和过渡
- ⚡ **高性能渲染**: 优化的渲染引擎
- 🔧 **灵活的对象操作**: 强大的数学对象创建和操作工具
- 📊 **性能分析**: 内置性能监控和优化建议
- 🧪 **全面测试**: 完整的测试覆盖
- 🔒 **类型安全**: 完整的类型注解和 mypy 支持

## 📦 安装方式

### 从 PyPI 安装
```bash
pip install manimlib-creation
```

### 从 GitHub 安装
```bash
pip install git+https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
```

### 使用 Conda
```bash
conda install -c conda-forge manimlib-creation
```

## 🚀 快速开始

```python
import creation
creation._module_self_test()  # 运行自测试
```

## 📋 技术规格

- **Python 版本**: 3.9+
- **主要依赖**: numpy>=1.20.0, typing-extensions>=4.0.0
- **测试覆盖率**: >95%
- **代码质量**: 通过 flake8, mypy, black 检查

## 🔗 相关链接

- [文档](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME/wiki)
- [问题报告](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME/issues)
- [变更日志](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME/blob/main/creationbuild_package/CHANGELOG.md)

---

**完整的发布说明请查看 [CHANGELOG.md](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME/blob/main/creationbuild_package/CHANGELOG.md)**
```

#### 6.2 上传构建文件 (可选)
在 "Attach binaries" 部分，您可以上传:
- `creationbuild_package/dist/manimlib_creation-1.0.0-py3-none-any.whl`
- `creationbuild_package/dist/manimlib_creation-1.0.0.tar.gz`

#### 6.3 发布 Release
点击 "Publish release" 完成发布。

## 📦 包安装测试

### 测试从 GitHub 安装
```bash
# 创建新的测试环境
python -m venv github_test_env
github_test_env\Scripts\activate  # Windows

# 从 GitHub 安装
pip install git+https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# 测试功能
python -c "import creation; creation._module_self_test()"

# 清理
deactivate
rmdir /s github_test_env  # Windows
```

### 测试从本地包安装
```bash
# 创建新的测试环境
python -m venv local_test_env
local_test_env\Scripts\activate  # Windows

# 从本地 wheel 文件安装
pip install creationbuild_package/dist/*.whl

# 测试功能
python -c "import creation; creation._module_self_test()"

# 清理
deactivate
rmdir /s local_test_env  # Windows
```

## 🔄 持续集成/持续部署 (CI/CD)

项目包含完整的 GitHub Actions 工作流:

- **`python-package.yml`**: 标准 Python 包 CI/CD
- **`python-package-conda.yml`**: Conda 包 CI/CD
- **`ci.yml`**: 基本持续集成
- **`release.yml`**: 自动发布流程

这些工作流会在以下情况自动运行:
- 推送到 `main` 或 `develop` 分支
- 创建 Pull Request
- 创建 Release

## 🐛 故障排除

### 常见问题

#### 1. Git 推送失败
```bash
# 如果遇到认证问题，使用 Personal Access Token
# 在 GitHub Settings > Developer settings > Personal access tokens 创建
git remote set-url origin https://YOUR_TOKEN@github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
```

#### 2. 包构建失败
```bash
# 确保安装了构建工具
pip install --upgrade build setuptools wheel

# 清理之前的构建
rm -rf creationbuild_package/dist/
rm -rf creationbuild_package/build/
rm -rf creationbuild_package/*.egg-info/

# 重新构建
cd creationbuild_package
python -m build
```

#### 3. 测试失败
```bash
# 安装测试依赖
pip install pytest pytest-cov

# 运行测试
python -m pytest creationbuild_package/test_creation.py -v
```

#### 4. GitHub Actions 失败
- 检查 `.github/workflows/` 中的工作流文件
- 确保所有必需的 Secrets 已配置
- 查看 Actions 日志了解具体错误

## 📞 获取帮助

如果您在发布过程中遇到问题:

1. **检查文档**: 阅读 `PROJECT_OVERVIEW.md` 和 `README.md`
2. **运行诊断**: `python prepare_github_release.py`
3. **查看日志**: 检查 GitHub Actions 的运行日志
4. **寻求帮助**: 在 GitHub Issues 中报告问题

## 🎉 发布完成！

恭喜！您已经成功将 Manimlib Creation Package 发布到 GitHub。

现在用户可以通过以下方式安装您的包:

```bash
# 从 GitHub 安装
pip install git+https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# 如果发布到 PyPI
pip install manimlib-creation

# 如果发布到 Conda
conda install -c conda-forge manimlib-creation
```

---

**记住**: 将所有示例中的 `YOUR_USERNAME` 和 `YOUR_REPO_NAME` 替换为您的实际 GitHub 用户名和仓库名称。