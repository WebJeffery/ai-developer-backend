# -*- coding: utf-8 -*-

from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query
from starlette.responses import StreamingResponse

from backend.common.pagination import DependsPagination, PageData, paging_data
from backend.common.response.response_schema import ResponseModel, ResponseSchemaModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.common.security.permission import RequestPermission
from backend.common.security.rbac import DependsRBAC
from backend.database.db import CurrentSession
from .schema import CreateMcpParam, GetMcpDetail, McpChatParam, UpdateMcpParam
from .service import mcp_service

from fastapi import APIRouter, Depends, WebSocket
from fastapi.responses import JSONResponse, StreamingResponse

from app.common.response import StreamResponse, SuccessResponse
from app.core.dependencies import AuthPermission
from app.core.router_class import OperationLogRoute
from app.core.logger import logger
from app.api.v1.module_system.auth.schema import AuthSchema
from .service import MCPService
from .schema import ChatQuerySchema


MCPRouter = APIRouter(route_class=OperationLogRoute, prefix="", tags=["MCP智能助手"])


@MCPRouter.post("/mcp/chat", summary="智能对话", description="与MCP智能助手进行对话")
async def chat_controller(
    query: ChatQuerySchema,
    auth: AuthSchema = Depends(AuthPermission(permissions=["ai:mcp:chat"]))
) -> StreamingResponse:
    """智能对话接口"""
    logger.info(f"用户 {auth.user.name} 发起智能对话: {query.message[:50]}...")
    
    async def generate_response():
        try:
            async for chunk in MCPService.chat_query(query.message):
                # 确保返回的是字节串
                if chunk:
                    yield chunk.encode('utf-8') if isinstance(chunk, str) else chunk
        except Exception as e:
            logger.error(f"流式响应出错: {str(e)}")
            yield f"抱歉，处理您的请求时出现了错误: {str(e)}".encode('utf-8')
    
    return StreamingResponse(generate_response(), media_type="text/plain; charset=utf-8")


@MCPRouter.websocket("/ws/mcp/chat", name="WebSocket聊天")
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
            try:
                async for chunk in MCPService.chat_query(data):
                    if chunk:
                        await websocket.send_text(chunk)
            except Exception as e:
                logger.error(f"处理聊天查询出错: {str(e)}")
                await websocket.send_text(f"抱歉，处理您的请求时出现了错误: {str(e)}")
    except Exception as e:
        logger.error(f"WebSocket聊天出错: {str(e)}")
    finally:
        await websocket.close()


@MCPRouter.get('/{pk}', summary='获取 MCP 服务器详情', dependencies=[DependsJwtAuth])
async def get_mcp(pk: Annotated[int, Path(description='MCP ID')]) -> ResponseSchemaModel[GetMcpDetail]:
    mcp = await mcp_service.get(pk=pk)
    return response_base.success(data=mcp)


@MCPRouter.get('', summary='分页获取所有 MCP 服务器', dependencies=[DependsJwtAuth, DependsPagination])
async def get_pagination_mcps(
    db: CurrentSession,
    name: Annotated[str | None, Query(description='MCP 名称')] = None,
    type: Annotated[int | None, Query(description='MCP 类型')] = None,
) -> ResponseSchemaModel[PageData[GetMcpDetail]]:
    mcp_select = await mcp_service.get_select(name=name, type=type)
    page_data = await paging_data(db, mcp_select)
    return response_base.success(data=page_data)


@MCPRouter.post('', summary='创建 MCP 服务器', dependencies=[Depends(RequestPermission('sys:mcp:add')), DependsRBAC])
async def create_mcp(obj: CreateMcpParam) -> ResponseModel:
    await mcp_service.create(obj=obj)
    return response_base.success()


@MCPRouter.put('/{pk}', summary='更新 MCP 服务器', dependencies=[ Depends(RequestPermission('sys:mcp:edit')), DependsRBAC])
async def update_mcp(pk: Annotated[int, Path(description='MCP ID')], obj: UpdateMcpParam) -> ResponseModel:
    count = await mcp_service.update(pk=pk, obj=obj)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@MCPRouter.delete('/{pk}',summary='删除 MCP 服务器',dependencies=[Depends(RequestPermission('sys:mcp:del')), DependsRBAC])
async def delete_mcp(pk: Annotated[int, Path(description='MCP ID')]) -> ResponseModel:
    count = await mcp_service.delete(pk=pk)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@MCPRouter.post('/chat',summary='MCP ChatGPT', dependencies=[Depends(RequestPermission('sys:mcp:chat')), DependsRBAC])
async def mcp_chat(obj: McpChatParam) -> StreamingResponse:
    data = await mcp_service.chat(obj=obj)
    return StreamingResponse(data, media_type='text/event-stream')