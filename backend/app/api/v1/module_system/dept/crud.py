# -*- coding: utf-8 -*-

from typing import Dict, List, Optional, Sequence

from app.core.base_crud import CRUDBase
from ..auth.schema import AuthSchema
from .model import DeptModel
from .schema import DeptCreateSchema, DeptUpdateSchema


class DeptCRUD(CRUDBase[DeptModel, DeptCreateSchema, DeptUpdateSchema]):
    """部门模块数据层"""

    def __init__(self, auth: AuthSchema) -> None:
        """初始化部门CRUD"""
        self.auth = auth
        super().__init__(model=DeptModel, auth=auth)

    async def get_by_id_crud(self, id: int) -> Optional[DeptModel]:
        """
        根据id获取部门信息
        
        :param id: 部门ID
        :return: 部门信息
        """
        obj = await self.get(id=id)
        if not obj:
            return None
        return obj

    async def get_list_crud(self, search: Optional[Dict] = None, order_by: Optional[List[Dict[str, str]]] = None) -> Sequence[DeptModel]:
        """
        获取部门列表
        
        :param search: 搜索条件
        :param order_by: 排序字段
        :return: 部门列表
        """
        return await self.list(search=search, order_by=order_by)

    async def get_tree_list_crud(self, search: Optional[Dict] = None, order_by: Optional[List[Dict[str, str]]] = None) -> Sequence[DeptModel]:
        """
        获取部门树形列表
        
        :param search: 搜索条件
        :param order_by: 排序字段
        :return: 部门树形列表
        """
        return await self.tree_list(search=search, order_by=order_by, children_attr='children')

    async def set_available_crud(self, ids: List[int], status: bool) -> None:
        """
        批量设置部门可用状态
        
        :param ids: 部门ID列表
        :param status: 可用状态
        """
        await self.set(ids=ids, status=status)

    async def get_name_crud(self, id: int) -> Optional[str]:
        """
        根据id获取部门名称
        """
        obj = await self.get(id=id)
        return obj.name if obj else None
