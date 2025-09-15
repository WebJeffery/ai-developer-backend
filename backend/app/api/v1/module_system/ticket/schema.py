from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class TicketCreate(BaseModel):
    """创建工单"""
    title: str
    description: Optional[str] = None
    status: Optional[str] = "open"
    priority: Optional[str] = "medium"
    type: Optional[str] = "bug"
    assignee_id: Optional[int] = None
    reporter_id: int
    project: Optional[str] = None
    version: Optional[str] = None


class TicketUpdate(BaseModel):
    """更新工单"""
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    type: Optional[str] = None
    assignee_id: Optional[int] = None
    project: Optional[str] = None
    version: Optional[str] = None


class TicketOut(BaseModel):
    """工单输出"""
    id: int
    title: str
    description: Optional[str] = None
    status: str
    priority: str
    type: str
    assignee_id: Optional[int] = None
    reporter_id: int
    project: Optional[str] = None
    version: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True