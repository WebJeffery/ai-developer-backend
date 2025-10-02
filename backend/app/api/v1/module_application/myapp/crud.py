# -*- coding: utf-8 -*-

from typing import Dict, List, Optional, Sequence

from app.core.base_crud import CRUDBase
from app.api.v1.module_system.auth.schema import AuthSchema
from .model import ApplicationModel
from .schema import ApplicationCreateSchema, ApplicationUpdateSchema


class ApplicationCRUD(CRUDBase[ApplicationModel, ApplicationCreateSchema, ApplicationUpdateSchema]):
    """应用系统数据层"""

    def __init__(self, auth: AuthSchema) -> None:
        """初始化CRUD"""
        self.auth = auth
        super().__init__(model=ApplicationModel, auth=auth)

    async def get_by_id_crud(self, id: int) -> Optional[ApplicationModel]:
        """获取应用详情"""
        return await self.get(id=id)
    
    async def list_crud(self, search: Optional[Dict] = None, order_by: Optional[List[Dict[str, str]]] = None) -> Sequence[ApplicationModel]:
        """列表查询"""
        return await self.list(search=search, order_by=order_by)
    
    async def create_crud(self, data: ApplicationCreateSchema) -> Optional[ApplicationModel]:
        """创建应用"""
        return await self.create(data=data)
    
    async def update_crud(self, id: int, data: ApplicationUpdateSchema) -> Optional[ApplicationModel]:
        """更新应用"""
        return await self.update(id=id, data=data)
    
    async def delete_crud(self, ids: List[int]) -> None:
        """批量删除应用"""
        return await self.delete(ids=ids)
    
    async def set_available_crud(self, ids: List[int], status: bool) -> None:
        """批量设置可用状态"""
        return await self.set(ids=ids, status=status)