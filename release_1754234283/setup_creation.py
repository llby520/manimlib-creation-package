#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ManimLib Creation Animation Module - 长期支持版本
安装配置文件

这个setup.py文件允许将creation模块作为标准Python包进行安装和分发。

安装方法:
    pip install .
    
开发模式安装:
    pip install -e .
    
构建分发包:
    python setup.py sdist bdist_wheel
"""

import sys
from pathlib import Path
from setuptools import setup, find_packages

# 确保Python版本兼容性
if sys.version_info < (3, 8):
    raise RuntimeError(
        "ManimLib Creation Module 需要 Python 3.8 或更高版本。"
        f"当前版本: {sys.version_info.major}.{sys.version_info.minor}"
    )

# 读取README文件
HERE = Path(__file__).parent
README_PATH = HERE / "README_creation.md"
REQUIREMENTS_PATH = HERE / "requirements_creation.txt"

# 读取长描述
long_description = ""
if README_PATH.exists():
    with open(README_PATH, "r", encoding="utf-8") as f:
        long_description = f.read()

# 读取依赖要求
requirements = []
if REQUIREMENTS_PATH.exists():
    with open(REQUIREMENTS_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and not line.startswith("-"):
                requirements.append(line)

# 模块信息
MODULE_NAME = "manimlib_creation"
VERSION = "2.0.0"
AUTHOR = "ManimLib Community"
AUTHOR_EMAIL = "community@manimlib.org"
DESCRIPTION = "ManimLib创建动画模块 - 长期支持版本"
URL = "https://github.com/llby520/manimlib-creation-package"
LICENSE = "MIT"

# 分类器
CLASSIFIERS = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "Intended Audience :: Education",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    "Topic :: Multimedia :: Graphics",
    "Topic :: Multimedia :: Graphics :: 3D Modeling",
    "Topic :: Scientific/Engineering :: Visualization",
    "Topic :: Software Development :: Libraries :: Python Modules",
]

# 关键词
KEYWORDS = [
    "manim", "animation", "graphics", "visualization", 
    "mathematics", "education", "presentation", "创建动画",
    "数学可视化", "教育工具"
]

# 项目URL
PROJECT_URLS = {
    "Documentation": "https://docs.manim.community/",
    "Source": "https://github.com/llby520/manimlib-creation-package",
        "Tracker": "https://github.com/llby520/manimlib-creation-package/issues",
}

setup(
    name=MODULE_NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=URL,
    project_urls=PROJECT_URLS,
    
    # 包配置
    py_modules=["creation"],  # 单文件模块
    packages=find_packages(exclude=["tests*", "docs*"]),
    
    # 依赖配置
    python_requires=">=3.8",
    install_requires=requirements,
    
    # 可选依赖
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "black>=21.0.0",
            "mypy>=0.800",
            "flake8>=3.8.0",
        ],
        "docs": [
            "sphinx>=4.0.0",
            "sphinx-rtd-theme>=1.0.0",
        ],
    },
    
    # 元数据
    classifiers=CLASSIFIERS,
    keywords=KEYWORDS,
    license=LICENSE,
    
    # 包含数据文件
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.rst"],
    },
    
    # 入口点
    entry_points={
        "console_scripts": [
            "creation-test=creation:_module_self_test",
        ],
    },
    
    # 平台兼容性
    platforms=["any"],
    
    # ZIP安全
    zip_safe=False,
)

print(f"\n🎉 {MODULE_NAME} v{VERSION} 安装配置完成！")
print(f"📚 支持Python {sys.version_info.major}.{sys.version_info.minor}+")
print(f"🔧 依赖包数量: {len(requirements)}")
print(f"📖 长描述长度: {len(long_description)} 字符")
print("\n安装命令:")
print("  标准安装: pip install .")
print("  开发安装: pip install -e .")
print("  测试安装: pip install .[dev]")
print("\n验证安装:")
print("  python -c 'import creation; creation._module_self_test()'")
print("  或者: creation-test")