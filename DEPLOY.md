# projectAlpha 部署文档

## 环境要求

| 组件 | 最低版本 | 推荐版本 |
|------|---------|---------|
| Python | 3.11 | 3.12 |
| Node.js | 18 | 20 LTS |
| PostgreSQL | 15 | 16 |
| 操作系统 | Windows 10 / Ubuntu 22.04 / macOS 12 | - |
| 内存 | 2GB | 4GB |
| 磁盘 | 500MB | 1GB |

---

## 一、环境准备

### 1.1 安装 PostgreSQL

**Windows:**
```powershell
winget install PostgreSQL.PostgreSQL
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

**macOS:**
```bash
brew install postgresql
```

### 1.2 安装 Python 3.11+

**Windows:**
```powershell
winget install Python.Python.3.12
```

**Ubuntu/Debian:**
```bash
sudo apt install python3.12 python3.12-venv python3.12-dev
```

**macOS:**
```bash
brew install python@3.12
```

### 1.3 安装 Node.js

从 [官网](https://nodejs.org/) 下载 LTS 版本，或使用包管理器安装。

---

## 二、数据库配置

### 2.1 创建数据库和用户

```bash
# 以 postgres 用户登录数据库
psql -U postgres

# 执行以下 SQL
CREATE USER projectalpha_user WITH PASSWORD 'your_secure_password';
CREATE DATABASE projectalpha OWNER projectalpha_user;
GRANT ALL PRIVILEGES ON DATABASE projectalpha TO projectalpha_user;

# 创建测试数据库（可选）
CREATE DATABASE projectalpha_test OWNER projectalpha_user;

# 退出
\q
```

### 2.2 配置数据库连接

编辑 `backend/.env.production`：

```ini
DATABASE_URL=postgresql+asyncpg://projectalpha_user:your_secure_password@localhost:5432/projectalpha
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=False
CORS_ORIGINS=http://your-domain.com,http://127.0.0.1:80
LOG_LEVEL=WARNING
LOG_DIR=logs
LOG_MAX_BYTES=10485760
LOG_BACKUP_COUNT=5
```

> **安全提示**：请替换 `your_secure_password` 为实际密码，并将 `CORS_ORIGINS` 设置为实际的前端域名。

### 2.3 执行数据库迁移

```bash
cd backend

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 执行 Alembic 迁移
alembic upgrade head
```

---

## 三、后端部署

### 3.1 Windows 部署

#### 方法一：直接运行

```cmd
cd backend
venv\Scripts\activate
set ENV_FILE=.env.production
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

#### 方法二：使用 NSSM 注册 Windows 服务

1. 下载 NSSM：https://nssm.cc/download
2. 注册服务：

```cmd
nssm install projectalpha-backend
nssm set projectalpha-backend Application C:\Python312\python.exe
nssm set projectalpha-backend AppParameters -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
nssm set projectalpha-backend AppDirectory C:\projectalpha\backend
nssm set projectalpha_environment ENV_FILE .env.production
nssm set projectalpha-backend AppStdout C:\projectalpha\backend\logs\stdout.log
nssm set projectalpha-backend AppStderr C:\projectalpha\backend\logs\stderr.log
nssm start projectalpha-backend
```

### 3.2 Linux 部署

#### 使用 systemd 服务

1. 创建服务文件 `/etc/systemd/system/projectalpha-backend.service`：

```ini
[Unit]
Description=projectAlpha Backend Service
After=network.target postgresql.service

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/opt/projectalpha/backend
Environment=ENV_FILE=.env.production
ExecStart=/opt/projectalpha/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always
RestartSec=5

# 日志
StandardOutput=append:/opt/projectalpha/backend/logs/stdout.log
StandardError=append:/opt/projectalpha/backend/logs/stderr.log

[Install]
WantedBy=multi-user.target
```

2. 启用并启动服务：

```bash
sudo systemctl daemon-reload
sudo systemctl enable projectalpha-backend
sudo systemctl start projectalpha-backend
sudo systemctl status projectalpha-backend
```

---

## 四、前端部署

### 4.1 构建生产包

```bash
cd frontend

# 设置后端 API 地址
echo "VITE_API_BASE_URL=http://your-api-domain:8000" > .env.production

# 安装依赖并构建
npm install
npm run build
```

构建产物将输出到 `dist/` 目录。

### 4.2 使用 Nginx 部署

创建 Nginx 配置文件 `/etc/nginx/sites-available/projectalpha`：

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # 前端静态文件
    location / {
        root /opt/projectalpha/frontend/dist;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    # 后端 API 代理（可选，用于解决 CORS）
    location /api/ {
        proxy_pass http://127.0.0.1:8000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # 健康检查代理
    location /health {
        proxy_pass http://127.0.0.1:8000/health;
    }
}
```

启用站点：
```bash
sudo ln -s /etc/nginx/sites-available/projectalpha /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 4.3 使用 serve 快速部署

```bash
npm install -g serve
cd frontend
serve -s dist -l 80
```

---

## 五、数据备份

### Windows

```cmd
scripts\backup_database.bat
```

可通过 Windows 任务计划程序设置为每日自动执行。

### Linux

```bash
chmod +x scripts/backup_database.sh
sudo crontab -e
# 添加以下行实现每日凌晨 2 点自动备份
0 2 * * * /opt/projectalpha/scripts/backup_database.sh
```

### 手动备份

```bash
pg_dump -h localhost -U projectalpha_user -d projectalpha -F c -f backup.sql
```

### 恢复数据

```bash
pg_restore -h localhost -U projectalpha_user -d projectalpha backup.sql
```

---

## 六、验证部署

### 6.1 检查后端健康状态

```bash
curl http://127.0.0.1:8000/health
# 预期响应: {"status": "healthy", "database": "connected"}
```

### 6.2 检查前端

```bash
curl -I http://127.0.0.1:80
# 预期响应: HTTP/1.1 200 OK
```

### 6.3 功能测试

1. 打开浏览器访问 `http://your-domain.com`
2. 创建一条测试 Ticket
3. 添加标签
4. 验证筛选和搜索功能

---

## 七、运维管理

### 7.1 查看日志

```bash
# 后端日志
tail -f backend/logs/app.log

# Nginx 日志
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

### 7.2 服务管理

```bash
# 后端服务
sudo systemctl status projectalpha-backend
sudo systemctl restart projectalpha-backend
sudo systemctl stop projectalpha-backend

# Nginx
sudo systemctl status nginx
sudo systemctl restart nginx
```

### 7.3 数据库维护

```sql
-- 检查表大小
SELECT table_name, pg_size_pretty(pg_total_relation_size(table_name::text))
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY pg_total_relation_size(table_name::text) DESC;

-- 检查索引使用情况
SELECT schemaname, tablename, indexname, idx_scan
FROM pg_stat_user_indexes
ORDER BY idx_scan ASC;
```

---

## 八、故障排查

### 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| 连接数据库失败 | 密码错误或服务未启动 | 检查 `.env.production` 中 DATABASE_URL |
| CORS 错误 | 前端域名未配置 | 更新 CORS_ORIGINS |
| 端口占用 | 8000 端口已被占用 | `netstat -ano \| findstr :8000` 查看并关闭 |
| 前端白屏 | dist 目录未正确构建 | 执行 `npm run build` |
| API 404 | 路由未注册 | 检查 `app/main.py` 中路由注册 |

### 日志级别调整

如需详细调试日志，修改 `.env.production`：

```ini
LOG_LEVEL=DEBUG
```

---

## 九、安全建议

1. **数据库密码**：使用强密码，避免使用默认密码
2. **防火墙**：仅开放必要的端口（80/443），关闭 8000 端口的外网访问
3. **HTTPS**：使用 Let's Encrypt 免费证书启用 HTTPS
4. **Swagger UI**：生产环境已自动禁用 `/docs` 和 `/redoc`
5. **备份**：定期备份数据库，并验证备份可恢复
6. **依赖更新**：定期运行 `pip list --outdated` 和 `npm outdated` 更新依赖
