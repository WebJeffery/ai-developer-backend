# -*- coding: utf-8 -*-

from typing import Dict, List, Optional, Sequence

from app.core.base_crud import CRUDBase
from app.api.v1.module_system.auth.schema import AuthSchema
from .model import VersionModel
from .schema import VersionCreateSchema, VersionUpdateSchema


class VersionCRUD(CRUDBase[VersionModel, VersionCreateSchema, VersionUpdateSchema]):
    """版本模块数据层"""

    def __init__(self, auth: AuthSchema) -> None:
        """初始化版本CRUD"""
        self.auth = auth
        super().__init__(model=VersionModel, auth=auth)

    async def get_by_id_crud(self, id: int) -> Optional[VersionModel]:
        """根据id获取版本信息
        
        :param id: 版本ID
        :return: 版本信息
        """
        return await self.get(id=id)

    async def get_list_crud(self, search: Optional[Dict] = None, order_by: Optional[List[Dict[str, str]]] = None) -> Sequence[VersionModel]:
        """获取版本列表
        
        :param search: 搜索条件
        :param order_by: 排序字段
        :return: 版本列表
        """
        return await self.list(search=search or {}, order_by=order_by or [])

    async def create_crud(self, data: VersionCreateSchema) -> Optional[VersionModel]:
        """创建版本
        
        :param data: 版本创建数据
        :return: 创建的版本
        """
        return await self.create(data=data)

    async def update_crud(self, id: int, data: VersionUpdateSchema) -> Optional[VersionModel]:
        """更新版本
        
        :param id: 版本ID
        :param data: 版本更新数据
        :return: 更新的版本
        """
        return await self.update(id=id, data=data)

    async def delete_crud(self, ids: List[int]) -> None:
        """批量删除版本
        
        :param ids: 版本ID列表
        """
        return await self.delete(ids=ids)

    async def get_by_number_crud(self, version_number: str) -> Optional[VersionModel]:
        """根据版本号获取版本
        
        :param version_number: 版本号
        :return: 版本信息
        """
        return await self.get(version_number=version_number)

    async def get_by_status_crud(self, status: str, search: Optional[Dict] = None, order_by: Optional[List[Dict[str, str]]] = None) -> Sequence[VersionModel]:
        """根据状态获取版本列表
        
        :param status: 版本状态
        :param search: 搜索条件
        :param order_by: 排序字段
        :return: 版本列表
        """
        if search is None:
            search = {}
        search['version_status'] = status
        return await self.list(search=search, order_by=order_by or [])