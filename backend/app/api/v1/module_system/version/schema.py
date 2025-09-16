# -*- coding: utf-8 -*-

from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

from app.core.base_schema import BaseSchema
from app.core.validator import DateTimeStr


class VersionCreateSchema(BaseModel):
    """创建版本"""
    version_number: str = Field(..., max_length=50, description='版本号')
    title: str = Field(..., max_length=255, description='版本标题')
    release_notes: Optional[str] = Field(default=None, description='发布说明')
    description: Optional[str] = Field(default=None, description='工单描述')
    status: Optional[str] = Field(default='draft', description='版本状态(draft: 草稿, released: 已发布, archived: 已归档)')
    project: Optional[str] = Field(default=None, max_length=100, description='所属项目')
    released_at: Optional[DateTimeStr] = Field(default=None, description='发布时间')


class VersionUpdateSchema(VersionCreateSchema):
    """更新版本"""
    ...


class VersionOutSchema(VersionCreateSchema, BaseSchema):
    """版本输出"""
    model_config = ConfigDict(from_attributes=True)
    ...