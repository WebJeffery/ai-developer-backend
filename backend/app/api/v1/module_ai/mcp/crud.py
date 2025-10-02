# -*- coding: utf-8 -*-

from typing import Dict, List, Optional, Sequence

from app.core.base_crud import CRUDBase
from app.api.v1.module_system.auth.schema import AuthSchema
from .model import McpModel
from .schema import McpCreateSchema, McpUpdateSchema


class McpCRUD(CRUDBase[McpModel, McpCreateSchema, McpUpdateSchema]):
    """MCP 服务器数据层"""

    def __init__(self, auth: AuthSchema) -> None:
        """初始化CRUD"""
        self.auth = auth
        super().__init__(model=McpModel, auth=auth)

    async def get_by_id_crud(self, id: int) -> Optional[McpModel]:
        """详情"""
        return await self.get(id=id)
    
    async def get_by_name_crud(self, name: str) -> Optional[McpModel]:
        """通过名称获取MCP服务器"""
        return await self.get(name=name)
    
    async def get_list_crud(self, search: Optional[Dict] = None, order_by: Optional[List[Dict[str, str]]] = None) -> Sequence[McpModel]:
        """列表查询"""
        return await self.list(search=search or {}, order_by=order_by or [{'id': 'asc'}])
    
    async def create_crud(self, data: McpCreateSchema) -> Optional[McpModel]:
        """创建"""
        return await self.create(data=data)
    
    async def update_crud(self, id: int, data: McpUpdateSchema) -> Optional[McpModel]:
        """更新"""
        return await self.update(id=id, data=data)
    
    async def delete_crud(self, ids: List[int]) -> None:
        """批量删除"""
        return await self.delete(ids=ids)
