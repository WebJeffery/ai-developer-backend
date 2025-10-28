# Python 开发最佳实践

本指南总结了 Python 和 FastAPI 开发中的最佳实践，帮助您写出高质量、可维护的代码。

## 📋 目录

- [代码规范](#代码规范)
- [命名规范](#命名规范)
- [函数设计](#函数设计)
- [错误处理](#错误处理)
- [注释和文档](#注释和文档)
- [性能优化](#性能优化)
- [安全实践](#安全实践)

## 📝 代码规范

### 1. PEP 8 编码规范

遵循 Python 官方的 PEP 8 编码规范：

```python
# ✅ 推荐：使用 4 个空格缩进
def example():
    print("Hello")
    if True:
        print("World")

# ❌ 不推荐：使用 tab 或 2 个空格
def example():
  print("Hello")

# ✅ 推荐：行长度不超过 100 字符
result = very_long_function_name(
    parameter1, 
    parameter2, 
    parameter3
)

# ✅ 推荐：使用空行分隔逻辑块
def create_user():
    """创建用户"""
    
    # 验证数据
    validate_data()
    
    # 保存到数据库
    save_to_db()
```

### 2. 导入顺序

```python
# ✅ 标准库导入（第一组）
import os
from datetime import datetime
from typing import List, Dict

# ✅ 第三方库导入（第二组）
from fastapi import APIRouter, Depends
from sqlalchemy import select

# ✅ 本地模块导入（第三组）
from app.core.database import AsyncSessionLocal
from app.api.v1.module_system.user.model import UserModel
```

### 3. 类型提示

始终使用类型提示，提高代码可读性和 IDE 支持：

```python
# ✅ 推荐：使用类型提示
def get_user(user_id: int) -> dict:
    """获取用户"""
    return {"id": user_id, "name": "张三"}

# ❌ 不推荐：无类型提示
def get_user(user_id):
    return {"id": user_id, "name": "张三"}
```

## 🏷️ 命名规范

### 1. 变量和函数命名

```python
# ✅ 使用小写字母和下划线
user_name = "张三"
order_id = 12345
is_active = True

def get_user_info():
    pass

def create_order():
    pass

# ❌ 不推荐
userName = "张三"
orderId = 12345
def getUserInfo():
    pass
```

### 2. 类命名

```python
# ✅ 使用 PascalCase
class UserService:
    pass

class ArticleController:
    pass

# ❌ 不推荐
class userService:
    pass
```

### 3. 常量命名

```python
# ✅ 使用大写字母和下划线
MAX_RETRY_COUNT = 3
DEFAULT_PAGE_SIZE = 10
API_BASE_URL = "https://api.example.com"

# ❌ 不推荐
max_retry_count = 3
```

### 4. 私有成员

```python
class User:
    """用户类"""
    
    def __init__(self):
        self.name = "张三"          # 公共属性
        self._age = 25              # 受保护属性
        self.__password = "***"     # 私有属性
    
    def public_method(self):
        """公共方法"""
        pass
    
    def _protected_method(self):
        """受保护方法"""
        pass
    
    def __private_method(self):
        """私有方法"""
        pass
```

## 🔧 函数设计

### 1. 单一职责原则

```python
# ✅ 推荐：每个函数只做一件事
def calculate_total(price: float, quantity: int) -> float:
    """计算总价"""
    return price * quantity

def apply_discount(total: float, discount: float) -> float:
    """应用折扣"""
    return total * (1 - discount)

def process_order(price: float, quantity: int, discount: float):
    """处理订单"""
    total = calculate_total(price, quantity)
    final_price = apply_discount(total, discount)
    return final_price

# ❌ 不推荐：一个函数做多件事
def process_order(price, quantity, discount):
    """计算、应用折扣、保存订单"""
    total = price * quantity
    final = total * (1 - discount)
    save_to_db(...)
    send_email(...)
    return final
```

### 2. 参数设计

```python
# ✅ 推荐：使用有意义的默认值
def get_users(page: int = 1, size: int = 10):
    """获取用户列表"""
    pass

# ✅ 推荐：使用关键字参数
create_user(name="张三", email="xxx@example.com", age=25)

# ❌ 不推荐：参数过多
def create_user(name, email, age, phone, address, city, country):
    pass
```

### 3. 返回值设计

```python
# ✅ 推荐：返回有意义的对象
class User:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

def get_user(user_id: int) -> Optional[User]:
    """获取用户"""
    # 返回 User 对象或 None
    if user_exists:
        return User(name="张三", email="xxx@example.com")
    return None

# ❌ 不推荐：返回原始数据
def get_user(user_id: int) -> dict:
    return {"name": "张三", "email": "xxx@example.com"}
```

## ⚠️ 错误处理

### 1. 使用自定义异常

```python
from app.core.exceptions import CustomException

# ✅ 推荐：抛出明确的异常
def get_user(user_id: int):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise CustomException(msg=f"用户不存在，ID: {user_id}")
    return user

# ❌ 不推荐：使用通用异常
def get_user(user_id: int):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise Exception("用户不存在")  # 信息不够明确
    return user
```

### 2. 异常处理模式

```python
# ✅ 推荐：具体的异常处理
try:
    user = get_user(user_id)
except CustomException as e:
    # 处理业务异常
    logger.error(f"业务异常: {e.msg}")
    return {"error": e.msg}
except Exception as e:
    # 处理系统异常
    logger.error(f"系统异常: {str(e)}")
    return {"error": "系统错误"}

# ❌ 不推荐：捕获所有异常
try:
    user = get_user(user_id)
except:
    return {"error": "错误"}  # 不知道是什么错误
```

### 3. 日志记录

```python
from app.core.logger import logger

# ✅ 推荐：记录关键操作
async def create_user(data: UserCreateSchema):
    """创建用户"""
    logger.info(f"开始创建用户: {data.name}")
    
    try:
        user = await db.create_user(data)
        logger.info(f"用户创建成功: {user.id}")
        return user
    except Exception as e:
        logger.error(f"用户创建失败: {str(e)}")
        raise
```

## 📖 注释和文档

### 1. 函数文档字符串（Docstring）

```python
def calculate_total(price: float, quantity: int, discount: float = 0.0) -> float:
    """
    计算订单总价
    
    参数:
    - price (float): 商品单价
    - quantity (int): 购买数量
    - discount (float): 折扣比例，0-1之间
    
    返回:
    - float: 计算后的总价
    
    异常:
    - ValueError: 当参数无效时抛出
    
    示例:
        >>> calculate_total(100.0, 2, 0.1)
        180.0
    """
    if price < 0 or quantity < 0:
        raise ValueError("价格和数量必须为正数")
    if not 0 <= discount <= 1:
        raise ValueError("折扣必须在 0-1 之间")
    
    total = price * quantity
    return total * (1 - discount)
```

### 2. 行内注释

```python
# ✅ 推荐：解释"为什么"而不是"做什么"
# 缓存用户信息，提高查询性能
user_cache = get_from_cache(user_id)

# ❌ 不推荐：无意义的注释
# 获取用户
user = get_user(user_id)
```

### 3. 类型注解即文档

```python
# ✅ 推荐：使用类型注解替代注释
def process_order(order: Order, customer: Customer) -> OrderResult:
    """处理订单"""
    pass

# ❌ 不推荐：没有类型注解
def process_order(order, customer):  # order: Order, customer: Customer
    pass
```

## 🚀 性能优化

### 1. 使用异步编程

```python
# ✅ 推荐：使用异步 I/O
async def fetch_user(user_id: int):
    """异步获取用户"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"/api/users/{user_id}")
        return response.json()

# ❌ 不推荐：阻塞式调用
def fetch_user(user_id: int):
    """获取用户"""
    response = requests.get(f"/api/users/{user_id}")
    return response.json()
```

### 2. 数据库查询优化

```python
# ✅ 推荐：使用预加载避免 N+1 查询
article = await crud.get(id=article_id, preload=["author", "category"])

# ❌ 不推荐：多次查询
article = await crud.get(id=article_id)
author = await get_author(article.author_id)
category = await get_category(article.category_id)

# ✅ 推荐：使用索引字段查询
users = await crud.list(search={"email": user_email})

# ❌ 不推荐：全表扫描
users = await crud.list()
filtered = [u for u in users if u.email == user_email]
```

### 3. 缓存机制

```python
from functools import lru_cache

# ✅ 推荐：使用缓存装饰器
@lru_cache(maxsize=128)
def get_config(key: str):
    """获取配置"""
    return db.query(Config).filter(Config.key == key).first()
```

## 🔒 安全实践

### 1. 密码处理

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ✅ 推荐：存储密码哈希
def hash_password(password: str) -> str:
    """加密密码"""
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    """验证密码"""
    return pwd_context.verify(plain, hashed)

# ❌ 绝对禁止：明文存储密码
user.password = password
```

### 2. SQL 注入防护

```python
# ✅ 推荐：使用参数化查询（SQLAlchemy 自动防护）
user = await db.execute(
    select(UserModel).filter(UserModel.email == user_email)
)

# ❌ 绝对禁止：字符串拼接 SQL
query = f"SELECT * FROM users WHERE email = '{user_email}'"
```

### 3. 输入验证

```python
from pydantic import BaseModel, validator

class UserCreateSchema(BaseModel):
    """创建用户模型"""
    
    email: str = Field(..., regex=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    
    @validator('email')
    def validate_email(cls, v):
        if 'test' in v:
            raise ValueError('无效的邮箱地址')
        return v
```

## 🧪 测试实践

### 1. 单元测试

```python
import pytest

def test_add_numbers():
    """测试加法"""
    assert add(1, 2) == 3
    assert add(-1, 1) == 0
    assert add(0, 0) == 0

async def test_create_user():
    """测试创建用户"""
    data = UserCreateSchema(name="测试", email="test@example.com")
    user = await create_user(data)
    assert user.name == "测试"
    assert user.email == "test@example.com"
```

### 2. 测试覆盖率

```bash
# 运行测试并生成覆盖率报告
pytest --cov=app tests/
```

## 📝 代码审查清单

编写代码后，自我审查以下事项：

- [ ] 代码符合 PEP 8 规范
- [ ] 变量和函数命名有意义
- [ ] 所有函数都有类型提示
- [ ] 所有函数都有文档字符串
- [ ] 异常处理得当
- [ ] 没有硬编码的魔法数字/字符串
- [ ] 使用了适当的日志记录
- [ ] 性能关键的代码已经优化
- [ ] 安全性考虑充分

## 💡 小贴士

1. **使用 IDE 插件**：推荐使用 Pylint、Flake8 等代码检查工具
2. **定期重构**：保持代码整洁，及时重构冗余代码
3. **学习开源项目**：多阅读优秀的开源代码，学习最佳实践
4. **代码审查**：提交代码前，进行自我审查

## 📚 推荐工具

- **代码格式化**：black, autopep8
- **类型检查**：mypy
- **代码检查**：pylint, flake8
- **测试框架**：pytest
- **文档生成**：Sphinx

---

**记住：好的代码是可读的代码！** 📖

