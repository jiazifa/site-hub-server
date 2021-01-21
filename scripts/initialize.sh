#!/bin/sh

set -e

poetry install

# 创建本地设置
touch local_settings.py > /dev/null