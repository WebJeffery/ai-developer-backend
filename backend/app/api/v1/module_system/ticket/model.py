from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.base_model import BaseModel
from app.api.v1.module_system.user.model import User
from datetime import datetime


class Ticket(BaseModel):
    """工单模型"""
    __tablename__ = "ticket"
    
    id = Column(Integer, primary_key=True, index=True, comment="工单ID")
    
    title = Column(String(255), nullable=False, comment="工单标题")
    
    status = Column(String(50), default="open", comment="工单状态(open, in_progress, resolved, closed)")
    priority = Column(String(50), default="medium", comment="优先级(low, medium, high, urgent)")
    type = Column(String(50), comment="工单类型(bug, feature, task)")
    assignee_id = Column(Integer, ForeignKey("system_user.id"), comment="指派给用户ID")
    reporter_id = Column(Integer, ForeignKey("system_user.id"), comment="报告人ID")
    project = Column(String(100), comment="所属项目")
    version = Column(String(50), comment="版本号")

    description = Column(Text, comment="工单描述")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    
    # 关系
    assignee = relationship("User", foreign_keys=[assignee_id])
    reporter = relationship("User", foreign_keys=[reporter_id])