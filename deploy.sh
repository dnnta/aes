#!/bin/bash

# AES应用部署脚本

echo "开始部署AES加密应用..."

# 1. 更新系统包
echo "更新系统包..."
sudo apt update && sudo apt upgrade -y

# 2. 安装Python和pip
echo "安装Python和pip..."
sudo apt install python3 python3-pip python3-venv -y

# 3. 创建虚拟环境
echo "创建Python虚拟环境..."
python3 -m venv venv
source venv/bin/activate

# 4. 安装依赖
echo "安装Python依赖..."
pip install --upgrade pip
pip install -r requirements.txt

# 5. 安装Nginx
echo "安装Nginx..."
sudo apt install nginx -y

# 6. 配置Nginx
echo "配置Nginx..."
sudo tee /etc/nginx/sites-available/aes-app << EOF
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# 7. 启用站点
sudo ln -sf /etc/nginx/sites-available/aes-app /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t && sudo systemctl restart nginx

# 8. 创建systemd服务
echo "创建systemd服务..."
sudo tee /etc/systemd/system/aes-app.service << EOF
[Unit]
Description=AES Encryption Web App
After=network.target

[Service]
User=$USER
WorkingDirectory=$(pwd)
Environment="PATH=$(pwd)/venv/bin"
ExecStart=$(pwd)/venv/bin/gunicorn -c gunicorn.conf.py wsgi:app
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# 9. 启动服务
echo "启动服务..."
sudo systemctl daemon-reload
sudo systemctl enable aes-app
sudo systemctl start aes-app

# 10. 配置防火墙
echo "配置防火墙..."
sudo ufw allow 80
sudo ufw allow 22
sudo ufw --force enable

echo "部署完成！"
echo "应用地址: http://$(curl -s ifconfig.me)"
echo "检查服务状态: sudo systemctl status aes-app"
echo "查看日志: sudo journalctl -u aes-app -f" 