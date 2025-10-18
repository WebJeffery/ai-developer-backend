# -*- coding: utf-8 -*-

from typing import Dict, List, Optional, Sequence

from app.core.base_crud import CRUDBase
from ..auth.schema import AuthSchema
from .model import NoticeModel
from .schema import NoticeCreateSchema, NoticeUpdateSchema


class NoticeCRUD(CRUDBase[NoticeModel, NoticeCreateSchema, NoticeUpdateSchema]):
    """公告数据层"""

    def __init__(self, auth: AuthSchema) -> None:
        """
        初始化公告数据层。
        
        参数:
        - auth (AuthSchema): 认证信息模型。
        """
        self.auth = auth
        super().__init__(model=NoticeModel, auth=auth)

    async def get_by_id_crud(self, id: int) -> Optional[NoticeModel]:
        """
        根据ID获取公告详情。
        
        参数:
        - id (int): 公告ID。
        
        返回:
        - Optional[NoticeModel]: 公告模型实例。
        """
        return await self.get(id=id)
    
    async def get_list_crud(self, search: Optional[Dict] = None, order_by: Optional[List[Dict[str, str]]] = None) -> Sequence[NoticeModel]:
        """
        获取公告列表。
        
        参数:
        - search (Optional[Dict]): 查询参数。
        - order_by (Optional[List[Dict[str, str]]]): 排序参数。
        
        返回:
        - Sequence[NoticeModel]: 公告模型实例列表。
        """
        return await self.list(search=search, order_by=order_by)
    
    async def create_crud(self, data: NoticeCreateSchema) -> Optional[NoticeModel]:
        """
        创建公告。
        
        参数:
        - data (NoticeCreateSchema): 公告创建模型。
        
        返回:
        - Optional[NoticeModel]: 公告模型实例。
        """
        return await self.create(data=data)
    
    async def update_crud(self, id: int, data: NoticeUpdateSchema) -> Optional[NoticeModel]:
        """
        更新公告。
        
        参数:
        - id (int): 公告ID。
        - data (NoticeUpdateSchema): 公告更新模型。
        
        返回:
        - Optional[NoticeModel]: 公告模型实例。
        """
        return await self.update(id=id, data=data)
    
    async def delete_crud(self, ids: List[int]) -> None:
        """
        删除公告。
        
        参数:
        - ids (List[int]): 公告ID列表。
        
        返回:
        - None
        """
        return await self.delete(ids=ids)
    
    async def set_available_crud(self, ids: List[int], status: bool) -> None:
        """
        设置公告的可用状态。
        
        参数:
        - ids (List[int]): 公告ID列表。
        - status (bool): 可用状态。
        
        返回:
        - None
        """
        return await self.set(ids=ids, status=status)