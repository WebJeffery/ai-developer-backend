# -*- coding: utf-8 -*-

from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

from app.core.base_schema import BaseSchema


class ApplicationCreateSchema(BaseModel):
    """应用创建模型"""
    name: str = Field(..., max_length=64, description='应用名称')
    access_url: str = Field(..., max_length=255, description="访问地址")
    icon_url: Optional[str] = Field(None, max_length=300, description="应用图标URL")
    status: bool = Field(True, description="是否启用(True:启用 False:禁用)")
    description: Optional[str] = Field(default=None, max_length=255, description="描述")


class ApplicationUpdateSchema(ApplicationCreateSchema):
    """应用更新模型"""
    ...


class ApplicationOutSchema(ApplicationCreateSchema, BaseSchema):
    """应用响应模型"""
    model_config = ConfigDict(from_attributes=True)
