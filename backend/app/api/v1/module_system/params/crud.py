# -*- coding: utf-8 -*-

from typing import Dict, List, Optional, Sequence

from app.core.base_crud import CRUDBase
from ..auth.schema import AuthSchema
from .model import ParamsModel
from .schema import ParamsCreateSchema, ParamsUpdateSchema


class ParamsCRUD(CRUDBase[ParamsModel, ParamsCreateSchema, ParamsUpdateSchema]):
    """配置管理数据层"""

    def __init__(self, auth: AuthSchema) -> None:
        """初始化配置CRUD"""
        self.auth = auth
        super().__init__(model=ParamsModel, auth=auth)
    
    async def get_obj_by_id_crud(self, id: int) -> Optional[ParamsModel]:
        """获取配置管理型详情"""
        return await self.get(id=id)
    
    async def get_obj_by_key_crud(self, key: str) -> Optional[ParamsModel]:
        """根据key获取配置管理型详情"""
        return await self.get(config_key=key)
    
    async def get_obj_list_crud(self, search: Dict = None, order_by: List[Dict[str, str]] = None) -> Sequence[ParamsModel]:
        """获取配置管理型列表"""
        return await self.list(search=search, order_by=order_by)
    
    async def create_obj_crud(self, data: ParamsCreateSchema) -> Optional[ParamsModel]:
        """创建配置管理型"""
        return await self.create(data=data)
    
    async def update_obj_crud(self, id: int, data: ParamsUpdateSchema) -> Optional[ParamsModel]:
        """更新配置管理型"""
        return await self.update(id=id, data=data)
    
    async def delete_obj_crud(self, ids: List[int]) -> None:
        """删除配置管理型"""
        return await self.delete(ids=ids)
