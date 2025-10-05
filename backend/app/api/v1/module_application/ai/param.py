# -*- coding: utf-8 -*-

from typing import Optional, List
from fastapi import Query
from pydantic import Field

from app.core.base_schema import BaseSchema
from app.common.enums import McpLLMProvider


class McpQueryParam:
    """MCP 服务器查询参数"""

    def __init__(
        self,
        name: Optional[str] = Query(None, description="MCP 名称"),
        type: Optional[int] = Query(None, description="MCP 类型"),
    ) -> None:
        
        # 模糊查询字段
        self.name = ("like", name) if name else None

        # 精确查询字段
        self.type = type


class McpChatParam(BaseSchema):
    """MCP 聊天参数"""
    pk: List[int] = Field(..., description='MCP ID 列表')
    provider: McpLLMProvider = Field(McpLLMProvider.openai, description='LLM 供应商')
    model: str = Field(..., description='LLM 名称')
    key: str = Field(..., description='LLM API Key')
    base_url: Optional[str] = Field(None, description='自定义 LLM API 地址，必须兼容 openai 供应商')
    prompt: str = Field(..., description='用户提示词')