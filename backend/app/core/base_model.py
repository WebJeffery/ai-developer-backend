# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Annotated

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs

from sqlalchemy import Boolean, Column, String, Integer, DateTime, ForeignKey, Text, BigInteger, DateTime, TypeDecorator
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, declared_attr, mapped_column


class DateTimeMixin(MappedAsDataclass):
    """日期时间 Mixin 数据类"""

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment='创建时间')
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')


class BaseMixin(AsyncAttrs, DeclarativeBase, DateTimeMixin):
    """
    SQLAlchemy 基础模型类
    继承自 AsyncAttrs 和 DeclarativeBase,提供异步操作支持
    """
    __abstract__ = True  # 声明为抽象基类,不会创建实际数据库表
    id: Mapped[int] = mapped_column(Integer, index=True, unique=True, primary_key=True, autoincrement=True, comment='主键ID')
    # id: Mapped[int] = mapped_column(BigInteger, index=True, unique=True, primary_key=True, autoincrement=True, comment='主键ID')
    
    # 状态字段
    status: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, comment="是否启用(True:启用 False:禁用)")
    
    # 审计字段
    description: Mapped[str] = mapped_column(Text, nullable=True, comment="备注说明")
    
    creator_id: Mapped[int] = mapped_column(
        Integer, 
        ForeignKey("system_users.id", ondelete="SET NULL", onupdate="CASCADE"), 
        nullable=True, 
        index=True, 
        comment="创建人ID"
    )
    creator: Mapped["UserModel"] = relationship(
        "UserModel", 
        foreign_keys=creator_id, 
        lazy="joined",
        post_update=True,
        uselist=False
    )
    # creator = relationship(
    #     "UserModel",
    #     remote_side=[id],
    #     foreign_keys=[creator_id],
    #     lazy="selectin",
    #     uselist=False
    # )


class ModelBase(AsyncAttrs, DeclarativeBase):
    """
    SQLAlchemy 基础模型类
    继承自 AsyncAttrs 和 DeclarativeBase,提供异步操作支持
    """
    __abstract__ = True  # 声明为抽象基类,不会创建实际数据库表
