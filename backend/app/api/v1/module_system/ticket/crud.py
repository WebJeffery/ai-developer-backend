from typing import Dict, List, Optional, Sequence

from app.core.base_crud import CRUDBase
from app.api.v1.module_system.auth.schema import AuthSchema
from .model import TicketModel
from .schema import TicketCreateSchema, TicketUpdateSchema


class TicketCRUD(CRUDBase[TicketModel, TicketCreateSchema, TicketUpdateSchema]):
    """工单 CRUD 操作"""

    def __init__(self, auth: AuthSchema) -> None:
        """初始化工单CRUD"""
        self.auth = auth
        super().__init__(model=TicketModel, auth=auth)

    async def get_by_id_crud(self, id: int) -> Optional[TicketModel]:
        """根据id获取工单信息
        
        :param id: 工单ID
        :return: 工单信息
        """
        return await self.get(id=id)

    async def get_list_crud(self, search: Optional[Dict] = None, order_by: Optional[List[Dict[str, str]]] = None) -> Sequence[TicketModel]:
        """获取工单列表
        
        :param search: 搜索条件
        :param order_by: 排序字段
        :return: 工单列表
        """
        return await self.list(search=search or {}, order_by=order_by or [])

    async def create_crud(self, data: TicketCreateSchema) -> Optional[TicketModel]:
        """创建工单
        
        :param data: 工单创建数据
        :return: 创建的工单
        """
        return await self.create(data=data)

    async def update_crud(self, id: int, data: TicketUpdateSchema) -> Optional[TicketModel]:
        """更新工单
        
        :param id: 工单ID
        :param data: 工单更新数据
        :return: 更新的工单
        """
        return await self.update(id=id, data=data)

    async def delete_crud(self, ids: List[int]) -> None:
        """批量删除工单
        
        :param ids: 工单ID列表
        """
        return await self.delete(ids=ids)