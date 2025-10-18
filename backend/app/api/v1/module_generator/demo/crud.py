# -*- coding: utf-8 -*-

from typing import Dict, List, Optional, Sequence

from app.core.base_crud import CRUDBase
from app.api.v1.module_system.auth.schema import AuthSchema
from .model import DemoModel
from .schema import DemoCreateSchema, DemoUpdateSchema


class DemoCRUD(CRUDBase[DemoModel, DemoCreateSchema, DemoUpdateSchema]):
    """示例数据层"""

    def __init__(self, auth: AuthSchema) -> None:
        """
        初始化CRUD数据层
        
        参数:
        - auth (AuthSchema): 认证信息模型
        """
        super().__init__(model=DemoModel, auth=auth)

    async def get_by_id_crud(self, id: int) -> Optional[DemoModel]:
        """
        详情
        
        参数:
        - id (int): 示例ID
        
        返回:
        - Optional[DemoModel]: 示例模型实例或None
        """
        return await self.get(id=id)
    
    async def list_crud(self, search: Optional[Dict] = None, order_by: Optional[List[Dict[str, str]]] = None) -> Sequence[DemoModel]:
        """
        列表查询
        
        参数:
        - search (Optional[Dict]): 查询参数
        - order_by (Optional[List[Dict[str, str]]]): 排序参数
        
        返回:
        - Sequence[DemoModel]: 示例模型实例序列
        """
        return await self.list(search=search, order_by=order_by)
    
    async def create_crud(self, data: DemoCreateSchema) -> Optional[DemoModel]:
        """
        创建
        
        参数:
        - data (DemoCreateSchema): 示例创建模型
        
        返回:
        - Optional[DemoModel]: 示例模型实例或None
        """
        return await self.create(data=data)
    
    async def update_crud(self, id: int, data: DemoUpdateSchema) -> Optional[DemoModel]:
        """
        更新
        
        参数:
        - id (int): 示例ID
        - data (DemoUpdateSchema): 示例更新模型
        
        返回:
        - Optional[DemoModel]: 示例模型实例或None
        """
        return await self.update(id=id, data=data)
    
    async def delete_crud(self, ids: List[int]) -> None:
        """
        批量删除
        
        参数:
        - ids (List[int]): 示例ID列表
        
        返回:
        - None
        """
        return await self.delete(ids=ids)
    
    async def set_available_crud(self, ids: List[int], status: bool) -> None:
        """
        批量设置可用状态
        
        参数:
        - ids (List[int]): 示例ID列表
        - status (bool): 可用状态
        
        返回:
        - None
        """
        return await self.set(ids=ids, status=status)