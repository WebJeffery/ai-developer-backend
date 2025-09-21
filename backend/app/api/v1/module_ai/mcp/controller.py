# -*- coding: utf-8 -*-

from fastapi import APIRouter, Depends, Path, Query, Body, WebSocket
from fastapi.responses import JSONResponse, StreamingResponse

from app.common.response import StreamResponse, SuccessResponse
from app.common.request import PaginationService
from app.core.base_params import PaginationQueryParam
from app.core.dependencies import AuthPermission
from app.core.router_class import OperationLogRoute
from app.core.logger import logger
from app.api.v1.module_system.auth.schema import AuthSchema
from .param import McpQueryParam
from .service import McpService
from .schema import McpCreateSchema, McpUpdateSchema, ChatQuerySchema


MCPRouter = APIRouter(route_class=OperationLogRoute, prefix="/mcp", tags=["MCP智能助手"])


@MCPRouter.post("/chat", summary="智能对话", description="与MCP智能助手进行对话")
async def chat_controller(
    query: ChatQuerySchema,
    auth: AuthSchema = Depends(AuthPermission(permissions=["ai:mcp:chat"]))
) -> StreamingResponse:
    """智能对话接口"""
    user_name = auth.user.name if auth.user else "未知用户"
    logger.info(f"用户 {user_name} 发起智能对话: {query.message[:50]}...")
    
    async def generate_response():
        try:
            async for chunk in McpService.chat_query(query=query):
                # 确保返回的是字节串
                if chunk:
                    yield chunk.encode('utf-8') if isinstance(chunk, str) else chunk
        except Exception as e:
            logger.error(f"流式响应出错: {str(e)}")
            yield f"抱歉，处理您的请求时出现了错误: {str(e)}".encode('utf-8')
    
    return StreamResponse(generate_response(), media_type="text/plain; charset=utf-8")


@MCPRouter.get("/detail/{id}", summary="获取 MCP 服务器详情", description="获取 MCP 服务器详情")
async def get_mcp_detail_controller(
    id: int = Path(..., description="MCP ID"),
    auth: AuthSchema = Depends(AuthPermission(permissions=["ai:mcp:query"]))
) -> JSONResponse:
    result_dict = await McpService.get_mcp_detail_service(auth=auth, id=id)
    logger.info(f"获取 MCP 服务器详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取 MCP 服务器详情成功")


@MCPRouter.get("/list", summary="查询 MCP 服务器列表", description="查询 MCP 服务器列表")
async def get_mcp_list_controller(
    page: PaginationQueryParam = Depends(),
    search: McpQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(permissions=["ai:mcp:query"]))
) -> JSONResponse:
    result_dict_list = await McpService.get_mcp_list_service(auth=auth, search=search, order_by=page.order_by)
    result_dict = await PaginationService.paginate(data_list=result_dict_list, page_no=page.page_no, page_size=page.page_size)
    logger.info(f"查询 MCP 服务器列表成功")
    return SuccessResponse(data=result_dict, msg="查询 MCP 服务器列表成功")


@MCPRouter.post("/create", summary="创建 MCP 服务器", description="创建 MCP 服务器")
async def create_mcp_controller(
    data: McpCreateSchema,
    auth: AuthSchema = Depends(AuthPermission(permissions=["ai:mcp:create"]))
) -> JSONResponse:
    result_dict = await McpService.create_mcp_service(auth=auth, data=data)
    logger.info(f"创建 MCP 服务器成功: {result_dict}")
    return SuccessResponse(data=result_dict, msg="创建 MCP 服务器成功")


@MCPRouter.put("/update/{id}", summary="修改 MCP 服务器", description="修改 MCP 服务器")
async def update_mcp_controller(
    data: McpUpdateSchema,
    id: int = Path(..., description="MCP ID"),
    auth: AuthSchema = Depends(AuthPermission(permissions=["ai:mcp:update"]))
) -> JSONResponse:
    result_dict = await McpService.update_mcp_service(auth=auth, id=id, data=data)
    logger.info(f"修改 MCP 服务器成功: {result_dict}")
    return SuccessResponse(data=result_dict, msg="修改 MCP 服务器成功")


@MCPRouter.delete("/delete", summary="删除 MCP 服务器", description="删除 MCP 服务器")
async def delete_mcp_controller(
    ids: list[int] = Body(..., description="ID列表"),
    auth: AuthSchema = Depends(AuthPermission(permissions=["ai:mcp:delete"]))
) -> JSONResponse:
    await McpService.delete_mcp_service(auth=auth, ids=ids)
    logger.info(f"删除 MCP 服务器成功: {ids}")
    return SuccessResponse(msg="删除 MCP 服务器成功")


@MCPRouter.websocket("/ws/chat", name="WebSocket聊天")
async def websocket_chat_controller(
    query: ChatQuerySchema,
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
                async for chunk in McpService.chat_query(query=query):
                    if chunk:
                        await websocket.send_text(chunk)
            except Exception as e:
                logger.error(f"处理聊天查询出错: {str(e)}")
                await websocket.send_text(f"抱歉，处理您的请求时出现了错误: {str(e)}")
    except Exception as e:
        logger.error(f"WebSocket聊天出错: {str(e)}")
    finally:
        await websocket.close()
