from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class VersionCreate(BaseModel):
    """创建版本"""
    version_number: str
    title: str
    description: Optional[str] = None
    release_notes: Optional[str] = None
    status: Optional[str] = "draft"
    project: Optional[str] = None
    released_at: Optional[datetime] = None


class VersionUpdate(BaseModel):
    """更新版本"""
    version_number: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    release_notes: Optional[str] = None
    status: Optional[str] = None
    project: Optional[str] = None
    released_at: Optional[datetime] = None


class VersionOut(BaseModel):
    """版本输出"""
    id: int
    version_number: str
    title: str
    description: Optional[str] = None
    release_notes: Optional[str] = None
    status: str
    project: Optional[str] = None
    released_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True