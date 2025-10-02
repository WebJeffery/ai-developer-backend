# -*- coding: utf-8 -*-

from typing import Any, List, Dict, Optional


from app.core.base_schema import BatchSetAvailable
from app.core.exceptions import CustomException
from app.utils.excel_util import ExcelUtil
from ..auth.schema import AuthSchema
from .schema import NoticeCreateSchema, NoticeUpdateSchema, NoticeOutSchema
from .param import NoticeQueryParam
from .crud import NoticeCRUD


class NoticeService:
    """
    公告管理模块服务层
    """
    
    @classmethod
    async def get_notice_detail_service(cls, auth: AuthSchema, id: int) -> Dict:
        notice_obj = await NoticeCRUD(auth).get_by_id_crud(id=id)
        return NoticeOutSchema.model_validate(notice_obj).model_dump()
    
    @classmethod
    async def get_notice_list_available_service(cls, auth: AuthSchema) -> List[Dict]:
        notice_obj_list = await NoticeCRUD(auth).get_list_crud(search={'status': True})
        return [NoticeOutSchema.model_validate(notice_obj).model_dump() for notice_obj in notice_obj_list]

    @classmethod
    async def get_notice_list_service(cls, auth: AuthSchema, search: Optional[NoticeQueryParam] = None, order_by: Optional[List[Dict[str, str]]] = None) -> List[Dict]:
        notice_obj_list = await NoticeCRUD(auth).get_list_crud(search=search.__dict__, order_by=order_by)
        return [NoticeOutSchema.model_validate(notice_obj).model_dump() for notice_obj in notice_obj_list]
    
    @classmethod
    async def create_notice_service(cls, auth: AuthSchema, data: NoticeCreateSchema) -> Dict:
        notice = await NoticeCRUD(auth).get(notice_title=data.notice_title)
        if notice:
            raise CustomException(msg='创建失败，该公告通知已存在')
        notice_obj = await NoticeCRUD(auth).create_crud(data=data)
        return NoticeOutSchema.model_validate(notice_obj).model_dump()
    
    @classmethod
    async def update_notice_service(cls, auth: AuthSchema, id: int, data: NoticeUpdateSchema) -> Dict:
        notice = await NoticeCRUD(auth).get_by_id_crud(id=id)
        if not notice:
            raise CustomException(msg='更新失败，该公告通知不存在')
        exist_notice = await NoticeCRUD(auth).get(notice_title=data.notice_title)
        if exist_notice and exist_notice.id != id:
            raise CustomException(msg='更新失败，公告通知标题重复')
        notice_obj = await NoticeCRUD(auth).update_crud(id=id, data=data)
        return NoticeOutSchema.model_validate(notice_obj).model_dump()
    
    @classmethod
    async def delete_notice_service(cls, auth: AuthSchema, ids: list[int]) -> None:
        if len(ids) < 1:
            raise CustomException(msg='删除失败，删除对象不能为空')
        for id in ids:
            notice = await NoticeCRUD(auth).get_by_id_crud(id=id)
            if not notice:
                raise CustomException(msg='删除失败，该公告通知不存在')
        await NoticeCRUD(auth).delete_crud(ids=ids)
    
    @classmethod
    async def set_notice_available_service(cls, auth: AuthSchema, data: BatchSetAvailable) -> None:
        await NoticeCRUD(auth).set_available_crud(ids=data.ids, status=data.status)
    
    @classmethod
    async def export_notice_service(cls, notice_list: List[Dict[str, Any]]) -> bytes:
        """导出公告列表"""
        mapping_dict = {
            'id': '编号',
            'notice_title': '公告标题', 
            'notice_type': '公告类型（1通知 2公告）',
            'notice_content': '公告内容',
            'status': '状态',
            'description': '备注',
            'created_at': '创建时间',
            'updated_at': '更新时间',
            'creator_id': '创建者ID',
            'creator': '创建者',
        }

        # 复制数据并转换状态
        data = notice_list.copy()
        for item in data:
            # 处理状态
            item['status'] = '正常' if item.get('status') else '停用'
            # 处理公告类型
            item['notice_type'] = '通知' if item.get('notice_type') == '1' else '公告'
            item['creator'] = item.get('creator', {}).get('name', '未知') if isinstance(item.get('creator'), dict) else '未知'

        return ExcelUtil.export_list2excel(list_data=data, mapping_dict=mapping_dict)