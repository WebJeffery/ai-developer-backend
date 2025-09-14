# -*- coding: utf-8 -*-

from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

from app.core.base_schema import BaseSchema


class DemoCreateSchema(BaseModel):
    """新增模型"""
    name: str = Field(..., max_length=50, description='名称')
    status: bool = Field(True, description="是否启用(True:启用 False:禁用)")
    description: Optional[str] = Field(default=None, max_length=255, description="描述")


class DemoUpdateSchema(DemoCreateSchema):
    """更新模型"""
    ...


class DemoOutSchema(DemoCreateSchema, BaseSchema):
    """响应模型"""
    model_config = ConfigDict(from_attributes=True)
