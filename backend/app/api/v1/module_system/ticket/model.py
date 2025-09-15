# -*- coding: utf-8 -*-

from typing import Optional
from sqlalchemy import String, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from app.core.base_model import CreatorMixin


class TicketModel(CreatorMixin):
    """
    工单模型 - SQLAlchemy 2.0 语法
    兼容 MySQL 和 PostgreSQL
    """
    __tablename__ = 'system_ticket'
    __table_args__ = ({'comment': '工单表'})

    title: Mapped[str] = mapped_column(String(255), nullable=False, comment='工单标题')
    ticket_status: Mapped[str] = mapped_column(String(50), default='1', comment='工单状态(1:待处理 2:处理中 3:已解决 4:已关闭)')
    priority: Mapped[str] = mapped_column(String(50), default='medium', comment='优先级(low, medium, high, urgent)')
    type: Mapped[Optional[str]] = mapped_column(String(50), comment='工单类型(bug, feature, task)')
    assignee_id: Mapped[Optional[int]] = mapped_column(ForeignKey('system_users.id'), comment='指派给用户ID')
    reporter_id: Mapped[Optional[int]] = mapped_column(ForeignKey('system_users.id'), comment='报告人ID')
    project: Mapped[Optional[str]] = mapped_column(String(100), comment='所属项目')
    version: Mapped[Optional[str]] = mapped_column(String(50), comment='版本号')

    # 关系
    assignee = relationship('UserModel', foreign_keys=[assignee_id])
    reporter = relationship('UserModel', foreign_keys=[reporter_id])