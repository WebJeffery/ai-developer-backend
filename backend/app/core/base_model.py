# -*- coding: utf-8 -*-
"""
基础模型模块
提供跨数据库兼容的基础模型类和类型装饰器
"""

from datetime import datetime
from typing import Optional, Dict, Any

from sqlalchemy import Boolean, String, Integer, DateTime, ForeignKey, Text, BigInteger
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, declared_attr, mapped_column, MappedAsDataclass



class MappedBase(AsyncAttrs, DeclarativeBase):
    """
    声明式基类

    `AsyncAttrs <https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.AsyncAttrs>`__

    `DeclarativeBase <https://docs.sqlalchemy.org/en/20/orm/declarative_config.html>`__

    `mapped_column() <https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column>`__

    兼容 SQLite、MySQL 和 PostgreSQL
    """

    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        """生成表名"""
        return cls.__name__.lower()

    @declared_attr.directive
    def __table_args__(cls) -> dict:
        """表配置"""
        return {'comment': cls.__doc__ or ''}


class ModelMixin(MappedBase):
    """
    基础模型混合类
    """
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment='主键ID')
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True, default=None, comment="备注/描述")
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, default=datetime.now, comment='创建时间')
    create_by: Mapped[Optional[str]] = mapped_column(String(64), default='', comment='创建者')
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    update_by: Mapped[Optional[str]] = mapped_column(String(64), default='', comment='更新者')
    del_flag: Mapped[str] = mapped_column(String(1), nullable=False, default='0', comment='删除标志（0代表存在 2代表删除）')
    

class CreatorMixin(ModelMixin):
    """
    创建人混合类
    """
    __abstract__ = True

    creator_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, index=True, comment="创建人ID")

    @declared_attr
    def creator(cls) -> Mapped[Optional["UserModel"]]:
        """创建人关联关系（延迟加载，避免循环依赖）"""
        return relationship(
            "UserModel",
            primaryjoin=f"{cls.__name__}.creator_id == UserModel.id",
            lazy="selectin",
            foreign_keys=[cls.creator_id],
            viewonly=True,
            uselist=False  # 明确指定返回单个对象
        )
