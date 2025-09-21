# -*- coding: utf-8 -*-

from typing import Optional
from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import CreatorMixin


class DemoModel(CreatorMixin):
    """
    示例表
    """
    __tablename__ = 'example_demo'
    __table_args__ = ({'comment': '示例表'})

    name: Mapped[Optional[str]] = mapped_column(String(64), nullable=True, default='', comment='名称')
    status: Mapped[bool] = mapped_column(Boolean(), default=True, nullable=False, comment="是否启用(True:启用 False:禁用)")
