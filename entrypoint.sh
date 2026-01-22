#!/bin/bash
set -e

echo "🔧 启动 Flask 视频回放系统..."
echo "📁 挂载目录: /mnt/sdb1/jiankang"

# 确保视频目录存在
# 创建必要目录
mkdir -p /opt/videos/templates
mkdir -p /mnt/sdb1/jiankang


# 启动 Python 应用
echo "🚀 启动视频回放服务..."
exec python3 /opt/videos/app.py
