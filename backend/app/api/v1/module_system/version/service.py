# -*- coding: utf-8 -*-

from typing import Dict, List, Optional, Union
from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.exceptions import CustomException
from .crud import VersionCRUD
from .schema import VersionCreateSchema, VersionUpdateSchema, VersionOutSchema
from .param import VersionQueryParam


class VersionService:
    """版本模块服务层"""

    @classmethod
    async def get_version_detail_service(cls, auth: AuthSchema, id: int) -> Dict:
        """获取版本详情"""
        obj = await VersionCRUD(auth).get_by_id_crud(id=id)
        return VersionOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def get_version_list_service(cls, auth: AuthSchema, search: Optional[VersionQueryParam] = None, order_by: Optional[Union[str, List[Dict[str, str]]]] = None) -> List[Dict]:
        """获取版本列表"""
        # 处理排序参数
        processed_order_by = None
        if order_by:
            if isinstance(order_by, str):
                processed_order_by = eval(order_by)
            else:
                processed_order_by = order_by
                
        obj_list = await VersionCRUD(auth).get_list_crud(search=search.__dict__ if search else None, order_by=processed_order_by)
        return [VersionOutSchema.model_validate(obj).model_dump() for obj in obj_list]

    @classmethod
    async def create_version_service(cls, auth: AuthSchema, data: VersionCreateSchema) -> Dict:
        """创建版本"""
        # 检查版本号是否已存在
        exist_obj = await VersionCRUD(auth).get_by_number_crud(version_number=data.version_number)
        if exist_obj:
            raise CustomException(msg='创建失败，版本号已存在')
        obj = await VersionCRUD(auth).create_crud(data=data)
        return VersionOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def update_version_service(cls, auth: AuthSchema, id: int, data: VersionUpdateSchema) -> Dict:
        """更新版本"""
        # 检查版本是否存在
        obj = await VersionCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg='更新失败，该版本不存在')
        
        # 检查版本号是否重复（如果提供了版本号）
        if data.version_number:
            exist_obj = await VersionCRUD(auth).get_by_number_crud(version_number=data.version_number)
            if exist_obj and exist_obj.id != id:
                raise CustomException(msg='更新失败，版本号已存在')
                
        obj = await VersionCRUD(auth).update_crud(id=id, data=data)
        return VersionOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def delete_version_service(cls, auth: AuthSchema, ids: List[int]) -> None:
        """删除版本"""
        if len(ids) < 1:
            raise CustomException(msg='删除失败，删除对象不能为空')
        for id in ids:
            obj = await VersionCRUD(auth).get_by_id_crud(id=id)
            if not obj:
                raise CustomException(msg='删除失败，该版本不存在')
        await VersionCRUD(auth).delete_crud(ids=ids)

    @classmethod
    async def get_version_by_status_service(cls, auth: AuthSchema, search: Optional[VersionQueryParam] = None, order_by: Optional[Union[str, List[Dict[str, str]]]] = None) -> List[Dict]:
        """根据状态获取版本列表"""
        # 处理排序参数
        processed_order_by = None
        if order_by:
            if isinstance(order_by, str):
                processed_order_by = eval(order_by)
            else:
                processed_order_by = order_by
                
        obj_list = await VersionCRUD(auth).get_by_status_crud(
            search=search.__dict__ if search else None, 
            order_by=processed_order_by
        )
        return [VersionOutSchema.model_validate(obj).model_dump() for obj in obj_list]