# AES 加密/解密 Web 应用

这是一个基于Flask的AES加密/解密工具，支持ECB和CBC模式，提供详细的加密过程展示。

## 功能特性

- 支持AES-128、AES-192、AES-256加密
- 支持ECB和CBC模式
- 实时显示加密/解密过程
- 美观的Web界面
- 详细的步骤说明

## 本地开发

### 安装依赖
```bash
pip install -r requirements.txt
```

### 运行应用
```bash
python app.py
```

访问 http://localhost:5000

## 服务器部署

### 方法一：使用自动部署脚本

1. 上传项目文件到服务器
2. 给部署脚本执行权限：
   ```bash
   chmod +x deploy.sh
   ```
3. 运行部署脚本：
   ```bash
   ./deploy.sh
   ```

### 方法二：手动部署

1. **安装系统依赖**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip python3-venv nginx -y
   ```

2. **创建虚拟环境**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **配置Nginx**
   ```bash
   sudo cp nginx.conf /etc/nginx/sites-available/aes-app
   sudo ln -s /etc/nginx/sites-available/aes-app /etc/nginx/sites-enabled/
   sudo nginx -t && sudo systemctl restart nginx
   ```

4. **创建systemd服务**
   ```bash
   sudo cp aes-app.service /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl enable aes-app
   sudo systemctl start aes-app
   ```

5. **配置防火墙**
   ```bash
   sudo ufw allow 80
   sudo ufw allow 22
   sudo ufw enable
   ```

## 服务管理

- 启动服务：`sudo systemctl start aes-app`
- 停止服务：`sudo systemctl stop aes-app`
- 重启服务：`sudo systemctl restart aes-app`
- 查看状态：`sudo systemctl status aes-app`
- 查看日志：`sudo journalctl -u aes-app -f`

## 项目结构

```
aes/
├── app.py              # Flask应用主文件
├── aes_logic.py        # AES加密/解密逻辑
├── wsgi.py             # WSGI入口文件
├── gunicorn.conf.py    # Gunicorn配置
├── requirements.txt    # Python依赖
├── deploy.sh           # 自动部署脚本
├── README.md           # 项目文档
└── templates/
    └── index.html      # Web界面模板
```

## 安全注意事项

- 生产环境中请使用HTTPS
- 定期更新依赖包
- 监控服务器日志
- 配置适当的防火墙规则

## 故障排除

1. **服务无法启动**
   - 检查端口是否被占用：`sudo netstat -tlnp | grep :5000`
   - 查看服务日志：`sudo journalctl -u aes-app -f`

2. **Nginx配置错误**
   - 检查配置：`sudo nginx -t`
   - 重启Nginx：`sudo systemctl restart nginx`

3. **依赖安装失败**
   - 更新pip：`pip install --upgrade pip`
   - 检查Python版本：`python3 --version` 