# -*- coding: utf-8 -*-

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text

from app.core.base_model import BaseMixin


class DemoModel(BaseMixin):
    """
    示例表
    """

    __tablename__ = 'example_demo'
    __table_args__ = ({'comment': '示例表'})

    name=Column(String(64), nullable=True, default='', comment='名称')
    description=Column(Text, nullable=True, comment='描述')
    status = Column(Boolean, default=False, nullable=True, comment='任务状态:正常,停止')
