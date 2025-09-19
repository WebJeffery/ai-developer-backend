# -*- coding:utf-8 -*-

import io
import json
import os
import zipfile
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, List, Dict, Optional, Sequence

from app.config.setting import settings
from app.core.exceptions import CustomException
from app.utils.common_util import CamelCaseUtil
from app.utils.gen_util import GenUtils
from app.utils.template_util import TemplateInitializer, TemplateUtils
from app.common.constant import GenConstant
from app.common.response import SuccessResponse
from app.api.v1.module_system.user.schema import UserOutSchema
from .schema import (
    DeleteGenTableSchema,
    EditGenTableSchema,
    GenTableColumnSchema,
    GenTableSchema,
)
from .param import GenTableQueryParam
from .crud import GenTableColumnDao, GenTableDao
from .model import GenTableModel, GenTableColumnModel
from app.api.v1.module_system.auth.schema import AuthSchema


# 定义默认的GenConfig值
GEN_PATH = "generated_code"  # 默认生成路径


class GenTableService:
    """
    代码生成业务表服务层
    """

    @classmethod
    async def get_gen_table_list_services(
        cls, auth: AuthSchema, query_object: GenTableQueryParam, is_page: bool = False
    ):
        """
        获取代码生成业务表列表信息service

        :param auth: 认证信息
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 代码生成业务列表信息对象
        """
        # 确保db是AsyncSession类型
        if not isinstance(auth.db, AsyncSession):
            raise CustomException(msg='数据库会话类型不正确')
            
        gen_table_dao = GenTableDao(auth=auth)
        gen_table_list_result = await gen_table_dao.get_gen_table_list(auth.db, query_object, is_page)

        return gen_table_list_result

    @classmethod
    async def get_gen_db_table_list_services(
        cls, auth: AuthSchema, query_object: GenTableQueryParam, is_page: bool = False
    ):
        """
        获取数据库列表信息service

        :param auth: 认证信息
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 数据库列表信息对象
        """
        # 确保db是AsyncSession类型
        if not isinstance(auth.db, AsyncSession):
            raise CustomException(msg='数据库会话类型不正确')
            
        gen_table_dao = GenTableDao(auth=auth)
        gen_db_table_list_result = await gen_table_dao.get_gen_db_table_list(auth.db, query_object, is_page)

        return gen_db_table_list_result

    @classmethod
    async def get_gen_db_table_list_by_name_services(cls, auth: AuthSchema, table_names: List[str]) -> list[GenTableSchema]:
        """
        根据表名称组获取数据库列表信息service

        :param auth: 认证信息
        :param table_names: 表名称组
        :return: 数据库列表信息对象
        """
        # 确保db是AsyncSession类型
        if not isinstance(auth.db, AsyncSession):
            raise CustomException(msg='数据库会话类型不正确')
            
        gen_table_dao = GenTableDao(auth=auth)
        gen_db_table_list_result = await gen_table_dao.get_gen_db_table_list_by_names(auth.db, table_names)

        return [GenTableSchema(**gen_table) for gen_table in CamelCaseUtil.transform_result(gen_db_table_list_result)]

    @classmethod
    async def import_gen_table_services(
        cls, auth: AuthSchema, gen_table_list: List[GenTableSchema], current_user: UserOutSchema
    ):
        """
        导入表结构service

        :param auth: 认证信息
        :param gen_table_list: 导入表列表
        :param current_user: 当前用户信息对象
        :return: 导入结果
        """
        try:
            # 确保db是AsyncSession类型
            if not isinstance(auth.db, AsyncSession):
                raise CustomException(msg='数据库会话类型不正确')
                
            gen_table_dao = GenTableDao(auth=auth)
            gen_table_column_dao = GenTableColumnDao(auth=auth)
            
            for table in gen_table_list:
                table_name = table.table_name
                GenUtils.init_table(table, current_user.username)  # 使用username而不是user.user_name
                add_gen_table = await gen_table_dao.create(data=table.model_dump())
                if add_gen_table:
                    table.table_id = add_gen_table.table_id
                    gen_table_columns = await gen_table_column_dao.get_gen_db_table_columns_by_name(auth.db, table_name or "")
                    for column in [
                        GenTableColumnSchema(**gen_table_column)
                        for gen_table_column in CamelCaseUtil.transform_result(gen_table_columns)
                    ]:
                        GenUtils.init_column_field(column, table)
                        await gen_table_column_dao.create(data=column.model_dump())
            if isinstance(auth.db, AsyncSession):
                await auth.db.commit()
            return SuccessResponse(msg='导入成功')
        except Exception as e:
            if isinstance(auth.db, AsyncSession):
                try:
                    await auth.db.rollback()
                except:
                    pass  # 忽略回滚错误
            raise CustomException(msg=f'导入失败, {str(e)}')

    @classmethod
    async def edit_gen_table_services(cls, auth: AuthSchema, page_object: EditGenTableSchema) -> Dict[str, Any]:
        """
        编辑业务表信息service

        :param auth: 认证信息
        :param page_object: 编辑业务表对象
        :return: 编辑业务表校验结果
        """
        # 确保db是AsyncSession类型
        if not isinstance(auth.db, AsyncSession):
            raise CustomException(msg='数据库会话类型不正确')
            
        gen_table_dao = GenTableDao(auth=auth)
        gen_table_column_dao = GenTableColumnDao(auth=auth)
        
        # 检查必要字段是否存在
        if page_object.table_id is None:
            raise CustomException(msg='业务表ID不能为空')
            
        edit_gen_table = page_object.model_dump(exclude_unset=True, by_alias=True)
        gen_table_info = await cls.get_gen_table_by_id_services(auth, page_object.table_id)
        if gen_table_info.table_id:
            try:
                # 处理params字段，确保不为None
                params = edit_gen_table.get('params')
                if params is not None:
                    edit_gen_table['options'] = json.dumps(params)
                else:
                    edit_gen_table['options'] = '{}'  # 默认空对象
                
                # 移除params字段，因为options字段已经包含了序列化的params
                edit_gen_table.pop('params', None)
                
                await gen_table_dao.update(id=page_object.table_id, data=edit_gen_table)
                if page_object.columns:
                    for gen_table_column in page_object.columns:
                        gen_table_column.update_by = page_object.update_by
                        gen_table_column.update_time = datetime.now()
                        if gen_table_column.column_id is not None:
                            await gen_table_column_dao.update(
                                id=gen_table_column.column_id, 
                                data=gen_table_column.model_dump(by_alias=True)
                            )
                if isinstance(auth.db, AsyncSession):
                    await auth.db.commit()
                return {"is_success": True, "message": "更新成功"}
            except Exception as e:
                if isinstance(auth.db, AsyncSession):
                    try:
                        await auth.db.rollback()
                    except:
                        pass  # 忽略回滚错误
                raise CustomException(msg=f'更新失败: {str(e)}')
        else:
            raise CustomException(msg='业务表不存在')

    @classmethod
    async def delete_gen_table_services(cls, auth: AuthSchema, page_object: DeleteGenTableSchema) -> SuccessResponse:
        """
        删除业务表信息service

        :param auth: 认证信息
        :param page_object: 删除业务表对象
        :return: 删除业务表校验结果
        """
        # 确保db是AsyncSession类型
        if not isinstance(auth.db, AsyncSession):
            raise CustomException(msg='数据库会话类型不正确')
            
        gen_table_dao = GenTableDao(auth=auth)
        gen_table_column_dao = GenTableColumnDao(auth=auth)
        
        if page_object.table_ids:
            table_id_list = page_object.table_ids.split(',')
            try:
                for table_id in table_id_list:
                    await gen_table_dao.delete(ids=[int(table_id)])
                    # 删除相关的字段信息
                    # 这里需要先查询出所有相关的column_id，然后删除
                    columns = await gen_table_column_dao.get_gen_table_column_list_by_table_id(auth.db, int(table_id))
                    if columns:
                        column_ids = [column.column_id for column in columns]
                        await gen_table_column_dao.delete(ids=column_ids)
                if isinstance(auth.db, AsyncSession):
                    await auth.db.commit()
                return SuccessResponse(msg='删除成功')
            except Exception as e:
                if isinstance(auth.db, AsyncSession):
                    try:
                        await auth.db.rollback()
                    except:
                        pass  # 忽略回滚错误
                raise CustomException(msg=f'删除失败: {str(e)}')
        else:
            raise CustomException(msg='传入业务表id为空')

    @classmethod
    async def get_gen_table_by_id_services(cls, auth: AuthSchema, table_id: int) -> GenTableSchema:
        """
        获取需要生成的业务表详细信息service

        :param auth: 认证信息
        :param table_id: 需要生成的业务表id
        :return: 需要生成的业务表id对应的信息
        """
        # 确保db是AsyncSession类型
        if not isinstance(auth.db, AsyncSession):
            raise CustomException(msg='数据库会话类型不正确')
            
        gen_table_dao = GenTableDao(auth=auth)
        gen_table = await gen_table_dao.get_gen_table_by_id(auth.db, table_id)
        if gen_table:
            result = await cls.set_table_from_options(GenTableSchema(**CamelCaseUtil.transform_result(gen_table)))
            return result
        else:
            raise CustomException(msg='业务表不存在')

    @classmethod
    async def get_gen_table_all_services(cls, auth: AuthSchema) -> list[GenTableSchema]:
        """
        获取所有业务表信息service

        :param auth: 认证信息
        :return: 所有业务表信息
        """
        # 确保db是AsyncSession类型
        if not isinstance(auth.db, AsyncSession):
            raise CustomException(msg='数据库会话类型不正确')
            
        gen_table_dao = GenTableDao(auth=auth)
        gen_table_all = await gen_table_dao.get_gen_table_all(auth.db)
        result = [GenTableSchema(**gen_table) for gen_table in CamelCaseUtil.transform_result(gen_table_all)]

        return result

    @classmethod
    async def create_table_services(cls, auth: AuthSchema, sql: str, current_user: UserOutSchema) -> SuccessResponse:
        """
        创建表结构service

        :param auth: 认证信息
        :param sql: 建表语句
        :param current_user: 当前用户信息对象
        :return: 创建表结构结果
        """
        # 移除sqlglot相关代码，因为导入失败
        raise CustomException(msg='建表功能暂不可用')

    @classmethod
    async def preview_code_services(cls, auth: AuthSchema, table_id: int) -> dict[Any, Any]:
        """
        预览代码service

        :param auth: 认证信息
        :param table_id: 业务表id
        :return: 预览数据列表
        """
        gen_table = await cls.get_gen_table_by_id_services(auth, table_id)
        await cls.set_sub_table(auth, gen_table)
        await cls._set_pk_column(gen_table)
        env = TemplateInitializer.init_jinja2()
        context = TemplateUtils.prepare_context(gen_table)
        template_list = TemplateUtils.get_template_list(
            gen_table.tpl_category or "", 
            gen_table.tpl_web_type or ""
        )
        preview_code_result = {}
        for template in template_list:
            render_content = env.get_template(template).render(**context)
            preview_code_result[template] = render_content
        return preview_code_result

    @classmethod
    async def generate_code_services(cls, auth: AuthSchema, table_name: str) -> SuccessResponse:
        """
        生成代码至指定路径service

        :param auth: 认证信息
        :param table_name: 业务表名称
        :return: 生成代码结果
        """
        env = TemplateInitializer.init_jinja2()
        render_info = await cls.__get_gen_render_info(auth, table_name)
        for template in render_info[0]:
            try:
                render_content = env.get_template(template).render(**render_info[2])
                gen_path = cls.__get_gen_path(render_info[3], template)
                if gen_path:
                    os.makedirs(os.path.dirname(gen_path), exist_ok=True)
                    with open(gen_path, 'w', encoding='utf-8') as f:
                        f.write(render_content)
            except Exception as e:
                raise CustomException(msg=f'渲染模板失败，表名：{render_info[3].table_name}，详细错误信息：{str(e)}')

        return SuccessResponse(msg='生成代码成功')

    @classmethod
    async def batch_gen_code_services(cls, auth: AuthSchema, table_names: List[str]) -> bytes:
        """
        批量生成代码service

        :param auth: 认证信息
        :param table_names: 业务表名称组
        :return: 下载代码结果
        """
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for table_name in table_names:
                env = TemplateInitializer.init_jinja2()
                render_info = await cls.__get_gen_render_info(auth, table_name)
                for template_file, output_file in zip(render_info[0], render_info[1]):
                    render_content = env.get_template(template_file).render(**render_info[2])
                    zip_file.writestr(output_file, render_content)

        zip_data = zip_buffer.getvalue()
        zip_buffer.close()
        return zip_data

    @classmethod
    async def __get_gen_render_info(cls, auth: AuthSchema, table_name: str) -> list[Any]:
        """
        获取生成代码渲染模板相关信息

        :param auth: 认证信息
        :param table_name: 业务表名称
        :return: 生成代码渲染模板相关信息
        """
        # 确保db是AsyncSession类型
        if not isinstance(auth.db, AsyncSession):
            raise CustomException(msg='数据库会话类型不正确')
            
        gen_table_dao = GenTableDao(auth=auth)
        gen_table = await gen_table_dao.get_gen_table_by_name(auth.db, table_name)
        if gen_table:
            gen_table_schema = GenTableSchema(**CamelCaseUtil.transform_result(gen_table))
            await cls.set_sub_table(auth, gen_table_schema)
            await cls._set_pk_column(gen_table_schema)
            context = TemplateUtils.prepare_context(gen_table_schema)
            template_list = TemplateUtils.get_template_list(
                gen_table_schema.tpl_category or "", 
                gen_table_schema.tpl_web_type or ""
            )
            output_files = [TemplateUtils.get_file_name([template], gen_table_schema)[0] for template in template_list]

            return [template_list, output_files, context, gen_table_schema]
        else:
            raise CustomException(msg=f'业务表 {table_name} 不存在')

    @classmethod
    def __get_gen_path(cls, gen_table: GenTableSchema, template: str) -> Optional[str]:
        """
        根据GenTableModel对象和模板名称生成路径

        :param gen_table: GenTableModel对象
        :param template: 模板名称
        :return: 生成的路径
        """
        try:
            gen_path = gen_table.gen_path or ""
            if gen_path == '/':
                file_name = TemplateUtils.get_file_name([template], gen_table)[0]
                return os.path.join(os.getcwd(), GEN_PATH, file_name)
            else:
                file_name = TemplateUtils.get_file_name([template], gen_table)[0]
                return os.path.join(gen_path, file_name)
        except Exception:
            return None

    @classmethod
    async def sync_db_services(cls, auth: AuthSchema, table_name: str) -> SuccessResponse:
        """
        同步数据库service

        :param auth: 认证信息
        :param table_name: 业务表名称
        :return: 同步数据库结果
        """
        # 确保db是AsyncSession类型
        if not isinstance(auth.db, AsyncSession):
            raise CustomException(msg='数据库会话类型不正确')
            
        gen_table_dao = GenTableDao(auth=auth)
        gen_table_column_dao = GenTableColumnDao(auth=auth)
        
        gen_table = await gen_table_dao.get_gen_table_by_name(auth.db, table_name)
        if gen_table:
            table = GenTableSchema(**CamelCaseUtil.transform_result(gen_table))
            table_columns = table.columns or []  # 确保不为None
            table_column_map = {column.column_name: column for column in table_columns}
            query_db_table_columns = await gen_table_column_dao.get_gen_db_table_columns_by_name(auth.db, table_name)
            db_table_columns = [
                GenTableColumnSchema(**column) for column in CamelCaseUtil.transform_result(query_db_table_columns)
            ]
            if not db_table_columns:
                raise CustomException('同步数据失败，原表结构不存在')
            db_table_column_names = [column.column_name for column in db_table_columns]
            try:
                for column in db_table_columns:
                    GenUtils.init_column_field(column, table)
                    if column.column_name in table_column_map:
                        prev_column = table_column_map[column.column_name]
                        column.column_id = prev_column.column_id
                        if getattr(column, 'list', False):  # 使用getattr安全访问属性
                            column.dict_type = prev_column.dict_type
                            column.query_type = prev_column.query_type
                        if (
                            prev_column.is_required != ''
                            and not column.pk
                            and (column.insert or column.edit)
                            and (column.usable_column or column.super_column)
                        ):
                            column.is_required = prev_column.is_required
                            column.html_type = prev_column.html_type
                        if column.column_id is not None:
                            await gen_table_column_dao.update(id=column.column_id, data=column.model_dump(by_alias=True))
                    else:
                        await gen_table_column_dao.create(data=column.model_dump(by_alias=True))
                del_columns = [column for column in table_columns if column.column_name not in db_table_column_names]
                if del_columns:
                    for column in del_columns:
                        if column.column_id is not None:
                            await gen_table_column_dao.delete(ids=[column.column_id])
                if isinstance(auth.db, AsyncSession):
                    await auth.db.commit()
                return SuccessResponse(msg='同步成功')
            except Exception as e:
                if isinstance(auth.db, AsyncSession):
                    try:
                        await auth.db.rollback()
                    except:
                        pass  # 忽略回滚错误
                raise CustomException(msg=f'同步失败: {str(e)}')
        else:
            raise CustomException('业务表不存在')

    @classmethod
    async def set_sub_table(cls, auth: AuthSchema, gen_table: GenTableSchema) -> None:
        """
        设置主子表信息

        :param auth: 认证信息
        :param gen_table: 业务表信息
        :return:
        """
        # 确保db是AsyncSession类型
        if not isinstance(auth.db, AsyncSession):
            raise CustomException(msg='数据库会话类型不正确')
            
        if gen_table.sub_table_name:
            gen_table_dao = GenTableDao(auth=auth)
            sub_table = await gen_table_dao.get_gen_table_by_name(auth.db, gen_table.sub_table_name)
            if sub_table:
                gen_table.sub_table = GenTableSchema(**CamelCaseUtil.transform_result(sub_table))

    @classmethod
    async def _set_pk_column(cls, gen_table: GenTableSchema) -> None:
        """
        设置主键列信息

        :param gen_table: 业务表信息
        :return:
        """
        if gen_table.columns:
            for column in gen_table.columns:
                if column.pk:
                    gen_table.pk_column = column
                    break
        if gen_table.pk_column is None and gen_table.columns:
            gen_table.pk_column = gen_table.columns[0]
        if gen_table.tpl_category == GenConstant.TPL_SUB and gen_table.sub_table:
            if gen_table.sub_table.columns:
                for column in gen_table.sub_table.columns:
                    if column.pk:
                        gen_table.sub_table.pk_column = column
                        break
            if gen_table.sub_table.pk_column is None and gen_table.sub_table.columns:
                gen_table.sub_table.pk_column = gen_table.sub_table.columns[0]

    @classmethod
    async def set_table_from_options(cls, gen_table: GenTableSchema) -> GenTableSchema:
        """
        设置代码生成其他选项值

        :param gen_table: 生成对象
        :return: 设置后的生成对象
        """
        params_obj = json.loads(gen_table.options) if gen_table.options else None
        if params_obj:
            gen_table.tree_code = params_obj.get(GenConstant.TREE_CODE)
            gen_table.tree_parent_code = params_obj.get(GenConstant.TREE_PARENT_CODE)
            gen_table.tree_name = params_obj.get(GenConstant.TREE_NAME)
            gen_table.parent_menu_id = params_obj.get(GenConstant.PARENT_MENU_ID)
            gen_table.parent_menu_name = params_obj.get(GenConstant.PARENT_MENU_NAME)

        return gen_table

    @classmethod
    async def validate_edit(cls, edit_gen_table: EditGenTableSchema):
        """
        编辑保存参数校验

        :param edit_gen_table: 编辑业务表对象
        """
        if edit_gen_table.tpl_category == GenConstant.TPL_TREE:
            # 检查params是否为None
            if edit_gen_table.params is None:
                raise CustomException(msg='树表参数不能为空')
            
            params_obj = edit_gen_table.params.model_dump(by_alias=True)

            if GenConstant.TREE_CODE not in params_obj:
                raise CustomException(msg='树编码字段不能为空')
            elif GenConstant.TREE_PARENT_CODE not in params_obj:
                raise CustomException(msg='树父编码字段不能为空')
            elif GenConstant.TREE_NAME not in params_obj:
                raise CustomException(msg='树名称字段不能为空')
        elif edit_gen_table.tpl_category == GenConstant.TPL_SUB:
            if not edit_gen_table.sub_table_name:
                raise CustomException(msg='关联子表的表名不能为空')
            elif not edit_gen_table.sub_table_fk_name:
                raise CustomException(msg='子表关联的外键名不能为空')


class GenTableColumnService:
    """
    代码生成业务表字段服务层
    """

    @classmethod
    async def get_gen_table_column_list_by_table_id_services(cls, auth: AuthSchema, table_id: int):
        """
        获取业务表字段列表信息service

        :param auth: 认证信息
        :param table_id: 业务表格id
        :return: 业务表字段列表信息对象
        """
        # 确保db是AsyncSession类型
        if not isinstance(auth.db, AsyncSession):
            raise CustomException(msg='数据库会话类型不正确')
            
        gen_table_column_dao = GenTableColumnDao(auth=auth)
        gen_table_column_list_result = await gen_table_column_dao.get_gen_table_column_list_by_table_id(auth.db, table_id)

        return [
            GenTableColumnSchema(**gen_table_column)
            for gen_table_column in CamelCaseUtil.transform_result(gen_table_column_list_result)
        ]