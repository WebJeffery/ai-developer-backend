# -*- coding: utf-8 -*-

from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

from app.core.base_schema import BaseSchema


class TicketCreateSchema(BaseModel):
    """创建工单"""
    title: str = Field(..., max_length=255, description='工单标题')
    description: Optional[str] = Field(default=None, description='工单描述')
    status: Optional[str] = Field(default='pending', description='工单处理状态(pending:待处理 progress:处理中 resolved:已解决 closed:已关闭)')
    priority: Optional[str] = Field(default='medium', description='优先级(low, medium, high, urgent)')
    type: Optional[str] = Field(default='bug', description='工单类型(bug, feature, task)')
    assignee_id: Optional[int] = Field(default=None, description='指派给用户ID')
    reporter_id: int = Field(..., description='报告人ID')
    project: Optional[str] = Field(default=None, max_length=100, description='所属项目')
    version: Optional[str] = Field(default=None, max_length=50, description='版本号')


class TicketUpdateSchema(TicketCreateSchema):
    """更新工单"""
    ...


class TicketOutSchema(TicketCreateSchema, BaseSchema):
    """工单输出"""
    model_config = ConfigDict(from_attributes=True)
    ...