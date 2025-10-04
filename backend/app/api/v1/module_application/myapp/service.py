# -*- coding: utf-8 -*-

from typing import List, Dict, Optional

from app.core.base_schema import BatchSetAvailable
from app.core.exceptions import CustomException
from app.core.logger import logger
from app.api.v1.module_system.auth.schema import AuthSchema
from .schema import ApplicationCreateSchema, ApplicationUpdateSchema, ApplicationOutSchema
from .param import ApplicationQueryParam
from .crud import ApplicationCRUD


class ApplicationService:
    """
    应用系统管理服务层
    """
    
    @classmethod
    async def detail_service(cls, auth: AuthSchema, id: int) -> Dict:
        """获取应用详情"""
        obj = await ApplicationCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg='应用不存在')
        return ApplicationOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def list_service(cls, auth: AuthSchema, search: Optional[ApplicationQueryParam] = None, order_by: Optional[List[Dict[str, str]]] = None) -> List[Dict]:
        """应用列表查询"""
        if order_by:
            order_by = eval(order_by) if isinstance(order_by, str) else order_by
        
        # 过滤空值
        search_dict = {k: v for k, v in search.__dict__.items() if v is not None} if search else {}
        obj_list = await ApplicationCRUD(auth).list_crud(search=search_dict, order_by=order_by)
        return [ApplicationOutSchema.model_validate(obj).model_dump() for obj in obj_list]
    
    @classmethod
    async def create_service(cls, auth: AuthSchema, data: ApplicationCreateSchema) -> Dict:
        """创建应用"""
        # 检查名称是否重复
        obj = await ApplicationCRUD(auth).get(name=data.name)
        if obj:
            raise CustomException(msg='创建失败，应用名称已存在')
        
        obj = await ApplicationCRUD(auth).create_crud(data=data)
        return ApplicationOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def update_service(cls, auth: AuthSchema, id: int, data: ApplicationUpdateSchema) -> Dict:
        """更新应用"""
        obj = await ApplicationCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg='更新失败，该应用不存在')
        
        # 检查名称重复
        exist_obj = await ApplicationCRUD(auth).get(name=data.name)
        if exist_obj and exist_obj.id != id:
            raise CustomException(msg='更新失败，应用名称重复')
        
        obj = await ApplicationCRUD(auth).update_crud(id=id, data=data)
        return ApplicationOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def delete_service(cls, auth: AuthSchema, ids: list[int]) -> None:
        """删除应用"""
        if len(ids) < 1:
            raise CustomException(msg='删除失败，删除对象不能为空')
        for id in ids:
            obj = await ApplicationCRUD(auth).get_by_id_crud(id=id)
            if not obj:
                raise CustomException(msg=f'删除失败，应用 {id} 不存在')
        await ApplicationCRUD(auth).delete_crud(ids=ids)
    
    @classmethod
    async def set_available_service(cls, auth: AuthSchema, data: BatchSetAvailable) -> None:
        """批量设置应用状态"""
        await ApplicationCRUD(auth).set_available_crud(ids=data.ids, status=data.status)