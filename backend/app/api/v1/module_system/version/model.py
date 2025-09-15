from sqlalchemy import Column, Integer, String, Text, DateTime
from app.core.base_model import BaseModel
from datetime import datetime


class Version(BaseModel):
    """版本模型"""
    __tablename__ = "version"
    
    id = Column(Integer, primary_key=True, index=True, comment="版本ID")
    version_number = Column(String(50), nullable=False, comment="版本号")
    title = Column(String(255), nullable=False, comment="版本标题")
    release_notes = Column(Text, comment="发布说明")
    status = Column(String(50), default="draft", comment="版本状态(draft, released, archived)")
    project = Column(String(100), comment="所属项目")
    released_at = Column(DateTime, comment="发布时间")
    
    description = Column(Text, comment="版本描述")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")