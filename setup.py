"""
LogicDetector 安装脚本
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="logic-detector",
    version="1.0.0",
    author="火眼团队",
    author_email="logic-detector@example.com",
    description="多模块融合的逻辑推理幻觉检测框架 (ACL 2026)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/example/logic-detector",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "pytest>=7.3.0",
            "pytest-cov>=4.1.0",
        ],
        "full": [
            "z3-solver>=4.12.0",  # 完整的定理证明器支持
        ],
    },
    include_package_data=True,
    package_data={
        "logic_detector": [
            "data/*.json",
        ],
    },
)
