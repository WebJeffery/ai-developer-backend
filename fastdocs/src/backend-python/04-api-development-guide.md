# API 接口开发指南

本指南将教您从零开始开发一个完整的 API 接口，适合 Python 新手学习。

## 📋 目录

- [开发流程概述](#开发流程概述)
- [项目架构](#项目架构)
- [创建一个完整的业务模块](#创建一个完整的业务模块)
- [调试和测试](#调试和测试)
- [最佳实践](#最佳实践)

## 🏗️ 开发流程概述

在 FastAPI-Vue3-Admin 中，开发一个完整的接口通常需要以下步骤：

```
1. 创建数据模型 (Model)
   ↓
2. 创建 Pydantic Schema
   ↓
3. 创建 CRUD 数据访问层
   ↓
4. 创建 Service 业务逻辑层
   ↓
5. 创建 Controller 接口层
   ↓
6. 注册路由
```

## 📁 项目架构

### 典型的业务模块结构

```
module_product/                    # 产品模块
├── model.py                       # ORM 数据模型
├── schema.py                      # Pydantic 验证模型
├── param.py                       # 查询参数模型
├── crud.py                        # 数据访问层
├── service.py                     # 业务逻辑层
└── controller.py                  # 接口控制器
```

### 各层职责说明

| 层级 | 文件名 | 职责 | 说明 |
|------|--------|------|------|
| **Model** | `model.py` | 数据模型定义 | 对应数据库表结构 |
| **Schema** | `schema.py` | 数据验证 | 请求/响应的数据结构 |
| **Param** | `param.py` | 查询参数 | GET 请求的查询参数 |
| **CRUD** | `crud.py` | 数据访问 | 数据库增删改查操作 |
| **Service** | `service.py` | 业务逻辑 | 核心业务处理 |
| **Controller** | `controller.py` | 接口控制 | HTTP 请求处理 |

## 🎯 实战：创建一个 "文章管理" 模块

让我们通过一个实际的例子，创建一个完整的"文章管理"功能。

### 需求分析

- 文章标题、内容、分类
- 支持创建、查询、更新、删除
- 支持分页查询
- 需要权限控制

### 步骤 1: 创建 Model（数据模型）

创建文件 `app/api/v1/module_content/article/model.py`：

```python
# -*- coding: utf-8 -*-
"""
文章数据模型
"""

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Text, ForeignKey

from app.core.base_model import ModelMixin


class ArticleModel(ModelMixin):
    """文章模型"""
    
    __tablename__ = "content_article"
    
    # 文章标题
    title: Mapped[str] = mapped_column(String(255), comment="文章标题")
    
    # 文章内容
    content: Mapped[str] = mapped_column(Text, comment="文章内容")
    
    # 文章分类
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("content_category.id"), comment="分类ID")
    
    # 阅读量
    view_count: Mapped[int] = mapped_column(Integer, default=0, comment="阅读量")
    
    # 状态（0:草稿, 1:已发布）
    status: Mapped[int] = mapped_column(Integer, default=0, comment="状态")
```

### 步骤 2: 创建 Schema（数据验证）

创建文件 `app/api/v1/module_content/article/schema.py`：

```python
# -*- coding: utf-8 -*-
"""
文章 Schema
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ArticleCreateSchema(BaseModel):
    """创建文章的 Schema"""
    
    title: str = Field(..., min_length=1, max_length=255, description="文章标题")
    content: str = Field(..., description="文章内容")
    category_id: int = Field(..., description="分类ID")
    status: int = Field(default=0, description="状态")


class ArticleUpdateSchema(BaseModel):
    """更新文章的 Schema"""
    
    title: Optional[str] = Field(None, min_length=1, max_length=255, description="文章标题")
    content: Optional[str] = Field(None, description="文章内容")
    category_id: Optional[int] = Field(None, description="分类ID")
    status: Optional[int] = Field(None, description="状态")


class ArticleOutSchema(BaseModel):
    """文章输出 Schema"""
    
    id: int = Field(description="文章ID")
    title: str = Field(description="文章标题")
    content: str = Field(description="文章内容")
    category_id: int = Field(description="分类ID")
    view_count: int = Field(description="阅读量")
    status: int = Field(description="状态")
    create_datetime: datetime = Field(description="创建时间")
    
    class Config:
        from_attributes = True
```

### 步骤 3: 创建 Param（查询参数）

创建文件 `app/api/v1/module_content/article/param.py`：

```python
# -*- coding: utf-8 -*-
"""
文章查询参数
"""

from app.core.base_params import PageQueryParam
from pydantic import BaseModel, Field
from typing import Optional


class ArticleQueryParam(PageQueryParam):
    """文章查询参数"""
    
    # 文章标题（模糊查询）
    title: Optional[str] = Field(None, description="文章标题")
    
    # 分类ID
    category_id: Optional[int] = Field(None, description="分类ID")
    
    # 状态
    status: Optional[int] = Field(None, description="状态")
```

### 步骤 4: 创建 CRUD（数据访问层）

创建文件 `app/api/v1/module_content/article/crud.py`：

```python
# -*- coding: utf-8 -*-
"""
文章 CRUD
"""

from app.api.v1.module_content.article.model import ArticleModel
from app.api.v1.module_content.article.schema import ArticleCreateSchema, ArticleUpdateSchema
from app.core.base_crud import CRUDBase


class ArticleCRUD(CRUDBase[ArticleModel, ArticleCreateSchema, ArticleUpdateSchema]):
    """文章 CRUD"""
    
    def __init__(self, auth):
        super().__init__(ArticleModel, auth)
```

**说明**：
- 继承 `CRUDBase` 自动获得基础的增删改查功能
- 无需编写额外的 SQL 代码
- 自动处理数据权限

### 步骤 5: 创建 Service（业务逻辑层）

创建文件 `app/api/v1/module_content/article/service.py`：

```python
# -*- coding: utf-8 -*-
"""
文章业务逻辑层
"""

from typing import List
from app.api.v1.module_content.article.crud import ArticleCRUD
from app.api.v1.module_content.article.schema import (
    ArticleCreateSchema, 
    ArticleUpdateSchema,
    ArticleOutSchema
)
from app.api.v1.module_content.article.param import ArticleQueryParam
from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.exceptions import CustomException


class ArticleService:
    """文章服务"""
    
    def __init__(self, auth: AuthSchema):
        self.auth = auth
        self.crud = ArticleCRUD(auth)
    
    async def create_article(
        self, 
        data: ArticleCreateSchema
    ) -> ArticleOutSchema:
        """
        创建文章
        
        参数:
        - data: 文章数据
        
        返回:
        - ArticleOutSchema: 创建的文章信息
        """
        # 使用 CRUD 创建
        article = await self.crud.create(data=data)
        return ArticleOutSchema.model_validate(article)
    
    async def get_article(self, article_id: int) -> ArticleOutSchema:
        """
        获取文章详情
        
        参数:
        - article_id: 文章ID
        
        返回:
        - ArticleOutSchema: 文章详情
        """
        article = await self.crud.get(id=article_id)
        if not article:
            raise CustomException(msg=f"文章不存在，ID: {article_id}")
        return ArticleOutSchema.model_validate(article)
    
    async def update_article(
        self, 
        article_id: int, 
        data: ArticleUpdateSchema
    ) -> ArticleOutSchema:
        """
        更新文章
        
        参数:
        - article_id: 文章ID
        - data: 更新数据
        
        返回:
        - ArticleOutSchema: 更新后的文章信息
        """
        article = await self.crud.update(id=article_id, data=data)
        if not article:
            raise CustomException(msg=f"文章不存在，ID: {article_id}")
        return ArticleOutSchema.model_validate(article)
    
    async def delete_article(self, article_id: int):
        """
        删除文章
        
        参数:
        - article_id: 文章ID
        """
        await self.crud.delete(ids=[article_id])
    
    async def list_articles(
        self, 
        query: ArticleQueryParam
    ) -> List[ArticleOutSchema]:
        """
        获取文章列表
        
        参数:
        - query: 查询参数
        
        返回:
        - List[ArticleOutSchema]: 文章列表
        """
        # 构建查询条件
        search = {}
        if query.title:
            search["title__like"] = query.title
        if query.category_id:
            search["category_id"] = query.category_id
        if query.status is not None:
            search["status"] = query.status
        
        # 使用 CRUD 查询列表
        articles = await self.crud.list(
            search=search,
            order_by=[{"id": "desc"}]
        )
        
        return [ArticleOutSchema.model_validate(article) for article in articles]
```

### 步骤 6: 创建 Controller（接口控制器）

创建文件 `app/api/v1/module_content/article/controller.py`：

```python
# -*- coding: utf-8 -*-
"""
文章接口控制器
"""

from typing import List
from fastapi import APIRouter, Depends, Path as PathParam
from fastapi.params import Query

from app.api.v1.module_content.article.service import ArticleService
from app.api.v1.module_content.article.schema import (
    ArticleCreateSchema,
    ArticleUpdateSchema,
    ArticleOutSchema
)
from app.api.v1.module_content.article.param import ArticleQueryParam
from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.dependencies import AuthPermission
from app.core.router_class import OperationLogRoute
from app.common.response import SuccessResponse
from app.core.pagination import PaginationService


router = APIRouter(
    route_class=OperationLogRoute,
    prefix="/article",
    tags=["内容管理-文章"]
)


@router.post("", summary="创建文章")
async def create_article(
    data: ArticleCreateSchema,
    auth: AuthSchema = Depends(AuthPermission(["content:article:create"]))
):
    """
    创建文章
    
    需要权限: content:article:create
    """
    result = await ArticleService(auth).create_article(data)
    return SuccessResponse(data=result, msg="创建成功")


@router.get("/{article_id}", summary="获取文章详情")
async def get_article(
    article_id: int = PathParam(..., description="文章ID"),
    auth: AuthSchema = Depends(AuthPermission(["content:article:query"]))
):
    """
    获取文章详情
    
    需要权限: content:article:query
    """
    result = await ArticleService(auth).get_article(article_id)
    return SuccessResponse(data=result)


@router.put("/{article_id}", summary="更新文章")
async def update_article(
    data: ArticleUpdateSchema,
    article_id: int = PathParam(..., description="文章ID"),
    auth: AuthSchema = Depends(AuthPermission(["content:article:update"]))
):
    """
    更新文章
    
    需要权限: content:article:update
    """
    result = await ArticleService(auth).update_article(article_id, data)
    return SuccessResponse(data=result, msg="更新成功")


@router.delete("/{article_id}", summary="删除文章")
async def delete_article(
    article_id: int = PathParam(..., description="文章ID"),
    auth: AuthSchema = Depends(AuthPermission(["content:article:delete"]))
):
    """
    删除文章
    
    需要权限: content:article:delete
    """
    await ArticleService(auth).delete_article(article_id)
    return SuccessResponse(msg="删除成功")


@router.get("", summary="获取文章列表")
async def list_articles(
    query: ArticleQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["content:article:query"]))
):
    """
    获取文章列表（支持分页和筛选）
    
    需要权限: content:article:query
    """
    result_list = await ArticleService(auth).list_articles(query)
    
    # 分页处理
    result = PaginationService.paginate(
        data_list=result_list,
        page_no=query.page_no,
        page_size=query.page_size
    )
    
    return SuccessResponse(data=result)
```

### 步骤 7: 注册路由

在 `app/api/v1/__init__.py` 中注册路由：

```python
# 添加文章路由
from app.api.v1.module_content.article import controller as article_router

# 注册路由
v1_router.include_router(article_router.router)
```

## 🧪 测试接口

### 使用 API 文档测试

1. 启动项目：`python3 main.py run --env=dev`
2. 访问 http://localhost:8000/docs
3. 找到"内容管理-文章"分组
4. 点击"Try it out"测试各个接口

### 使用 curl 测试

```bash
# 1. 先登录获取 token
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "123456",
    "code": "1234",
    "uuid": "test"
  }'

# 2. 使用 token 创建文章
curl -X POST "http://localhost:8000/api/v1/content/article" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "我的第一篇文章",
    "content": "这是文章内容",
    "category_id": 1,
    "status": 0
  }'

# 3. 获取文章列表
curl -X GET "http://localhost:8000/api/v1/content/article?page_no=1&page_size=10" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## ✅ 开发清单

完成以下步骤，您的接口就开发完成了！

- [ ] 创建 Model 数据模型
- [ ] 创建 Schema 验证模型
- [ ] 创建 Param 查询参数
- [ ] 创建 CRUD 数据访问层
- [ ] 创建 Service 业务逻辑层
- [ ] 创建 Controller 接口控制器
- [ ] 注册路由
- [ ] 测试接口功能

## 💡 开发技巧

### 1. 批量操作

```python
# 批量删除
await self.crud.delete(ids=[1, 2, 3])

# 批量创建
articles = [ArticleCreateSchema(...), ...]
for article in articles:
    await self.crud.create(data=article)
```

### 2. 关联查询

```python
# 预加载关联数据
article = await self.crud.get(
    id=1, 
    preload=["category", "creator"]
)
```

### 3. 复杂查询

```python
# 组合条件查询
search = {
    "title__like": "Python",
    "status": 1,
    "create_datetime__gte": datetime.now()
}
articles = await self.crud.list(search=search)
```

## 📝 下一步

接口开发完成后，您可以：

1. 🎓 学习 [Python 开发教程](./05-python-tutorial.md)
2. 🔧 查看 [最佳实践](./06-best-practices.md)
3. 🗄️ 配置 [数据库](./03-database-setup-guide.md)

---

**恭喜！您已经掌握了 API 开发的完整流程！** 🎉

