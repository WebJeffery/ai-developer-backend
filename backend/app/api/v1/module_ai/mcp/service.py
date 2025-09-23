# -*- coding: utf-8 -*-

from typing import AsyncGenerator, List, Dict, Optional, Any

from app.core.exceptions import CustomException
from app.core.logger import logger
from app.api.v1.module_system.auth.schema import AuthSchema
from app.utils.ai_util import AIClient
from .schema import McpCreateSchema, McpUpdateSchema, McpOutSchema, ChatQuerySchema
from .param import McpQueryParam
from .crud import McpCRUD
from .model import McpModel


class McpService:
    """MCP服务层"""

    @classmethod
    async def get_mcp_detail_service(cls, auth: AuthSchema, id: int) -> Dict[str, Any]:
        """详情"""
        obj = await McpCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg='MCP 服务器不存在')
        return McpOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def get_mcp_list_service(cls, auth: AuthSchema, search: Optional[McpQueryParam] = None, order_by: Optional[List[Dict[str, str]]] = None) -> List[Dict[str, Any]]:
        """列表查询"""
        if order_by:
            order_by = eval(str(order_by))
        obj_list = await McpCRUD(auth).get_list_crud(search=search.__dict__ if search else {}, order_by=order_by)
        return [McpOutSchema.model_validate(obj).model_dump() for obj in obj_list]
    
    @classmethod
    async def create_mcp_service(cls, auth: AuthSchema, data: McpCreateSchema) -> Dict[str, Any]:
        """创建"""
        obj = await McpCRUD(auth).get_by_name_crud(name=data.name)
        if obj:
            raise CustomException(msg='创建失败，MCP 服务器已存在')
        obj = await McpCRUD(auth).create_crud(data=data)
        return McpOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def update_mcp_service(cls, auth: AuthSchema, id: int, data: McpUpdateSchema) -> Dict[str, Any]:
        """更新"""
        obj = await McpCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg='更新失败，该数据不存在')
        exist_obj = await McpCRUD(auth).get_by_name_crud(name=data.name)
        if exist_obj and exist_obj.id != id:
            raise CustomException(msg='更新失败，MCP 服务器名称重复')
        obj = await McpCRUD(auth).update_crud(id=id, data=data)
        return McpOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def delete_mcp_service(cls, auth: AuthSchema, ids: List[int]) -> None:
        """删除"""
        if len(ids) < 1:
            raise CustomException(msg='删除失败，删除对象不能为空')
        for id in ids:
            obj = await McpCRUD(auth).get_by_id_crud(id=id)
            if not obj:
                raise CustomException(msg='删除失败，该数据不存在')
        await McpCRUD(auth).delete_crud(ids=ids)
    
    @classmethod
    async def chat_query(cls, query: ChatQuerySchema):
        """处理聊天查询"""
        # 创建MCP客户端实例
        mcp_client = AIClient()
        try:
            # 处理消息
            async for response in mcp_client.process(query.message):
                yield response
        finally:
            # 确保关闭客户端连接
            await mcp_client.close()
