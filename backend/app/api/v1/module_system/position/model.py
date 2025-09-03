# -*- coding: utf-8 -*-
"""
岗位模型模块
定义岗位相关数据模型
"""

from typing import List

from sqlalchemy import String, Integer
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.core.base_model import CreatorMixin


class PositionModel(CreatorMixin):
    """
    岗位模型
    """
    __tablename__ = "system_position"
    __table_args__ = ({'comment': '岗位表'})

    name: Mapped[str] = mapped_column(String(40), nullable=False, unique=True, comment="岗位名称")
    order: Mapped[int] = mapped_column(Integer, nullable=False, default=1, comment="显示排序")

    # 用户关联关系
    users: Mapped[List["UserModel"]] = relationship(secondary="system_user_positions", back_populates="positions", lazy="selectin")

    # users: Mapped[List["UserModel"]] = relationship(secondary="system_user_positions", back_populates="positions", lazy="select")

