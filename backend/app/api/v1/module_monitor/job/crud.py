# -*- coding: utf-8 -*-

from typing import Dict, List, Optional, Sequence

from app.core.base_crud import CRUDBase
from app.api.v1.module_system.auth.schema import AuthSchema
from .model import JobModel, JobLogModel
from .schema import JobCreateSchema,JobUpdateSchema,JobLogCreateSchema,JobLogUpdateSchema



class JobCRUD(CRUDBase[JobModel, JobCreateSchema, JobUpdateSchema]):
    """定时任务数据层"""

    def __init__(self, auth: AuthSchema) -> None:
        """初始化定时任务CRUD"""
        self.auth = auth
        super().__init__(model=JobModel, auth=auth)

    async def get_obj_by_id_crud(self, id: int) -> Optional[JobModel]:
        """获取定时任务详情"""
        return await self.get(id=id)
    
    async def get_obj_list_crud(self, search: Optional[Dict] = None, order_by: Optional[List[Dict[str, str]]] = None) -> Sequence[JobModel]:
        """获取定时任务列表"""
        return await self.list(search=search, order_by=order_by)
    
    async def create_obj_crud(self, data: JobCreateSchema) -> Optional[JobModel]:
        """创定时任务"""
        return await self.create(data=data)
    
    async def update_obj_crud(self, id: int, data: JobUpdateSchema) -> Optional[JobModel]:
        """更新定时任务"""
        return await self.update(id=id, data=data)
    
    async def delete_obj_crud(self, ids: List[int]) -> None:
        """删除定时任务"""
        return await self.delete(ids=ids)
    
    async def set_obj_field_crud(self, ids: List[int], **kwargs) -> None:
        """设置定时任务的可用状态"""
        return await self.set(ids=ids, **kwargs)
    
    async def clear_obj_crud(self) -> None:
        """清除定时任务日志"""
        return await self.clear()


class JobLogCRUD(CRUDBase[JobLogModel, JobLogCreateSchema, JobLogUpdateSchema]):
    """定时任务日志数据层"""

    def __init__(self, auth: AuthSchema) -> None:
        """初始化定时任务日志CRUD"""
        self.auth = auth
        super().__init__(model=JobLogModel, auth=auth)

    async def get_obj_log_by_id_crud(self, id: int) -> Optional[JobLogModel]:
        """获取定时任务日志详情"""
        return await self.get(id=id)
    
    async def get_obj_log_list_crud(self, search: Optional[Dict] = None, order_by: Optional[List[Dict[str, str]]] = None) -> Sequence[JobLogModel]:
        """获取定时任务日志列表"""
        return await self.list(search=search, order_by=order_by)
    
    async def create_obj_log_crud(self, data: JobLogCreateSchema) -> Optional[JobLogModel]:
        """创建定时任务日志"""
        return await self.create(data=data)
    
    async def delete_obj_log_crud(self, ids: List[int]) -> None:
        """删除定时任务日志"""
        return await self.delete(ids=ids)