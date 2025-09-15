# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.base_model import MappedBase, CreatorMixin

class Ticket(CreatorMixin):
    """工单模型"""
    __tablename__ = "ticket"
        
    title = Column(String(255), nullable=False, comment="工单标题")
    status = Column(String(50), default="1", comment="工单状态(1:待处理 2:处理中 3:已解决 4:已关闭)")
    priority = Column(String(50), default="medium", comment="优先级(low, medium, high, urgent)")
    type = Column(String(50), comment="工单类型(bug, feature, task)")
    assignee_id = Column(Integer, ForeignKey("system_user.id"), comment="指派给用户ID")
    reporter_id = Column(Integer, ForeignKey("system_user.id"), comment="报告人ID")
    project = Column(String(100), comment="所属项目")
    version = Column(String(50), comment="版本号")

    # 关系
    assignee = relationship("UserModel", foreign_keys=[assignee_id])
    reporter = relationship("UserModel", foreign_keys=[reporter_id])