# -*- coding: utf-8 -*-

from typing import Optional
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import CreatorMixin


class DemoModel(CreatorMixin):
    """
    示例表 - SQLAlchemy 2.0 语法
    兼容 MySQL 和 PostgreSQL
    """
    __tablename__ = 'example_demo'
    __table_args__ = ({'comment': '示例表'})

    name: Mapped[Optional[str]] = mapped_column(String(64), nullable=True, default='', comment='名称')
