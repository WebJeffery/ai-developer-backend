# -*- coding: utf-8 -*-

from typing import Dict, List, Optional, Union
from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.exceptions import CustomException
from .crud import TicketCRUD
from .schema import TicketCreateSchema, TicketUpdateSchema, TicketOutSchema
from .param import TicketQueryParam


class TicketService:
    """工单模块服务层"""

    @classmethod
    async def get_ticket_detail_service(cls, auth: AuthSchema, id: int) -> Dict:
        """获取工单详情"""
        obj = await TicketCRUD(auth).get_by_id_crud(id=id)
        return TicketOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def get_ticket_list_service(cls, auth: AuthSchema, search: Optional[TicketQueryParam] = None, order_by: Optional[Union[str, List[Dict[str, str]]]] = None) -> List[Dict]:
        """获取工单列表"""
        # 处理排序参数
        processed_order_by = None
        if order_by:
            if isinstance(order_by, str):
                processed_order_by = eval(order_by)
            else:
                processed_order_by = order_by
                
        obj_list = await TicketCRUD(auth).get_list_crud(search=search.__dict__ if search else None, order_by=processed_order_by)
        return [TicketOutSchema.model_validate(obj).model_dump() for obj in obj_list]

    @classmethod
    async def create_ticket_service(cls, auth: AuthSchema, data: TicketCreateSchema) -> Dict:
        """创建工单"""
        obj = await TicketCRUD(auth).create_crud(data=data)
        return TicketOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def update_ticket_service(cls, auth: AuthSchema, id: int, data: TicketUpdateSchema) -> Dict:
        """更新工单"""
        # 检查工单是否存在
        obj = await TicketCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg='更新失败，该工单不存在')
                
        obj = await TicketCRUD(auth).update_crud(id=id, data=data)
        return TicketOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def delete_ticket_service(cls, auth: AuthSchema, ids: List[int]) -> None:
        """删除工单"""
        if len(ids) < 1:
            raise CustomException(msg='删除失败，删除对象不能为空')
        for id in ids:
            obj = await TicketCRUD(auth).get_by_id_crud(id=id)
            if not obj:
                raise CustomException(msg='删除失败，该工单不存在')
        await TicketCRUD(auth).delete_crud(ids=ids)