# 项目启动指南

本指南将帮您在 5 分钟内启动 FastAPI-Vue3-Admin 后端项目。

## 📋 目录

- [前置准备](#前置准备)
- [配置环境变量](#配置环境变量)
- [初始化数据库](#初始化数据库)
- [启动项目](#启动项目)
- [验证运行](#验证运行)
- [快速启动脚本](#快速启动脚本)

## ✅ 前置准备

在开始之前，请确保：

- ✅ Python 3.10+ 已安装
- ✅ 虚拟环境已创建并激活
- ✅ 项目依赖已安装（详见 [Python 环境搭建](./01-python-environment-setup.md)）

## ⚙️ 配置环境变量

### 步骤 1：创建配置目录

```bash
# 进入项目目录
cd /Users/zhifeixie/my-github/ai-developer-backend/backend

# 创建配置目录
mkdir -p env
```

### 步骤 2：创建环境配置文件

创建 `env/.env.dev` 文件：

```bash
# 创建文件
touch env/.env.dev
```

### 步骤 3：编辑配置文件

使用您喜欢的编辑器打开 `env/.env.dev`，复制以下配置：

#### 使用 SQLite（最简单，推荐新手）

```env
# ==================== 环境配置 ====================
ENVIRONMENT=dev

# ==================== 服务器配置 ====================
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
RELOAD=True
FACTORY=True
LIFESPAN=on
WORKERS=1
LIMIT_CONCURRENCY=1000
BACKLOG=2048
LIMIT_MAX_REQUESTS=1000
TIMEOUT_KEEP_ALIVE=5

# ==================== API文档配置 ====================
DEBUG=True
TITLE=Fastapi-Vue3-Admin
VERSION=v1.0.0
DESCRIPTION=FastAPI + Vue3 快速开发框架
SUMMARY=一个现代化的快速开发平台
DOCS_URL=/docs
REDOC_URL=/redoc
ROOT_PATH=

# ==================== 数据库配置 ====================
SQL_DB_ENABLE=True
DATABASE_ECHO=False
ECHO_POOL=False
DATABASE_TYPE=sqlite
DATABASE_HOST=
DATABASE_PORT=
DATABASE_USER=
DATABASE_PASSWORD=
DATABASE_NAME=fastapiadmin

# ==================== MongoDB配置（禁用）====================
MONGO_DB_ENABLE=False
MONGO_DB_USER=
MONGO_DB_PASSWORD=
MONGO_DB_HOST=
MONGO_DB_PORT=
MONGO_DB_NAME=

# ==================== Redis配置（可选）====================
REDIS_ENABLE=False
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB_NAME=0
REDIS_USER=
REDIS_PASSWORD=

# ==================== AI大模型配置 ====================
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_API_KEY=sk-placeholder
OPENAI_MODEL=gpt-3.5-turbo
```

#### 使用 MySQL（生产环境推荐）

修改数据库部分配置：

```env
# 数据库配置
DATABASE_TYPE=mysql
DATABASE_HOST=localhost
DATABASE_PORT=3306
DATABASE_USER=root
DATABASE_PASSWORD=your_password
DATABASE_NAME=fastapiadmin
```

## 🗄️ 初始化数据库

### 步骤 1：生成数据库迁移文件

```bash
# 确保虚拟环境已激活
source venv/bin/activate

# 生成迁移文件
python3 main.py revision "初始化数据库" --env=dev
```

**输出示例**：
```bash
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.autogenerate.compare] Detected added table 'users'
INFO  [alembic.autogenerate.compare] Detected added table 'roles'
...
生成迁移文件: 初始化数据库
```

### 步骤 2：应用数据库迁移

```bash
# 应用迁移，创建数据库表结构
python3 main.py upgrade --env=dev
```

**输出示例**：
```bash
INFO  [alembic.runtime.migration] Running upgrade  -> revision_id, 初始化数据库
数据库迁移完成
```

### 步骤 3：验证数据库文件

```bash
# 如果使用 SQLite，会生成 .db 文件
ls -lh backend/*.db

# 或者查看数据库文件
ls -lh backend/fastapiadmin.db
```

## 🚀 启动项目

### 方法一：使用项目启动命令（推荐）

```bash
# 确保在项目根目录
cd /Users/zhifeixie/my-github/ai-developer-backend/backend

# 激活虚拟环境
source venv/bin/activate

# 启动开发服务器
python3 main.py run --env=dev
```

**成功启动后，您会看到：**
```
INFO:     Started server process [xxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### 方法二：使用 uvicorn 直接启动

```bash
uvicorn main:create_app --host 0.0.0.0 --port 8000 --reload
```

### 启动日志解读

当您看到以下日志时，说明启动成功：

```
# 项目 Banner
 ______        _                  _ 
|  ____|      | |     /\         (_)
...

# 数据库初始化
✅️ 初始化 sqlite 数据库初始化完成...
✅️ 初始化全局事件完成...
✅️ 初始化Redis系统配置完成...
✅️ 初始化Redis数据字典完成...
✅️ 初始化定时任务完成...
✅️ Fastapi-Vue3-Admin 服务成功启动...

# 服务器信息
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

## ✅ 验证运行

### 1. 访问 API 文档

打开浏览器，访问：

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 2. 健康检查接口

```bash
# 测试健康检查接口
curl http://localhost:8000/health

# 预期响应
{"code": 200, "msg": "success"}
```

### 3. 测试获取验证码接口

```bash
# 获取验证码
curl http://localhost:8000/api/v1/auth/captcha

# 应该返回验证码图片数据
```

### 4. 测试登录接口

```bash
# 先获取验证码
curl -o /tmp/captcha.png http://localhost:8000/api/v1/auth/captcha

# 使用默认账号登录（用户名：admin，密码：123456）
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "123456",
    "code": "1234",
    "uuid": "test-uuid"
  }'

# 应该返回 JWT token
```

## 🔧 快速启动脚本

为了更方便启动项目，我们可以创建一个启动脚本：

### 创建启动脚本

```bash
# 创建启动脚本
cat > backend/start.sh << 'EOF'
#!/bin/bash

# 切换到项目目录
cd "$(dirname "$0")"

# 激活虚拟环境
if [ ! -d "venv" ]; then
    echo "❌ 错误: 虚拟环境不存在，请先创建"
    echo "运行命令: python3 -m venv venv"
    exit 1
fi

source venv/bin/activate

# 检查环境配置文件
if [ ! -f "env/.env.dev" ]; then
    echo "❌ 错误: 环境配置文件不存在"
    echo "请创建 env/.env.dev 文件"
    exit 1
fi

# 启动服务
echo "🚀 正在启动 FastAPI 服务..."
python3 main.py run --env=dev
EOF

# 赋予执行权限
chmod +x backend/start.sh
```

### 使用启动脚本

```bash
# 直接在 backend 目录运行
./start.sh

# 或者在项目根目录
cd backend && ./start.sh
```

## 📊 项目启动流程

```
1. 加载环境配置 (env/.env.dev)
   ↓
2. 初始化 FastAPI 应用
   ↓
3. 注册中间件（CORS、日志、压缩）
   ↓
4. 注册路由和 API
   ↓
5. 初始化数据库连接
   ↓
6. 加载系统配置到 Redis
   ↓
7. 启动定时任务调度器
   ↓
8. 启动 Uvicorn 服务器
   ↓
9. ✅ 服务启动成功！
```

## 🎯 启动成功清单

- [ ] 环境配置文件已创建
- [ ] 数据库迁移已完成
- [ ] 服务器成功启动
- [ ] 可以访问 API 文档
- [ ] 健康检查接口正常
- [ ] 可以获取验证码

## 🛑 停止服务

要停止正在运行的服务：

```bash
# 在运行服务的终端窗口按
Ctrl + C

# 或者如果服务在后台运行
pkill -f "python3 main.py"
```

## ❗ 常见问题

### 1. 提示 "环境配置文件不存在"

**原因**：未创建 `.env.dev` 文件

**解决**：参考[配置环境变量](#配置环境变量)章节创建文件

### 2. 数据库连接失败

**原因**：数据库配置错误或数据库未启动

**解决**：
- SQLite：检查文件权限
- MySQL：确保数据库服务已启动，密码正确

### 3. 端口 8000 已被占用

**解决**：修改配置文件中的 `SERVER_PORT=8000` 为其他端口

```bash
# 查找占用 8000 端口的进程
lsof -i :8000

# 杀死进程
kill -9 <PID>
```

### 4. 提示 "ModuleNotFoundError"

**原因**：未安装依赖或虚拟环境未激活

**解决**：
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### 5. 数据库迁移失败

**解决**：
```bash
# 删除旧的数据库文件
rm fastapiadmin.db

# 重新生成并应用迁移
python3 main.py revision "重新初始化" --env=dev
python3 main.py upgrade --env=dev
```
