# -*- coding: utf-8 -*-

from typing import Optional, Dict, Any
from sqlalchemy import JSON, String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import CreatorMixin


class McpModel(CreatorMixin):
    """
    MCP 服务器表
    """

    __tablename__ = 'app_ai_mcp'
    __table_args__ = ({'comment': 'MCP 服务器表'})
    __loader_options__ = ["creator"]

    name: Mapped[str] = mapped_column(String(50), unique=True, comment='MCP 名称')
    type: Mapped[int] = mapped_column(Integer, default=0, comment='MCP 类型（0:stdio 1:sse）')
    url: Mapped[Optional[str]] = mapped_column(String(255), default=None, comment='远程 SSE 地址')
    command: Mapped[Optional[str]] = mapped_column(String(255), default=None, comment='MCP 命令')
    args: Mapped[Optional[str]] = mapped_column(String(255), default=None, comment='MCP 命令参数')
    env: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON(), default=None, comment='MCP 环境变量')