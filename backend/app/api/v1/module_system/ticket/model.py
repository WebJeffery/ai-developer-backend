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
    status: Mapped[str] = mapped_column(String(50), default='pending', comment='工单状态(pending:待处理 progress:处理中 resolved:已解决 closed:已关闭)')
    priority: Mapped[str] = mapped_column(String(50), default='medium', comment='优先级(low:低, medium:中, high:高, urgent：紧急)')
    type: Mapped[Optional[str]] = mapped_column(String(50), comment='工单类型(bug:缺陷, feature:功能, task:任务)')
    assignee_id: Mapped[Optional[int]] = mapped_column(ForeignKey('system_users.id'), comment='指派给用户ID')
    reporter_id: Mapped[Optional[int]] = mapped_column(ForeignKey('system_users.id'), comment='报告人ID')
    project: Mapped[Optional[str]] = mapped_column(String(100), comment='所属项目或模块')
    version: Mapped[Optional[str]] = mapped_column(String(50), comment='版本号')

    # 关系
    assignee = relationship('UserModel', foreign_keys=[assignee_id])
    reporter = relationship('UserModel', foreign_keys=[reporter_id])