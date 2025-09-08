# -*- coding: utf-8 -*-

from app.utils.ai_util import AIClient


class MCPService:
    """MCP服务层 - 适配FastAPI-MCP"""

    @classmethod
    async def chat_query(cls, message: str):
        """处理聊天查询"""
        # 创建MCP客户端实例
        mcp_client = AIClient()
        try:
            # 处理消息
            async for response in mcp_client.process(message):
                yield response
        finally:
            # 确保关闭客户端连接
            await mcp_client.close()