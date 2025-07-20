# Vercel 部署指南

## 部署步骤

### 1. 安装 Vercel CLI
```bash
npm install -g vercel
```

### 2. 登录 Vercel
```bash
vercel login
```

### 3. 部署项目
在项目根目录运行：
```bash
vercel
```

或者直接部署到生产环境：
```bash
vercel --prod
```

### 4. 自动部署
将代码推送到GitHub后，Vercel会自动检测并部署：
```bash
git add .
git commit -m "Add Vercel deployment"
git push origin main
```

## 项目结构
```
aes/
├── api/
│   └── index.py          # Vercel API入口
├── templates/
│   └── index.html        # HTML模板
├── app.py                # 原始Flask应用
├── aes_logic.py          # AES逻辑
├── requirements.txt      # Python依赖
├── vercel.json           # Vercel配置
└── VERCEL_DEPLOY.md      # 部署说明
```

## 注意事项

1. **依赖限制**: Vercel对Python包有大小限制，确保依赖包不会过大
2. **执行时间**: 函数执行时间限制为10秒（免费版）或60秒（付费版）
3. **内存限制**: 免费版限制为1024MB内存
4. **冷启动**: 首次访问可能有延迟

## 故障排除

### 常见问题

1. **导入错误**
   - 确保所有依赖都在 `requirements.txt` 中
   - 检查Python路径设置

2. **模板找不到**
   - 确保 `templates` 目录在正确位置
   - 检查Flask应用配置

3. **部署失败**
   - 检查 `vercel.json` 配置
   - 查看Vercel部署日志

### 调试命令
```bash
# 本地测试
vercel dev

# 查看部署日志
vercel logs

# 重新部署
vercel --force
```

## 自定义域名

部署成功后，可以在Vercel控制台添加自定义域名：
1. 进入项目设置
2. 选择 "Domains"
3. 添加你的域名
4. 配置DNS记录 