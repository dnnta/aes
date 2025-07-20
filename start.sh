#!/bin/bash

# 简单的AES应用启动脚本

echo "启动AES加密应用..."

# 检查虚拟环境是否存在
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 安装/更新依赖
echo "安装依赖..."
pip install --upgrade pip
pip install -r requirements.txt

# 启动应用
echo "启动应用..."
echo "应用将在 http://0.0.0.0:5000 上运行"
echo "按 Ctrl+C 停止应用"

# 使用gunicorn启动
gunicorn -c gunicorn.conf.py wsgi:app 