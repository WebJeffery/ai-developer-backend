# 数据库安装配置指南

本指南将帮助您安装和配置项目支持的三种数据库：SQLite、MySQL 和 PostgreSQL。

## 📋 目录

- [数据库选择建议](#数据库选择建议)
- [SQLite 配置](#sqlite-配置)（最简单，推荐新手）
- [MySQL 配置](#mysql-配置)
- [PostgreSQL 配置](#postgresql-配置)
- [数据库开发技巧](#数据库开发技巧)
- [常见问题](#常见问题)

## 🎯 数据库选择建议

### SQLite（推荐新手）
- ✅ **优点**：无需安装，零配置
- ✅ **适用场景**：开发测试、小型项目
- ⚠️ **限制**：不支持并发写入

### MySQL（生产推荐）
- ✅ **优点**：性能好，生态完善
- ✅ **适用场景**：生产环境
- ⚠️ **需要**：单独安装数据库服务

### PostgreSQL（高级推荐）
- ✅ **优点**：功能强大，扩展性好
- ✅ **适用场景**：复杂业务场景
- ⚠️ **需要**：单独安装数据库服务

## 💾 SQLite 配置

SQLite 是最简单的选择，无需单独安装数据库服务。

### 1. 修改配置文件

编辑 `backend/env/.env.dev`：

```env
# 数据库配置
SQL_DB_ENABLE=True
DATABASE_TYPE=sqlite
DATABASE_ECHO=False
ECHO_POOL=False
DATABASE_HOST=
DATABASE_PORT=
DATABASE_USER=
DATABASE_PASSWORD=
DATABASE_NAME=fastapiadmin
```

### 2. 初始化数据库

```bash
# 生成迁移文件
python3 main.py revision "初始化数据库" --env=dev

# 应用迁移
python3 main.py upgrade --env=dev
```

### 3. 验证

```bash
# 查看生成的数据库文件
ls -lh backend/*.db

# 使用 sqlite3 命令行工具查看
sqlite3 backend/fastapiadmin.db ".tables"

# 查看某个表的数据
sqlite3 backend/fastapiadmin.db "SELECT * FROM users LIMIT 5;"
```

**完成！** SQLite 配置成功，可以直接启动项目。

## 🗄️ MySQL 配置

### 1. 安装 MySQL

```bash
# 使用 Homebrew 安装
brew install mysql@8.0

# 启动 MySQL 服务
brew services start mysql@8.0

# 验证服务状态
brew services list | grep mysql
```

### 2. 创建数据库和用户

```bash
# 连接到 MySQL
mysql -u root -p

# 在 MySQL 命令行中执行
CREATE DATABASE fastapiadmin CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 创建用户（可选）
CREATE USER 'fastapi'@'localhost' IDENTIFIED BY 'your_password';

# 授权
GRANT ALL PRIVILEGES ON fastapiadmin.* TO 'fastapi'@'localhost';
FLUSH PRIVILEGES;

# 退出
EXIT;
```

### 3. 修改配置文件

编辑 `backend/env/.env.dev`：

```env
# 数据库配置
SQL_DB_ENABLE=True
DATABASE_TYPE=mysql
DATABASE_ECHO=False
ECHO_POOL=False
DATABASE_HOST=localhost
DATABASE_PORT=3306
DATABASE_USER=root              # 或 fastapi
DATABASE_PASSWORD=your_password
DATABASE_NAME=fastapiadmin
```

### 4. 初始化数据库

```bash
# 生成迁移文件
python3 main.py revision "初始化数据库" --env=dev

# 应用迁移
python3 main.py upgrade --env=dev
```

### 5. 验证

```bash
# 连接数据库查看表
mysql -u root -p fastapiadmin

# 在 MySQL 中
SHOW TABLES;
SELECT * FROM users LIMIT 5;
EXIT;
```

## 🐘 PostgreSQL 配置

### 1. 安装 PostgreSQL

```bash
# 使用 Homebrew 安装
brew install postgresql@15

# 启动服务
brew services start postgresql@15

# 验证服务状态
brew services list | grep postgresql
```

### 2. 创建数据库和用户

```bash
# 创建数据库
createdb fastapiadmin

# 或使用 psql 命令
psql postgres

# 在 psql 中
CREATE DATABASE fastapiadmin;
CREATE USER fastapi WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE fastapiadmin TO fastapi;
\q
```

### 3. 修改配置文件

编辑 `backend/env/.env.dev`：

```env
# 数据库配置
SQL_DB_ENABLE=True
DATABASE_TYPE=postgresql
DATABASE_ECHO=False
ECHO_POOL=False
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_USER=postgres          # 或 fastapi
DATABASE_PASSWORD=your_password
DATABASE_NAME=fastapiadmin
```

### 4. 初始化数据库

```bash
# 生成迁移文件
python3 main.py revision "初始化数据库" --env=dev

# 应用迁移
python3 main.py upgrade --env=dev
```

### 5. 验证

```bash
# 连接数据库查看表
psql -d fastapiadmin

# 在 psql 中
\dt
SELECT * FROM users LIMIT 5;
\q
```

## 🔧 数据库开发技巧

### 1. 使用 Alembic 管理数据库变更

#### 生成新的迁移文件

```bash
# 修改模型后，自动检测变更并生成迁移文件
python3 main.py revision "添加新字段" --env=dev
```

#### 应用迁移

```bash
# 应用到数据库
python3 main.py upgrade --env=dev
```

#### 回滚迁移

```bash
# 回退到上一个版本
python3 main.py downgrade -1 --env=dev

# 回退到指定版本
python3 main.py downgrade <revision_id> --env=dev
```

#### 查看迁移历史

```bash
# 查看所有迁移版本
python3 main.py history --env=dev

# 查看当前版本
python3 main.py current --env=dev
```

### 2. 数据库查询工具

#### 使用 SQLite3 命令行

```bash
# 打开数据库
sqlite3 backend/fastapiadmin.db

# 常用命令
.tables              # 列出所有表
.schema users        # 查看表结构
SELECT * FROM users; # 查询数据
.headers on          # 显示列头
.mode column         # 列模式显示
```

#### 使用 MySQL 命令行

```bash
# 连接数据库
mysql -u root -p fastapiadmin

# 常用命令
SHOW TABLES;                        # 列出所有表
DESCRIBE users;                     # 查看表结构
SELECT * FROM users LIMIT 10;       # 查询数据
```

#### 使用 PostgreSQL 命令行

```bash
# 连接数据库
psql -d fastapiadmin

# 常用命令
\dt                    # 列出所有表
\d users              # 查看表结构
SELECT * FROM users;  # 查询数据
\q                    # 退出
```

### 3. 使用可视化工具

推荐使用图形化工具管理数据库：

- **TablePlus**（macOS，推荐）
- **DBeaver**（跨平台）
- **MySQL Workbench**（仅 MySQL）
- **pgAdmin**（仅 PostgreSQL）

### 4. 备份和恢复数据库

#### SQLite

```bash
# 备份
cp fastapiadmin.db fastapiadmin.db.bak

# 恢复
cp fastapiadmin.db.bak fastapiadmin.db
```

#### MySQL

```bash
# 备份
mysqldump -u root -p fastapiadmin > backup.sql

# 恢复
mysql -u root -p fastapiadmin < backup.sql
```

#### PostgreSQL

```bash
# 备份
pg_dump -U postgres fastapiadmin > backup.sql

# 恢复
psql -U postgres fastapiadmin < backup.sql
```

## 🎯 项目中的数据库配置

### 查看配置文件

项目数据库配置在 `app/config/setting.py`：

```python
# 数据库类型
DATABASE_TYPE: Literal['sqlite','mysql', 'postgresql']

# 连接池配置
POOL_SIZE: int = 20                    # 连接池大小
MAX_OVERFLOW: int = 10                   # 最大溢出连接数
POOL_TIMEOUT: int = 30                  # 连接超时时间(秒)
POOL_RECYCLE: int = 1800                # 连接回收时间(秒)
POOL_PRE_PING: bool = True              # 连接预检

# SQL 日志
DATABASE_ECHO: bool = False             # 显示 SQL 日志（调试时设为 True）
```

### 在代码中使用数据库

```python
from app.core.database import async_db_session
from app.api.v1.module_system.user.model import UserModel

# 在 Service 或 Controller 中使用
async def get_user(db: AsyncSession, user_id: int):
    """获取用户信息"""
    result = await db.execute(
        select(UserModel).filter(UserModel.id == user_id)
    )
    return result.scalar_one_or_none()
```

## ❗ 常见问题

### 1. MySQL 连接失败

**错误信息**：`Access denied for user 'root'@'localhost'`

**解决方案**：
```bash
# 重置密码
mysql -u root -p
ALTER USER 'root'@'localhost' IDENTIFIED BY 'new_password';
```

### 2. PostgreSQL 连接失败

**错误信息**：`FATAL: password authentication failed`

**解决方案**：
```bash
# 编辑配置文件
nano /opt/homebrew/var/postgresql@15/pg_hba.conf

# 修改认证方式为 md5 或 trust
local   all   all   md5
host    all   all   127.0.0.1/32   md5

# 重启服务
brew services restart postgresql@15
```

### 3. 数据库迁移失败

**错误信息**：`alembic.util.exc.CommandError: Target database is not up to date`

**解决方案**：
```bash
# 强制同步到当前版本
alembic stamp head

# 或重新生成迁移
rm -rf alembic/versions/*
python3 main.py revision "重新初始化" --env=dev
python3 main.py upgrade --env=dev
```

### 4. 字符编码问题

**确保数据库使用 UTF-8 编码**：

```bash
# MySQL
CREATE DATABASE fastapiadmin CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# PostgreSQL
CREATE DATABASE fastapiadmin WITH ENCODING = 'UTF8';
```

## 📝 下一步

数据库配置完成后，您可以：

1. 📖 学习 [接口开发指南](./04-api-development-guide.md)
2. 🎓 阅读 [Python 开发教程](./05-python-tutorial.md)
3. 🔧 查看 [最佳实践](./06-best-practices.md)

---

**数据库配置完成！现在可以开始开发了！** 🚀

