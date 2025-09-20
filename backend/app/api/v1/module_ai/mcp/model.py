# -*- coding: utf-8 -*-

from sqlalchemy import JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import CreatorMixin

class Mcp(CreatorMixin):
    """MCP 服务器表"""

    __tablename__ = 'ai_mcp'
    __table_args__ = ({'comment': 'MCP 服务器表'})

    name: Mapped[str] = mapped_column(String(50), unique=True, comment='MCP 名称')
    type: Mapped[int] = mapped_column(default=0, comment='MCP 类型（0stdio 1sse）')
    url: Mapped[str | None] = mapped_column(String(255), default=None, comment='远程 SSE 地址')
    command: Mapped[str | None] = mapped_column(String(255), default=None, comment='MCP 命令')
    args: Mapped[str | None] = mapped_column(String(255), default=None, comment='MCP 命令参数')
    env: Mapped[str | None] = mapped_column(JSON(), default=None, comment='MCP 环境变量')