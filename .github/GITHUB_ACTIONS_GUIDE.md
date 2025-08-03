# GitHub Actions 工作流指南

本指南详细介绍了项目中的 GitHub Actions 工作流配置，帮助您理解、使用和定制这些自动化流程。

## 📋 目录

- [工作流概览](#工作流概览)
- [快速开始](#快速开始)
- [工作流详解](#工作流详解)
- [配置说明](#配置说明)
- [最佳实践](#最佳实践)
- [故障排除](#故障排除)
- [自定义指南](#自定义指南)

## 🔍 工作流概览

| 工作流 | 文件 | 触发条件 | 主要功能 | 运行时间 |
|--------|------|----------|----------|----------|
| **持续集成** | `ci.yml` | Push/PR | 代码质量检查、测试、构建 | ~15-25分钟 |
| **快速测试** | `quick-test.yml` | Push/PR | 基础语法和功能验证 | ~3-5分钟 |
| **发布部署** | `release.yml` | 标签推送 | 自动化版本发布和分发 | ~10-15分钟 |
| **安全检查** | `security-and-deps.yml` | 定时/手动 | 安全扫描和依赖更新 | ~8-12分钟 |
| **文档构建** | `docs.yml` | 文档变更 | API文档生成和部署 | ~5-8分钟 |

## 🚀 快速开始

### 1. 启用 GitHub Actions

1. 在 GitHub 仓库中，转到 **Settings** → **Actions** → **General**
2. 选择 "Allow all actions and reusable workflows"
3. 保存设置

### 2. 配置必要的 Secrets

在 **Settings** → **Secrets and variables** → **Actions** 中添加：

```bash
# 可选：PyPI 发布（如果需要）
PYPI_API_TOKEN=your_pypi_token

# 可选：自定义通知
SLACK_WEBHOOK_URL=your_slack_webhook
DISCORD_WEBHOOK_URL=your_discord_webhook
```

### 3. 设置分支保护

在 **Settings** → **Branches** 中为 `main` 分支设置保护规则：

- ✅ Require status checks to pass before merging
- ✅ Require branches to be up to date before merging
- 选择必需的状态检查：
  - `code-quality`
  - `test-python-3.9`
  - `test-python-3.10`
  - `test-python-3.11`

## 📖 工作流详解

### 🔧 持续集成 (ci.yml)

**触发条件：**
- Push 到 `main`, `develop`, `feature/*` 分支
- Pull Request 到 `main` 分支
- 每日定时运行（UTC 02:00）

**主要作业：**

1. **代码质量检查** (`code-quality`)
   - 语法检查 (flake8)
   - 代码格式化 (black)
   - 导入排序 (isort)
   - 类型检查 (mypy)
   - 安全扫描 (bandit)

2. **多版本测试** (`test-python-X.X`)
   - Python 3.9, 3.10, 3.11
   - 多个 NumPy 版本组合
   - 单元测试和集成测试
   - 性能基准测试

3. **兼容性测试** (`compatibility-test`)
   - 不同操作系统 (Ubuntu, Windows, macOS)
   - 边界条件测试
   - 向后兼容性验证

4. **文档和示例测试** (`docs-and-examples`)
   - 文档构建测试
   - 示例代码执行
   - API 文档生成

5. **包构建测试** (`build-test`)
   - 源码分发包构建
   - Wheel 包构建
   - 安装测试

**输出产物：**
- 测试报告 (`test-reports`)
- 覆盖率报告 (`coverage-reports`)
- 构建包 (`build-artifacts`)
- 性能报告 (`performance-reports`)

### ⚡ 快速测试 (quick-test.yml)

**触发条件：**
- 所有 Push 和 Pull Request
- 优先级高，快速反馈

**检查项目：**
- Python 语法检查
- 模块导入测试
- 基本功能验证
- 代码格式检查

**特点：**
- 运行时间短 (~3-5分钟)
- 快速失败，及时反馈
- 适合开发过程中的频繁检查

### 🚀 发布部署 (release.yml)

**触发条件：**
- 推送版本标签 (如 `v2.0.0`)
- 手动触发 (workflow_dispatch)

**发布流程：**

1. **预发布检查**
   - 版本号验证
   - 模块完整性检查
   - 综合测试套件

2. **构建发布包**
   - 更新版本信息
   - 构建源码包和 Wheel
   - 包完整性检查

3. **创建 GitHub Release**
   - 自动生成发布说明
   - 上传构建产物
   - 创建 Release 页面

4. **发布到 PyPI** (可选)
   - 上传到 PyPI
   - 验证安装

**安全措施：**
- 需要手动批准
- 使用受保护的环境
- 签名验证

### 🔒 安全检查 (security-and-deps.yml)

**触发条件：**
- 每周定时运行
- 依赖文件变更
- 手动触发

**安全扫描：**
- **Safety**: 已知漏洞检查
- **pip-audit**: 依赖安全审计
- **Bandit**: 代码安全分析
- **Semgrep**: 静态代码分析

**依赖管理：**
- 过期依赖检查
- 依赖树分析
- 兼容性测试
- 自动更新建议

**问题处理：**
- 自动创建 Issue
- 安全报告生成
- 修复建议提供

### 📚 文档构建 (docs.yml)

**触发条件：**
- 文档文件变更
- 代码注释更新
- 手动触发

**构建内容：**
- API 文档 (Sphinx)
- 使用指南
- 示例代码
- 变更日志

**部署目标：**
- GitHub Pages
- 文档网站更新
- 搜索索引更新

## ⚙️ 配置说明

### 环境变量

```yaml
# 全局环境变量
env:
  PYTHONUNBUFFERED: 1              # 实时输出
  PYTHONDONTWRITEBYTECODE: 1       # 不生成 .pyc 文件
  PIP_DISABLE_PIP_VERSION_CHECK: 1 # 禁用 pip 版本检查
  PIP_NO_CACHE_DIR: 1              # 禁用 pip 缓存
```

### 权限设置

```yaml
permissions:
  contents: read          # 读取仓库内容
  issues: write          # 创建和更新 Issue
  pull-requests: write   # 创建和更新 PR
  security-events: write # 上传安全报告
  pages: write          # 部署到 GitHub Pages
  id-token: write       # OIDC 令牌
```

### 并发控制

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true  # 取消进行中的运行
```

## 🎯 最佳实践

### 1. 工作流优化

**缓存策略：**
```yaml
- name: Cache dependencies
  uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements*.txt') }}
    restore-keys: |
      ${{ runner.os }}-pip-
```

**矩阵策略：**
```yaml
strategy:
  fail-fast: false  # 不因单个失败而停止所有测试
  matrix:
    python-version: ['3.9', '3.10', '3.11']
    os: [ubuntu-latest, windows-latest, macos-latest]
    exclude:
      - os: macos-latest
        python-version: '3.9'  # 排除特定组合
```

**条件执行：**
```yaml
# 只在特定条件下运行
if: github.event_name == 'push' && github.ref == 'refs/heads/main'

# 检查提交消息
if: contains(github.event.head_commit.message, '[skip ci]') == false

# 检查文件变更
if: contains(github.event.head_commit.modified, '*.py')
```

### 2. 安全实践

**Secrets 使用：**
```yaml
# ✅ 正确做法
env:
  API_KEY: ${{ secrets.API_KEY }}
run: |
  if [ -n "$API_KEY" ]; then
    echo "API Key configured"
  fi

# ❌ 错误做法
run: echo "API Key: ${{ secrets.API_KEY }}"  # 会泄露到日志
```

**权限最小化：**
```yaml
permissions:
  contents: read  # 只给必需的权限
  # issues: write  # 注释掉不需要的权限
```

### 3. 性能优化

**并行执行：**
```yaml
jobs:
  test:
    strategy:
      matrix:
        include:
          - python: '3.9'
            toxenv: py39
          - python: '3.10'
            toxenv: py310
    runs-on: ubuntu-latest
```

**资源限制：**
```yaml
jobs:
  test:
    timeout-minutes: 30  # 防止无限运行
    runs-on: ubuntu-latest
```

### 4. 调试技巧

**调试模式：**
```yaml
- name: Debug information
  run: |
    echo "Event: ${{ github.event_name }}"
    echo "Ref: ${{ github.ref }}"
    echo "SHA: ${{ github.sha }}"
    echo "Actor: ${{ github.actor }}"
    env
```

**步骤输出：**
```yaml
- name: Set output
  id: step1
  run: echo "result=success" >> $GITHUB_OUTPUT

- name: Use output
  run: echo "Previous step result: ${{ steps.step1.outputs.result }}"
```

## 🔧 故障排除

### 常见问题

#### 1. 权限错误

**问题：** `Error: Resource not accessible by integration`

**解决方案：**
```yaml
permissions:
  contents: write  # 添加必要权限
  issues: write
```

#### 2. 缓存问题

**问题：** 依赖安装缓慢或失败

**解决方案：**
```yaml
- name: Clear cache
  run: |
    pip cache purge
    rm -rf ~/.cache/pip
```

#### 3. 超时问题

**问题：** 作业运行超时

**解决方案：**
```yaml
jobs:
  test:
    timeout-minutes: 60  # 增加超时时间
    steps:
    - name: Long running step
      timeout-minutes: 30  # 单步超时
```

#### 4. 矩阵测试失败

**问题：** 某个矩阵组合失败导致整个工作流失败

**解决方案：**
```yaml
strategy:
  fail-fast: false  # 允许其他组合继续运行
  matrix:
    python-version: ['3.9', '3.10', '3.11']
    experimental: [false]
    include:
      - python-version: '3.12-dev'
        experimental: true
continue-on-error: ${{ matrix.experimental }}  # 实验性版本允许失败
```

### 调试工具

#### 1. 启用调试日志

在仓库 Secrets 中添加：
```
ACTIONS_STEP_DEBUG=true
ACTIONS_RUNNER_DEBUG=true
```

#### 2. SSH 调试

```yaml
- name: Setup tmate session
  uses: mxschmitt/action-tmate@v3
  if: failure()  # 只在失败时启用
```

#### 3. 本地测试

使用 [act](https://github.com/nektos/act) 在本地运行 GitHub Actions：

```bash
# 安装 act
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

# 运行工作流
act push
act pull_request
```

## 🎨 自定义指南

### 1. 创建新工作流

1. 复制 `template.yml` 文件
2. 重命名为描述性名称
3. 修改触发条件和作业
4. 测试并调整

### 2. 修改现有工作流

**添加新的 Python 版本：**
```yaml
matrix:
  python-version: ['3.9', '3.10', '3.11', '3.12']  # 添加 3.12
```

**添加新的操作系统：**
```yaml
matrix:
  os: [ubuntu-latest, windows-latest, macos-latest, macos-13]  # 添加 macOS 13
```

**添加新的检查步骤：**
```yaml
- name: Custom check
  run: |
    echo "Running custom check"
    # 添加您的检查逻辑
```

### 3. 集成外部服务

**Slack 通知：**
```yaml
- name: Slack notification
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    webhook_url: ${{ secrets.SLACK_WEBHOOK_URL }}
  if: always()
```

**代码覆盖率报告：**
```yaml
- name: Upload to Codecov
  uses: codecov/codecov-action@v3
  with:
    file: ./coverage.xml
    flags: unittests
```

### 4. 环境特定配置

**开发环境：**
```yaml
if: github.ref == 'refs/heads/develop'
env:
  ENVIRONMENT: development
  DEBUG: true
```

**生产环境：**
```yaml
if: github.ref == 'refs/heads/main'
env:
  ENVIRONMENT: production
  DEBUG: false
environment: production  # 需要手动批准
```

## 📊 监控和分析

### 1. 工作流状态徽章

在 README.md 中添加状态徽章：

```markdown
[![CI](https://github.com/username/repo/workflows/CI/badge.svg)](https://github.com/username/repo/actions/workflows/ci.yml)
[![Security](https://github.com/username/repo/workflows/Security/badge.svg)](https://github.com/username/repo/actions/workflows/security-and-deps.yml)
```

### 2. 性能监控

```yaml
- name: Performance monitoring
  run: |
    echo "=== 性能指标 ==="
    echo "开始时间: $(date)"
    start_time=$(date +%s)
    
    # 运行测试
    python -m pytest --benchmark-only
    
    end_time=$(date +%s)
    duration=$((end_time - start_time))
    echo "执行时间: ${duration}秒"
    
    # 记录到文件
    echo "${duration}" >> performance.log
```

### 3. 资源使用监控

```yaml
- name: Resource monitoring
  run: |
    echo "=== 资源使用情况 ==="
    echo "CPU 信息:"
    nproc
    echo "内存信息:"
    free -h
    echo "磁盘空间:"
    df -h
```

## 📚 参考资源

### 官方文档
- [GitHub Actions 文档](https://docs.github.com/en/actions)
- [工作流语法参考](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [上下文和表达式](https://docs.github.com/en/actions/learn-github-actions/contexts)

### 有用的 Actions
- [actions/checkout](https://github.com/actions/checkout) - 检出代码
- [actions/setup-python](https://github.com/actions/setup-python) - 设置 Python
- [actions/cache](https://github.com/actions/cache) - 缓存依赖
- [actions/upload-artifact](https://github.com/actions/upload-artifact) - 上传产物
- [codecov/codecov-action](https://github.com/codecov/codecov-action) - 代码覆盖率

### 社区资源
- [GitHub Actions Marketplace](https://github.com/marketplace?type=actions)
- [Awesome Actions](https://github.com/sdras/awesome-actions)
- [GitHub Actions 最佳实践](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions)

## 🤝 贡献指南

如果您想改进这些工作流配置：

1. Fork 仓库
2. 创建功能分支
3. 测试您的更改
4. 提交 Pull Request
5. 详细描述更改内容

### 测试新工作流

1. 在您的 fork 中测试
2. 确保所有检查通过
3. 验证性能影响
4. 更新相关文档

---

**最后更新：** 2024年1月
**维护者：** Manimlib 开发团队
**许可证：** MIT License

如有问题或建议，请创建 Issue 或联系维护团队。