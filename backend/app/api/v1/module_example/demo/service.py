# -*- coding: utf-8 -*-

import io
from typing import Any, List, Dict, Optional
from fastapi import UploadFile
import pandas as pd

from app.core.base_schema import BatchSetAvailable
from app.core.exceptions import CustomException
from app.utils.excel_util import ExcelUtil
from app.common.response import ErrorResponse
from app.core.logger import logger
from app.api.v1.module_system.auth.schema import AuthSchema
from .schema import DemoCreateSchema, DemoUpdateSchema, DemoOutSchema
from .param import DemoQueryParam
from .crud import DemoCRUD


class DemoService:
    """
    示例管理模块服务层
    """
    
    @classmethod
    async def get_demo_detail_service(cls, auth: AuthSchema, id: int) -> Dict:
        """详情"""
        obj = await DemoCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg="该数据不存在")
        return DemoOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def get_demo_list_service(cls, auth: AuthSchema, search: Optional[DemoQueryParam] = None, order_by: Optional[List[Dict[str, str]]] = None) -> List[Dict]:
        """列表查询"""
        search_dict = search.__dict__ if search else None
        obj_list = await DemoCRUD(auth).get_list_crud(search=search_dict, order_by=order_by)
        return [DemoOutSchema.model_validate(obj).model_dump() for obj in obj_list]
    
    @classmethod
    async def create_demo_service(cls, auth: AuthSchema, data: DemoCreateSchema) -> Dict:
        """创建"""
        obj = await DemoCRUD(auth).get(name=data.name)
        if obj:
            raise CustomException(msg='创建失败，名称已存在')
        obj = await DemoCRUD(auth).create_crud(data=data)
        return DemoOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def update_demo_service(cls, auth: AuthSchema, id: int, data: DemoUpdateSchema) -> Dict:
        """更新"""
        # 检查数据是否存在
        obj = await DemoCRUD(auth).get_by_id_crud(id=id)
        if not obj:
            raise CustomException(msg='更新失败，该数据不存在')
        
        # 检查名称是否重复
        exist_obj = await DemoCRUD(auth).get(name=data.name)
        if exist_obj and exist_obj.id != id:
            raise CustomException(msg='更新失败，名称重复')
            
        obj = await DemoCRUD(auth).update_crud(id=id, data=data)
        return DemoOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def delete_demo_service(cls, auth: AuthSchema, ids: List[int]) -> None:
        """删除"""
        if len(ids) < 1:
            raise CustomException(msg='删除失败，删除对象不能为空')
        
        # 检查所有要删除的数据是否存在
        for id in ids:
            obj = await DemoCRUD(auth).get_by_id_crud(id=id)
            if not obj:
                raise CustomException(msg=f'删除失败，ID为{id}的数据不存在')
                
        await DemoCRUD(auth).delete_crud(ids=ids)
    
    @classmethod
    async def set_demo_available_service(cls, auth: AuthSchema, data: BatchSetAvailable) -> None:
        """批量设置状态"""
        await DemoCRUD(auth).set_available_crud(ids=data.ids, status=data.status)
    
    @classmethod
    async def batch_export_service(cls, obj_list: List[Dict[str, Any]]) -> bytes:
        """批量导出"""
        mapping_dict = {
            'id': '编号',
            'name': '名称', 
            'status': '状态',
            'description': '备注',
            'created_at': '创建时间',
            'updated_at': '更新时间',
            'creator': '创建者',
        }

        # 复制数据并转换状态
        data = obj_list.copy()
        for item in data:
            # 处理状态
            item['status'] = '正常' if item.get('status') else '停用'
            # 处理创建者
            creator_info = item.get('creator')
            if isinstance(creator_info, dict):
                item['creator'] = creator_info.get('name', '未知')
            else:
                item['creator'] = '未知'

        return ExcelUtil.export_list2excel(list_data=data, mapping_dict=mapping_dict)

    @classmethod
    async def batch_import_service(cls, auth: AuthSchema, file: UploadFile, update_support: bool = False) -> str:
        """批量导入"""
        
        header_dict = {
            '名称': 'name',
            '状态': 'status',
            '描述': 'description'
        }

        try:
            # 读取Excel文件
            contents = await file.read()
            df = pd.read_excel(io.BytesIO(contents))
            await file.close()
            
            if df.empty:
                raise CustomException(msg="导入文件为空")
            
            # 检查表头是否完整
            missing_headers = [header for header in header_dict.keys() if header not in df.columns]
            if missing_headers:
                raise CustomException(msg=f"导入文件缺少必要的列: {', '.join(missing_headers)}")
            
            # 重命名列名
            df.rename(columns=header_dict, inplace=True)
            
            # 验证必填字段
            required_fields = ['name', 'status']
            for field in required_fields:
                if df[field].isnull().any():  # type: ignore
                    missing_rows = df[df[field].isnull()].index.tolist()  # type: ignore
                    row_numbers = [str(int(i)+2) for i in missing_rows]  # +2 because index starts at 0 and first row is header
                    raise CustomException(msg=f"{[k for k,v in header_dict.items() if v == field][0]}不能为空，第{', '.join(row_numbers)}行")
            
            error_msgs = []
            success_count = 0
            
            # 处理每一行数据
            for index, row in df.iterrows():
                try:
                    # 数据转换前的类型检查
                    try:
                        name = str(row['name'])
                    except ValueError:
                        error_msgs.append(f"第{int(index)+2}行: 名称必须是字符串")
                        continue
                    
                    # 处理状态字段
                    status_value = row['status']
                    if isinstance(status_value, str):
                        status = status_value == '正常'
                    else:
                        status = bool(status_value)
                    
                    # 构建数据
                    data = {
                        "name": name,
                        "status": status,
                        "description": str(row['description']).strip() if not pd.isna(row['description']) else None,
                    }

                    # 处理导入逻辑
                    exists_obj = await DemoCRUD(auth).get(name=data["name"])
                    if exists_obj:
                        if update_support:
                            await DemoCRUD(auth).update_crud(id=exists_obj.id, data=DemoUpdateSchema(**data))
                            success_count += 1
                        else:
                            error_msgs.append(f"第{int(index)+2}行: 名称 {data['name']} 已存在")
                    else:
                        await DemoCRUD(auth).create_crud(data=DemoCreateSchema(**data))
                        success_count += 1
                        
                except Exception as e:
                    error_msgs.append(f"第{int(index)+2}行: {str(e)}")
                    continue

            # 返回详细的导入结果
            result = f"成功导入 {success_count} 条数据"
            if error_msgs:
                result += "\n错误信息:\n" + "\n".join(error_msgs)
            return result
            
        except Exception as e:
            logger.error(f"批量导入失败: {str(e)}")
            raise CustomException(msg=f"导入失败: {str(e)}")

    @classmethod
    async def import_template_download_service(cls) -> bytes:
        """下载导入模板"""
        header_list = ['名称', '状态', '描述']
        selector_header_list = ['状态'] 
        option_list = [{'状态': ['正常', '停用']}]
        return ExcelUtil.get_excel_template(
            header_list=header_list,
            selector_header_list=selector_header_list,
            option_list=option_list
        )