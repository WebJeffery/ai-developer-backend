# -*- coding: utf-8 -*-

from fastapi import APIRouter, Depends, WebSocket
from fastapi.responses import JSONResponse, StreamingResponse

from app.common.response import StreamResponse, SuccessResponse
from app.core.dependencies import AuthPermission
from app.core.router_class import OperationLogRoute
from app.core.logger import logger
from app.api.v1.module_system.auth.schema import AuthSchema
from .service import MCPService
from .schema import ChatQuerySchema


MCPRouter = APIRouter(route_class=OperationLogRoute, prefix="/mcp", tags=["MCP智能助手"])


@MCPRouter.post("/chat", summary="智能对话", description="与MCP智能助手进行对话")
async def chat_controller(
    query: ChatQuerySchema,
    auth: AuthSchema = Depends(AuthPermission(permissions=["ai:mcp:chat"]))
) -> StreamingResponse:
    """智能对话接口"""
    logger.info(f"用户 {auth.user.name} 发起智能对话: {query.message[:50]}...")
    
    async def generate_response():
        async for chunk in MCPService.chat_query(query.message):
            yield chunk
    
    return StreamingResponse(generate_response(), media_type="text/plain")


@MCPRouter.websocket("/ws/chat", name="WebSocket聊天")
async def websocket_chat_controller(
    websocket: WebSocket,
):
    """WebSocket聊天接口
    
    ws://127.0.0.1:8001/api/v1/ai/mcp/ws/chat
    """
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            # 流式发送响应
            async for chunk in MCPService.chat_query(data):
                await websocket.send_text(chunk)
    except Exception as e:
        logger.error(f"WebSocket聊天出错: {str(e)}")
        await websocket.close()
