# Python 开发教程

本教程专为 Python 新手设计，结合项目实际应用，快速掌握 Python 开发技能。

## 📋 目录

- [Python 基础语法](#python-基础语法)
- [项目中的 Python 用法](#项目中的-python-用法)
- [FastAPI 核心概念](#fastapi-核心概念)
- [异步编程](#异步编程)
- [数据验证和序列化](#数据验证和序列化)
- [实战案例](#实战案例)

## 🐍 Python 基础语法

### 1. 变量和数据类型

```python
# Python 是动态类型语言，无需声明类型
name = "张三"              # 字符串
age = 25                  # 整数
height = 175.5           # 浮点数
is_student = True        # 布尔值

# 变量命名规范：使用小写字母和下划线
user_name = "admin"
order_id = 12345

# Python 内置类型
numbers = [1, 2, 3]      # 列表
user = {"name": "张三", "age": 25}  # 字典
```

### 2. 函数定义

```python
# 基础函数
def greet(name):
    """问候函数"""
    return f"你好，{name}!"

# 带类型提示的函数（Python 3.5+）
def add(a: int, b: int) -> int:
    """
    加法函数
    
    参数:
    - a: 第一个数字
    - b: 第二个数字
    
    返回:
    - 两数之和
    """
    return a + b

# 调用函数
result = add(1, 2)
print(result)  # 输出: 3
```

### 3. 类定义

```python
# 定义类
class User:
    """用户类"""
    
    def __init__(self, name: str, age: int):
        """初始化方法"""
        self.name = name
        self.age = age
    
    def get_info(self) -> str:
        """获取用户信息"""
        return f"{self.name}, {self.age}岁"

# 创建对象
user = User("张三", 25)
print(user.get_info())  # 输出: 张三, 25岁
```

### 4. 字典和列表操作

```python
# 列表操作
users = ["张三", "李四", "王五"]
users.append("赵六")        # 添加元素
users.remove("李四")        # 删除元素
print(users[0])             # 获取第一个: 张三

# 字典操作
user_info = {
    "name": "张三",
    "age": 25,
    "email": "zhangsan@example.com"
}
print(user_info["name"])   # 获取值: 张三
user_info["phone"] = "13800138000"  # 添加键值对

# 遍历
for user in users:
    print(user)

for key, value in user_info.items():
    print(f"{key}: {value}")
```

### 5. 异常处理

```python
try:
    # 可能出错的代码
    result = 10 / 0
except ZeroDivisionError:
    # 处理异常
    print("除数不能为零")
except Exception as e:
    # 处理其他异常
    print(f"发生错误: {e}")
finally:
    # 无论是否出错都会执行
    print("清理工作")
```

## 📁 项目中的 Python 用法

### 1. 模块导入

```python
# 标准库导入
from datetime import datetime
import json

# 第三方库导入
from fastapi import FastAPI, Depends
from sqlalchemy import select

# 本地模块导入
from app.core.database import AsyncSessionLocal
from app.api.v1.module_system.user.model import UserModel
```

### 2. 类型提示（Type Hints）

```python
from typing import List, Dict, Optional

# 函数类型提示
def get_users() -> List[Dict]:
    """返回用户列表"""
    return [{"name": "张三"}, {"name": "李四"}]

# 变量类型提示
user_list: List[str] = ["张三", "李四"]
user_info: Optional[Dict] = None
```

### 3. 异步编程基础

```python
import asyncio

# 定义异步函数
async def fetch_user(user_id: int) -> dict:
    """异步获取用户"""
    # 模拟异步操作
    await asyncio.sleep(1)
    return {"id": user_id, "name": "张三"}

# 调用异步函数
async def main():
    user = await fetch_user(1)
    print(user)

# 运行异步函数
# asyncio.run(main())
```

## 🚀 FastAPI 核心概念

### 1. 路由定义

```python
from fastapi import APIRouter

# 创建路由
router = APIRouter(prefix="/users", tags=["用户管理"])

@router.get("", summary="获取用户列表")
async def get_users():
    """获取所有用户"""
    return {"users": []}

@router.post("", summary="创建用户")
async def create_user():
    """创建新用户"""
    return {"msg": "创建成功"}
```

### 2. 路径参数和查询参数

```python
from fastapi import Path, Query

# 路径参数
@router.get("/{user_id}")
async def get_user(user_id: int = Path(..., description="用户ID")):
    """获取单个用户"""
    return {"user_id": user_id}

# 查询参数
@router.get("")
async def search_users(
    page: int = Query(1, description="页码"),
    size: int = Query(10, description="每页数量")
):
    """搜索用户"""
    return {"page": page, "size": size}
```

### 3. 请求体

```python
from pydantic import BaseModel

# 定义请求模型
class CreateUserRequest(BaseModel):
    """创建用户请求"""
    name: str
    email: str
    age: int

# 使用请求体
@router.post("")
async def create_user(data: CreateUserRequest):
    """创建用户"""
    return {"name": data.name}
```

### 4. 依赖注入

```python
from fastapi import Depends

# 定义依赖
def get_db():
    """获取数据库连接"""
    return "db_connection"

# 使用依赖
@router.get("")
async def get_users(db = Depends(get_db)):
    """获取用户列表"""
    return {"db": db}
```

## ⚡ 异步编程

### 1. async/await 基础

```python
import asyncio
from datetime import datetime

# 同步函数
def sync_function():
    """同步函数"""
    print(f"开始: {datetime.now()}")
    # 模拟耗时操作
    time.sleep(1)
    print(f"结束: {datetime.now()}")

# 异步函数
async def async_function():
    """异步函数"""
    print(f"开始: {datetime.now()}")
    # 模拟耗时操作
    await asyncio.sleep(1)
    print(f"结束: {datetime.now()}")

# 运行异步函数
# asyncio.run(async_function())
```

### 2. 并发执行

```python
import asyncio

async def fetch_data(url: str) -> dict:
    """异步获取数据"""
    await asyncio.sleep(0.5)  # 模拟网络请求
    return {"url": url, "data": "result"}

async def main():
    """并发执行多个异步任务"""
    urls = ["url1", "url2", "url3"]
    
    # 并发执行
    tasks = [fetch_data(url) for url in urls]
    results = await asyncio.gather(*tasks)
    
    print(results)
```

### 3. 项目中的异步用法

```python
from sqlalchemy.ext.asyncio import AsyncSession

class UserService:
    """用户服务"""
    
    async def get_user(self, db: AsyncSession, user_id: int):
        """异步获取用户"""
        # 异步数据库查询
        result = await db.execute(
            select(UserModel).filter(UserModel.id == user_id)
        )
        return result.scalar_one_or_none()
```

## ✅ 数据验证和序列化

### 1. Pydantic 模型

```python
from pydantic import BaseModel, Field, validator

class UserCreateSchema(BaseModel):
    """创建用户模型"""
    
    # 必填字段
    name: str = Field(..., description="用户名", min_length=2, max_length=50)
    
    # 可选字段
    email: Optional[str] = Field(None, description="邮箱")
    
    # 自定义验证器
    @validator('name')
    def validate_name(cls, v):
        if 'admin' in v.lower():
            raise ValueError('用户名不能包含 admin')
        return v
    
    class Config:
        """配置"""
        from_attributes = True
```

### 2. 使用 Schema 验证数据

```python
# 创建对象
user_data = UserCreateSchema(name="张三", email="zhangsan@example.com")

# 转换为字典
user_dict = user_data.dict()

# 转换为 JSON
user_json = user_data.json()
```

## 🎯 实战案例

### 案例 1: 简单的用户管理接口

```python
from fastapi import APIRouter, Depends
from typing import List

router = APIRouter(prefix="/api/users", tags=["用户"])

# 模拟数据库
fake_users_db = [
    {"id": 1, "name": "张三", "age": 25},
    {"id": 2, "name": "李四", "age": 30},
]

@router.get("", summary="获取用户列表")
async def get_users() -> List[dict]:
    """获取所有用户"""
    return fake_users_db

@router.get("/{user_id}", summary="获取用户详情")
async def get_user(user_id: int):
    """根据 ID 获取用户"""
    for user in fake_users_db:
        if user["id"] == user_id:
            return user
    return {"error": "用户不存在"}

@router.post("", summary="创建用户")
async def create_user(name: str, age: int):
    """创建新用户"""
    new_user = {
        "id": len(fake_users_db) + 1,
        "name": name,
        "age": age
    }
    fake_users_db.append(new_user)
    return {"msg": "创建成功", "user": new_user}
```

### 案例 2: 使用数据库的真实接口

```python
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import async_db_session
from app.api.v1.module_system.user.model import UserModel

@router.get("", summary="获取用户列表")
async def get_users(db: AsyncSession = Depends(async_db_session)):
    """获取所有用户（实际项目用法）"""
    
    # 查询数据库
    result = await db.execute(select(UserModel))
    users = result.scalars().all()
    
    # 转换为字典
    return [{"id": u.id, "name": u.name} for u in users]
```

## 📚 进阶学习

### 1. 列表推导式

```python
# 传统方式
numbers = [1, 2, 3, 4, 5]
squares = []
for n in numbers:
    squares.append(n * n)

# 使用列表推导式
squares = [n * n for n in numbers]

# 带条件
even_squares = [n * n for n in numbers if n % 2 == 0]
```

### 2. 字典推导式

```python
# 创建字典
user_info = {f"user_{i}": i*10 for i in range(1, 6)}
# 结果: {'user_1': 10, 'user_2': 20, ...}

# 条件过滤
filtered = {k: v for k, v in user_info.items() if v > 20}
```

### 3. 装饰器

```python
def logger(func):
    """日志装饰器"""
    def wrapper(*args, **kwargs):
        print(f"调用函数: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@logger
def add(a, b):
    return a + b

result = add(1, 2)
# 输出: 调用函数: add
```

## 💡 学习资源

- **官方文档**: https://docs.python.org/zh-cn/3/
- **FastAPI 文档**: https://fastapi.tiangolo.com/
- **SQLAlchemy 文档**: https://docs.sqlalchemy.org/

## ✅ 练习任务

1. **基础题**：编写一个计算器类，支持加减乘除
2. **进阶题**：创建一个异步函数，模拟从多个 API 获取数据
3. **实战题**：实现一个简单的博客文章 CRUD 接口

## 📝 下一步

掌握了 Python 基础后，您可以：

1. 🎯 开发 [API 接口](./04-api-development-guide.md)
2. 🔧 了解 [最佳实践](./06-best-practices.md)
3. 🗄️ 深入学习 [数据库操作](./03-database-setup-guide.md)

---

**恭喜！您已经掌握了 Python 开发的基础技能！** 🎉

