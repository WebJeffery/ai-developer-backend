# -*- coding: utf-8 -*-

from typing import Optional, List
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.core.base_model import ModelMixin

class DeptModel(ModelMixin):
    """
    部门表 - 用于存储组织架构中的部门信息 - SQLAlchemy 2.0 语法
    支持层级结构，兼容 MySQL 和 PostgreSQL
    """
    __tablename__ = "system_dept"
    __table_args__ = ({'comment': '部门表'})
    # 基础字段
    name: Mapped[str] = mapped_column(String(40),nullable=False,unique=True,comment="部门名称")
    order: Mapped[int] = mapped_column(Integer,nullable=False,default=999,comment="显示排序")
    
    parent_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("system_dept.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=True, index=True, comment="父级部门ID")
    parent: Mapped[Optional["DeptModel"]] = relationship("DeptModel", cascade="all, delete-orphan", uselist=False)
    
    # 角色关联关系
    roles: Mapped[List["RoleModel"]] = relationship(secondary="system_role_depts", back_populates="depts", lazy="selectin")
    
    # 用户关联关系
    users: Mapped[List["UserModel"]] = relationship(back_populates="dept", lazy="selectin")
    
    # code: Mapped[Optional[str]] = mapped_column(String(20),nullable=True,unique=True,comment="部门编码")
    # leader_id: Mapped[Optional[int]] = mapped_column(Integer,nullable=True,comment="负责人ID")
    # parent: Mapped[Optional["DeptModel"]] = relationship(back_populates="children",remote_side=[id],lazy="select",uselist=False,foreign_keys=[parent_id])
    # children: Mapped[List["DeptModel"]] = relationship(back_populates="parent",lazy="select",cascade="all, delete-orphan",foreign_keys=[parent_id])
