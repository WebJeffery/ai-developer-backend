# -*- coding: utf-8 -*-

from typing import Optional
from sqlalchemy import String, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from app.core.base_model import CreatorMixin


class VersionModel(CreatorMixin):
    """
    版本模型 - SQLAlchemy 2.0 语法
    兼容 MySQL 和 PostgreSQL
    """
    __tablename__ = 'system_version'
    __table_args__ = ({'comment': '版本表'})

    version_number: Mapped[str] = mapped_column(String(50), nullable=False, comment='版本号')
    title: Mapped[str] = mapped_column(String(255), nullable=False, comment='版本标题')
    release_notes: Mapped[Optional[str]] = mapped_column(Text, comment='发布说明')
    status: Mapped[str] = mapped_column(String(50), default='draft', comment='版本状态(draft: 草稿, released: 已发布, archived: 已归档)')
    project: Mapped[Optional[str]] = mapped_column(String(100), comment='所属项目')
    released_at: Mapped[Optional[datetime]] = mapped_column(DateTime, comment='发布时间')