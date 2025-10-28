# 常见问题解答

本文档收集了开发过程中常见的问题和解决方案。

## 📋 目录

- [环境配置问题](#环境配置问题)
- [项目启动问题](#项目启动问题)
- [数据库问题](#数据库问题)
- [开发常见问题](#开发常见问题)
- [性能问题](#性能问题)
- [部署问题](#部署问题)

## 🔧 环境配置问题

### 1. Python 版本问题

**问题**：提示 "This application requires Python 3.10 or later"

**解决方案**：
```bash
# 检查当前 Python 版本
python3 --version

# 如果版本低于 3.10，安装新版本
brew install python@3.12

# 重新创建虚拟环境
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. 虚拟环境激活失败

**问题**：`source venv/bin/activate` 后提示找不到文件

**解决方案**：
```bash
# 检查虚拟环境是否存在
ls -la venv/

# 如果不存在，重新创建
python3 -m venv venv

# 再次激活
source venv/bin/activate
```

### 3. pip 安装速度慢

**问题**：安装依赖包时速度很慢，甚至超时

**解决方案**：
```bash
# 临时使用清华镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 永久配置镜像源
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
pip config set global.trusted-host pypi.tuna.tsinghua.edu.cn
```

### 4. 依赖包冲突

**问题**：安装依赖时提示版本冲突

**解决方案**：
```bash
# 升级 pip
pip install --upgrade pip

# 清理缓存
pip cache purge

# 重新安装依赖
pip install -r requirements.txt --no-cache-dir
```

## 🚀 项目启动问题

### 1. 环境配置文件不存在

**问题**：提示 "FileNotFoundError: 环境配置文件不存在"

**解决方案**：
```bash
# 检查配置文件是否存在
ls -la backend/env/.env.dev

# 如果不存在，创建文件
mkdir -p backend/env
touch backend/env/.env.dev

# 编辑配置文件（参考项目启动指南）
nano backend/env/.env.dev
```

### 2. 端口被占用

**问题**：提示 "Address already in use" 或端口 8000 被占用

**解决方案**：
```bash
# 查找占用端口的进程
lsof -i :8000

# 杀死进程
kill -9 <PID>

# 或者修改配置文件中的端口
# 编辑 env/.env.dev
SERVER_PORT=8001
```

### 3. 模块导入错误

**问题**：提示 "ModuleNotFoundError: No module named 'xxx'"

**解决方案**：
```bash
# 确保虚拟环境已激活
source venv/bin/activate

# 重新安装依赖
pip install -r requirements.txt

# 如果是本地模块导入错误，检查 PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:/path/to/project"
```

### 4. 启动服务后无法访问

**问题**：服务启动成功，但浏览器无法访问

**解决方案**：
```bash
# 检查防火墙设置
# macOS: 系统偏好设置 -> 安全性与隐私 -> 防火墙

# 检查服务器是否真的在监听
lsof -i :8000

# 尝试本地访问
curl http://localhost:8000/health

# 检查配置文件中的 HOST
# SERVER_HOST=0.0.0.0  # 允许所有 IP
# SERVER_HOST=127.0.0.1  # 仅本地访问
```

## 🗄️ 数据库问题

### 1. 数据库连接失败

**问题**：提示 "Could not connect to database"

**解决方案（MySQL）**：
```bash
# 检查 MySQL 服务是否运行
brew services list | grep mysql

# 如果没有运行，启动服务
brew services start mysql@8.0

# 测试连接
mysql -u root -p

# 检查用户权限
# 在 MySQL 中执行
SHOW GRANTS FOR 'your_user'@'localhost';
```

**解决方案（PostgreSQL）**：
```bash
# 检查 PostgreSQL 服务
brew services list | grep postgresql

# 启动服务
brew services start postgresql@15

# 测试连接
psql -d fastapiadmin
```

### 2. 数据库迁移失败

**问题**：`python3 main.py upgrade --env=dev` 失败

**解决方案**：
```bash
# 检查迁移文件
ls -la alembic/versions/

# 查看当前数据库版本
python3 main.py current --env=dev

# 强制同步到最新版本
alembic stamp head

# 或重新生成迁移文件
rm -rf alembic/versions/*.py
python3 main.py revision "重新初始化" --env=dev
python3 main.py upgrade --env=dev
```

### 3. 数据库字符编码问题

**问题**：中文显示为乱码

**解决方案**：
```bash
# 确保数据库使用 UTF-8 编码
# MySQL
CREATE DATABASE fastapiadmin CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 检查表的字符集
SHOW CREATE TABLE users;
```

### 4. 表已存在的错误

**问题**：提示 "Table 'xxx' already exists"

**解决方案**：
```bash
# 方法 1：删除旧表重新创建（仅开发环境）
# 使用 SQLite
rm fastapiadmin.db

# MySQL
mysql -u root -p
DROP DATABASE fastapiadmin;
CREATE DATABASE fastapiadmin CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 方法 2：回退迁移后重新执行
python3 main.py downgrade -1 --env=dev
python3 main.py upgrade --env=dev
```

## 💻 开发常见问题

### 1. 代码修改后不生效

**问题**：修改代码后重启服务，但改动不生效

**解决方案**：
```bash
# 检查是否正确启动了 reload 模式
# 启动命令应该包含 --reload
python3 main.py run --env=dev

# 或使用 uvicorn
uvicorn main:create_app --reload --host 0.0.0.0 --port 8000
```

### 2. IDE 提示找不到模块

**问题**：IDE 报错 "Cannot find module 'app'"

**解决方案**：
```bash
# 方法 1：配置 IDE 的 Python 解释器
# 选择 venv/bin/python

# 方法 2：添加项目根目录到 PYTHONPATH
# 在 VS Code 的 .vscode/settings.json 中
{
    "python.analysis.extraPaths": ["${workspaceFolder}/backend"]
}
```

### 3. 异步函数调用错误

**问题**：提示 "RuntimeWarning: coroutine was never awaited"

**原因**：忘记使用 await 调用异步函数

**解决方案**：
```python
# ❌ 错误
async def get_user():
    result = some_async_function()  # 缺少 await
    return result

# ✅ 正确
async def get_user():
    result = await some_async_function()
    return result
```

### 4. 类型检查错误

**问题**：mypy 报告类型错误

**解决方案**：
```python
# 使用类型注解
def get_user(user_id: int) -> Optional[User]:
    pass

# 使用类型忽略（谨慎使用）
result = some_function()  # type: ignore
```

## ⚡ 性能问题

### 1. 接口响应慢

**问题**：API 接口响应时间过长

**排查方法**：
```python
# 开启 SQL 日志查看数据库查询
# 在 env/.env.dev 中设置
DATABASE_ECHO=True

# 检查是否有 N+1 查询问题
# ❌ 避免
for article in articles:
    author = await get_author(article.author_id)

# ✅ 推荐
articles = await crud.list(preload=["author"])
```

**优化建议**：
1. 使用索引查询
2. 预加载关联数据
3. 实现缓存机制
4. 优化查询逻辑

### 2. 内存占用过高

**问题**：服务运行一段时间后内存占用持续增长

**解决方案**：
```bash
# 检查当前进程
ps aux | grep python

# 定期重启服务（生产环境）
# 使用进程管理工具
# supervisor, systemd 等
```

### 3. 数据库连接池耗尽

**问题**：提示 "Too many connections"

**解决方案**：
```python
# 在配置文件中增加连接池大小
POOL_SIZE=50
MAX_OVERFLOW=20

# 检查是否有连接未正确关闭
# 使用 async with 确保连接关闭
async with AsyncSessionLocal() as db:
    # 使用 db
    pass
```

## 🚢 部署问题

### 1. Docker 构建失败

**问题**：`docker build` 失败

**解决方案**：
```bash
# 检查 Dockerfile 是否正确
cat devops/backend/Dockerfile

# 清理旧镜像
docker image prune -a

# 重新构建
docker-compose build --no-cache
```

### 2. 容器启动失败

**问题**：容器启动后立即退出

**排查方法**：
```bash
# 查看容器日志
docker logs <container_id>

# 检查容器配置
docker-compose config

# 进入容器调试
docker exec -it <container_id> /bin/bash
```

### 3. 生产环境配置

**问题**：生产环境与开发环境配置不同

**解决方案**：
```bash
# 创建生产环境配置文件
cp env/.env.dev env/.env.prod

# 修改生产环境配置
nano env/.env.prod

# 使用生产配置启动
python3 main.py run --env=prod
```

## 📞 获取帮助

如果以上方案都无法解决您的问题：

1. **查看日志**：检查 `backend/logs/` 目录下的日志文件
2. **搜索 Issue**：在 [GitHub Issues](https://github.com/1014TaoTao/fastapi_vue3_admin/issues) 中搜索相似问题
3. **提交新 Issue**：详细描述问题，包含错误信息和环境信息
4. **联系社区**：加入技术交流群

## 🎯 快速排查清单

遇到问题时，按以下步骤排查：

- [ ] 检查 Python 版本是否 >= 3.10
- [ ] 确认虚拟环境已激活
- [ ] 确认所有依赖已安装
- [ ] 检查环境配置文件是否存在
- [ ] 查看日志文件中的错误信息
- [ ] 尝试重启服务
- [ ] 检查数据库服务是否运行
- [ ] 确认端口未被占用

## 💡 预防措施

避免常见问题的最佳实践：

1. **使用虚拟环境**：避免污染系统 Python
2. **版本固定**：在 requirements.txt 中固定版本号
3. **定期备份**：重要数据定期备份
4. **代码审查**：提交前进行代码审查
5. **测试驱动**：编写测试确保功能正常
6. **文档完善**：及时更新文档

---

**希望这份文档能帮助您快速解决问题！** 🎉

