#!/bin/sh

set -e

# 设置虚拟环境存在于本地
poetry config virtualenvs.in-project true

# 安装依赖
poetry install

# 创建本地设置
touch local_settings.py > /dev/null