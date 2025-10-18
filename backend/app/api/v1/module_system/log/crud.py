# -*- coding: utf-8 -*-

from typing import Dict, List, Optional, Sequence

from app.core.base_crud import CRUDBase
from ..auth.schema import AuthSchema
from .model import OperationLogModel
from .schema import OperationLogCreateSchema


class OperationLogCRUD(CRUDBase[OperationLogModel, OperationLogCreateSchema, OperationLogCreateSchema]):
    """
    操作日志数据层。
    """

    def __init__(self, auth: AuthSchema) -> None:
        """
        初始化操作日志CRUD。
        """
        self.auth = auth
        super().__init__(model=OperationLogModel, auth=auth)

    async def create_crud(self, data: OperationLogCreateSchema) -> Optional[OperationLogModel]:
        """
        创建操作日志记录。
        
        参数:
        - data (OperationLogCreateSchema): 操作日志创建模型。
        
        返回:
        - OperationLogModel | None: 创建后的日志记录。
        """
        return await self.create(data=data)

    async def get_by_id_crud(self, id: int) -> Optional[OperationLogModel]:
        """
        根据ID获取操作日志详情。
        
        参数:
        - id (int): 操作日志ID。
        
        返回:
        - OperationLogModel | None: 操作日志记录。
        """
        return await self.get(id=id)

    async def get_list_crud(self, search: Optional[Dict] = None, order_by: Optional[List[Dict[str, str]]] = None) -> Sequence[OperationLogModel]:
        """
        获取操作日志列表。
        
        参数:
        - search (Dict | None): 搜索条件字典。
        - order_by (List[Dict[str, str]] | None): 排序字段列表。
        
        返回:
        - Sequence[OperationLogModel]: 操作日志列表。
        """
        return await self.list(search=search, order_by=order_by)

