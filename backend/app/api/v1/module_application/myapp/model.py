# -*- coding: utf-8 -*-

from sqlalchemy import Boolean, String, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import CreatorMixin


class ApplicationModel(CreatorMixin):
    """
    应用系统表 - 用于管理分系统和外部应用
    """

    __tablename__ = 'application_myapp'
    __table_args__ = ({'comment': '应用系统表'})

    # 基本信息（必备字段）
    name: Mapped[str] = mapped_column(String(64), nullable=False, comment='应用名称', unique=True)

    # 状态
    status: Mapped[bool] = mapped_column(Boolean(), default=True, nullable=False, comment="是否启用(True:启用 False:禁用)")
    
    # 访问地址（核心字段）
    access_url: Mapped[str] = mapped_column(String(500), nullable=False, comment='访问地址')
    
    # 外观展示
    icon_url: Mapped[str] = mapped_column(String(300), nullable=True, comment='应用图标URL')
    