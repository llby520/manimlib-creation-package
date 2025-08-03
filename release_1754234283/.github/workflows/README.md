# GitHub Actions 工作流配置说明

本目录包含两个GitHub Actions配置文件，用于自动化测试和构建您的ManimLib Creation包。

## 配置文件说明

### 1. `python-package.yml` - 完整CI/CD流水线

这是一个功能完整的CI/CD配置，包含以下特性：

- **多平台测试**: Ubuntu, Windows, macOS
- **多Python版本**: 3.8, 3.9, 3.10, 3.11, 3.12
- **代码质量检查**: flake8, mypy
- **安全扫描**: safety, bandit
- **自动发布**: 支持PyPI发布
- **缓存优化**: pip依赖缓存

**触发条件**:
- 推送到main/develop分支
- Pull Request到main分支
- 发布新版本时

### 2. `simple-ci.yml` - 简化版CI

这是一个轻量级的CI配置，适合快速验证：

- **单平台测试**: 仅Ubuntu
- **多Python版本**: 3.8, 3.9, 3.10, 3.11
- **基础检查**: flake8代码检查
- **功能测试**: 模块导入和自测试
- **中文支持测试**: 验证中文编码

**触发条件**:
- 推送到main分支
- Pull Request到main分支

## 使用建议

### 初学者或小项目
推荐使用 `simple-ci.yml`：
- 运行速度快
- 资源消耗少
- 配置简单

### 生产环境或大型项目
推荐使用 `python-package.yml`：
- 全面的测试覆盖
- 多平台兼容性验证
- 自动化发布流程

## 项目结构适配

这些配置文件已经根据您的项目结构进行了定制：

```
creation_package/
├── .github/
│   └── workflows/
│       ├── python-package.yml
│       ├── simple-ci.yml
│       └── README.md
└── creationbuild_package/
    ├── creation.py
    ├── requirements_creation.txt
    ├── test_creation.py
    ├── Demo_ShowSubmobjectsOneByOne.py
    └── 中文输出文档/
        ├── test_chinese_encoding.py
        └── Demo_ShowSubmobjectsOneByOne.py
```

## 环境变量和密钥设置

如果要使用自动发布功能，需要在GitHub仓库设置中配置：

1. **PyPI API Token** (如果不使用trusted publishing):
   - 在仓库Settings → Secrets and variables → Actions
   - 添加名为 `PYPI_API_TOKEN` 的密钥

2. **Trusted Publishing** (推荐):
   - 在PyPI项目设置中配置GitHub Actions trusted publishing
   - 无需手动管理API token

## 自定义配置

您可以根据需要修改以下内容：

- **Python版本**: 在 `matrix.python-version` 中调整
- **触发分支**: 修改 `branches` 列表
- **测试命令**: 在相应的步骤中添加或修改命令
- **依赖文件**: 如果依赖文件名不同，请相应修改路径

## 故障排除

如果CI失败，请检查：

1. **依赖文件**: 确保 `requirements_creation.txt` 存在且格式正确
2. **文件路径**: 验证所有引用的文件路径是否正确
3. **Python版本兼容性**: 确保代码兼容所测试的Python版本
4. **中文编码**: 确保中文文件和路径在CI环境中正常工作

## 监控和通知

您可以在GitHub仓库的Actions标签页查看工作流运行状态。建议：

- 启用邮件通知以及时了解CI状态
- 在README中添加CI状态徽章
- 定期检查和更新依赖版本