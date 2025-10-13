# -*- coding:utf-8 -*-

import io
import json
import os
import zipfile
from typing import Any, List, Dict, Literal, Optional
from sqlglot.expressions import Add, Alter, Create, Delete, Drop, Expression, Insert, Table, TruncateTable, Update
from sqlglot import parse as sqlglot_parse

from app.config.setting import settings
from app.core.exceptions import CustomException
from app.common.constant import GenConstant
from app.common.response import SuccessResponse
from app.api.v1.module_system.auth.schema import AuthSchema
from app.utils.common_util import CamelCaseUtil
from app.utils.gen_util import GenUtils
from app.utils.jinja2_template_util import Jinja2TemplateInitializerUtil, Jinja2TemplateUtil
from .schema import GenTableSchema, GenTableOutSchema, GenTableOutSchema, GenTableColumnSchema,  GenTableColumnOutSchema, GenTableColumnDeleteSchema
from .param import GenTableQueryParam
from .crud import GenTableColumnCRUD, GenTableCRUD


# 定义默认的GenConfig值
GEN_PATH = "generated_code"  # 默认生成路径


class GenTableService:
    """代码生成业务表服务层"""

    @classmethod
    async def get_gen_table_detail_service(cls, auth: AuthSchema, table_id: int) -> Dict:
        """获取业务表详细信息"""
        gen_table = await cls.get_gen_table_by_id_service(auth, table_id)
        gen_tables = await cls.get_gen_table_all_service(auth)
        gen_columns = await GenTableColumnService.get_gen_table_column_list_by_table_id_service(auth, table_id)
        return dict(info=gen_table, rows=gen_columns, tables=gen_tables)

    @classmethod
    async def get_gen_table_list_service(
        cls, auth: AuthSchema, search: GenTableQueryParam
    ) -> List[Dict]:
        """获取代码生成业务表列表信息"""
        gen_table_list_result = await GenTableCRUD(auth=auth).get_gen_table_list(search)
        return [GenTableOutSchema.model_validate(obj).model_dump() for obj in gen_table_list_result]

    @classmethod
    async def get_gen_db_table_list_service(cls, auth: AuthSchema, search: GenTableQueryParam, order_by: Optional[List[Dict[str, str]]] = None) -> list[Any]:
        """获取数据库列表信息"""
        # 确保db是AsyncSession类型
        gen_db_table_list_result = await GenTableCRUD(auth=auth).get_db_table_list(search)
        return gen_db_table_list_result

    @classmethod
    async def get_gen_db_table_list_by_name_service(cls, auth: AuthSchema, table_names: List[str]) -> List[GenTableOutSchema]:
        """根据表名称组获取数据库列表信息"""
        gen_db_table_list_result = await GenTableCRUD(auth=auth).get_db_table_list_by_names(table_names)
        # 修复：将GenDBTableSchema对象转换为字典后再传递给GenTableOutSchema
        result = []
        for gen_table in CamelCaseUtil.transform_result(gen_db_table_list_result):
            # 确保gen_table是字典类型
            if hasattr(gen_table, 'model_dump'):
                gen_table_dict = gen_table.model_dump()
            elif isinstance(gen_table, dict):
                gen_table_dict = gen_table
            else:
                gen_table_dict = gen_table.__dict__
            result.append(GenTableOutSchema(**gen_table_dict))
        
        # 检查是否有未找到的表
        found_table_names = [table.table_name for table in result]
        missing_tables = [name for name in table_names if name not in found_table_names]
        if missing_tables:
            raise CustomException(msg=f"以下数据表不存在: {', '.join(missing_tables)}")
        
        return result

    @classmethod
    async def import_gen_table_service(
        cls, auth: AuthSchema, gen_table_list: List[GenTableOutSchema]
    )  -> Literal[True] | None:
        """导入表结构"""
        # 检查是否有表需要导入
        if not gen_table_list:
            raise CustomException(msg="没有可导入的表结构")
            
        # 检查表是否已存在
        existing_tables = []
        for table in gen_table_list:
            table_name = table.table_name
            # 确保table_name不为None
            if table_name is None:
                raise CustomException(msg="表名不能为空")
            # 检查表是否已存在
            existing_table = await GenTableCRUD(auth).get_gen_table_by_name(table_name)
            if existing_table:
                existing_tables.append(table_name)
                
        # 如果有已存在的表，抛出异常
        if existing_tables:
            raise CustomException(msg=f"以下表已存在，不能重复导入: {', '.join(existing_tables)}")
            
        try:
            for table in gen_table_list:
                table_name = table.table_name
                GenUtils.init_table(table)
                add_gen_table = await GenTableCRUD(auth).add_gen_table(table)
                if add_gen_table:
                    table.table_id = add_gen_table.id
                    # 获取数据库表的字段信息
                    gen_table_columns = await GenTableColumnCRUD(auth).get_gen_db_table_columns_by_name(table_name)
                    
                    # 为每个字段初始化并保存到数据库
                    for column in gen_table_columns:
                        # 将GenTableColumnOutSchema转换为GenTableColumnSchema
                        column_schema = GenTableColumnSchema(
                            table_id=table.table_id,
                            column_name=column.column_name,
                            column_comment=column.column_comment,
                            column_type=column.column_type,
                            is_pk=column.is_pk,
                            is_increment=column.is_increment,
                            is_required=column.is_required,
                            sort=column.sort
                        )
                        # 初始化字段属性
                        GenUtils.init_column_field(column_schema, table)
                        # 保存到数据库
                        await GenTableColumnCRUD(auth).create_gen_table_column_crud(column_schema)
            return True
        except Exception as e:
            raise CustomException(msg=f'导入失败, {str(e)}')

    @classmethod
    async def create_table_service(cls, auth: AuthSchema, sql: str) -> Literal[True] | None:
        """创建表结构"""
        try:
            sql_statements = sqlglot_parse(sql, dialect=settings.DATABASE_TYPE)
            # 校验sql语句是否为合法的建表语句
            if not cls.__is_valid_create_table(sql_statements):
                raise CustomException(msg='sql语句不是合法的建表语句')
            table_names = cls.__get_table_names(sql_statements)
            # 执行SQL语句创建表
            await GenTableCRUD(auth=auth).create_table_by_sql(sql_statements)
            gen_table_list = await cls.get_gen_db_table_list_by_name_service(auth, table_names)
            import_result = await cls.import_gen_table_service(auth, gen_table_list)
            return import_result
        except Exception as e:
            raise CustomException(msg=f'创建表结构失败: {str(e)}')
    
    @classmethod
    def __is_valid_create_table(cls, sql_statements: List[Expression | None]) -> bool:
        """
        校验sql语句是否为合法的建表语句

        :param sql_statements: sql语句的ast列表
        :return: 校验结果
        """
        validate_create = [isinstance(sql_statement, Create) for sql_statement in sql_statements]
        validate_forbidden_keywords = [
            isinstance(
                sql_statement,
                (Add, Alter, Delete, Drop, Insert, TruncateTable, Update),
            )
            for sql_statement in sql_statements
        ]
        if not any(validate_create) or any(validate_forbidden_keywords):
            return False
        return True
    
    @classmethod
    def __get_table_names(cls, sql_statements: List[Expression | None]) -> List[str]:
        """
        获取sql语句中所有的建表表名

        :param sql_statements: sql语句的ast列表
        :return: 建表表名列表
        """
        table_names = []
        for sql_statement in sql_statements:
            if isinstance(sql_statement, Create):
                table = sql_statement.find(Table)
                if table and table.name:
                    table_names.append(table.name)
        return table_names

    @classmethod
    async def update_gen_table_service(cls, auth: AuthSchema, data: GenTableSchema, table_id: int) -> Dict[str, Any]:
        """编辑业务表信息"""        
        edit_gen_table = data.model_dump(exclude_unset=True, by_alias=True)
        gen_table_info = await cls.get_gen_table_by_id_service(auth, table_id)
        if gen_table_info.id:
            try:
                # 处理params为None的情况
                params = edit_gen_table.get('params')
                if params:
                    edit_gen_table['options'] = json.dumps(params)
                # 将字典转换为GenTableSchema对象
                gen_table_schema = GenTableSchema(**edit_gen_table)
                result = await GenTableCRUD(auth).edit_gen_table(table_id, gen_table_schema)
                # 处理data.columns为None的情况
                if data.columns:
                    for gen_table_column in data.columns:
                        # 确保column有id字段
                        if hasattr(gen_table_column, 'id') and gen_table_column.id:
                            await GenTableColumnCRUD(auth).update_gen_table_column_crud(gen_table_column.id, gen_table_column)
                return result.model_dump()
            except Exception as e:
                raise CustomException(msg=f'更新失败: {str(e)}')
        else:
            raise CustomException(msg='业务表不存在')

    @classmethod
    async def delete_gen_table_service(cls, auth: AuthSchema, ids: List[int]) -> None:
        """删除业务表信息"""
        try:
            # 先删除相关的字段信息
            await GenTableColumnCRUD(auth=auth).delete_gen_table_column_by_table_id_dao(ids)
            # 再删除表信息
            await GenTableCRUD(auth=auth).delete_gen_table(ids)
        except Exception as e:
            raise CustomException(msg=f'删除失败: {str(e)}')

    @classmethod
    async def get_gen_table_by_id_service(cls, auth: AuthSchema, table_id: int) -> GenTableOutSchema:
        """获取需要生成的业务表详细信息"""
        gen_table = await GenTableCRUD(auth=auth).get_gen_table_by_id(table_id)
        if gen_table:
            # 使用更直接的转换方式
            result_dict = gen_table.__dict__.copy()
            result_dict.pop('_sa_instance_state', None)
            # 确保columns正确加载
            if hasattr(gen_table, 'columns') and gen_table.columns:
                columns_list = []
                for column in gen_table.columns:
                    column_dict = column.__dict__.copy()
                    column_dict.pop('_sa_instance_state', None)
                    # 处理None值，转换为空字符串或适当的默认值
                    for key, value in column_dict.items():
                        if value is None:
                            column_dict[key] = ''
                    columns_list.append(column_dict)
                result_dict['columns'] = columns_list
            else:
                result_dict['columns'] = []
            # 处理其他None值，特殊处理creator_id和creator字段
            for key, value in result_dict.items():
                if value is None:
                    # 对于creator_id和creator字段，保持为None而不是转换为空字符串
                    if key not in ['creator_id', 'creator']:
                        result_dict[key] = ''
            # 手动创建GenTableOutSchema对象
            result = GenTableOutSchema(**result_dict)
            # 设置额外选项
            result = await cls.set_table_from_options(result)
            return result
        else:
            raise CustomException(msg='业务表不存在')

    @classmethod
    async def get_gen_table_all_service(cls, auth: AuthSchema) -> List[GenTableOutSchema]:
        """获取所有业务表信息"""
        gen_table_all = await GenTableCRUD(auth=auth).get_gen_table_all()
        result = [GenTableOutSchema(**gen_table) for gen_table in CamelCaseUtil.transform_result(gen_table_all)]
        return result

    @classmethod
    async def preview_code_service(cls, auth: AuthSchema, table_id: int) -> Dict[Any, Any]:
        """
        预览代码service

        :param auth: 认证对象
        :param table_id: 业务表id
        :return: 预览数据列表
        """
        gen_table = GenTableOutSchema(
            **CamelCaseUtil.transform_result(await GenTableCRUD(auth).get_gen_table_by_id(table_id))
        )
        await cls.set_sub_table(auth, gen_table)
        await cls.set_pk_column(gen_table)
        env = Jinja2TemplateInitializerUtil.init_jinja2()
        context = Jinja2TemplateUtil.prepare_context(gen_table)
        # 处理tpl_category和tpl_web_type为None的情况
        tpl_category = gen_table.tpl_category or ''
        tpl_web_type = gen_table.tpl_web_type or ''
        template_list = Jinja2TemplateUtil.get_template_list(tpl_category, tpl_web_type)
        preview_code_result = {}
        for template in template_list:
            render_content = env.get_template(template).render(**context)
            preview_code_result[template] = render_content
        return preview_code_result


    @classmethod
    async def generate_code_service(cls, auth: AuthSchema, table_name: str) -> SuccessResponse:
        """生成代码至指定路径"""
        env = Jinja2TemplateInitializerUtil.init_jinja2()
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
    async def batch_gen_code_service(cls, auth: AuthSchema, table_names: List[str]) -> bytes:
        """
        批量生成代码service

        :param auth: 认证对象
        :param table_names: 业务表名称组
        :return: 下载代码结果
        """
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for table_name in table_names:
                env = Jinja2TemplateInitializerUtil.init_jinja2()
                render_info = await cls.__get_gen_render_info(auth, table_name)
                for template_file, output_file in zip(render_info[0], render_info[1]):
                    render_content = env.get_template(template_file).render(**render_info[2])
                    zip_file.writestr(output_file, render_content)

        zip_data = zip_buffer.getvalue()
        zip_buffer.close()
        return zip_data

    @classmethod
    async def sync_db_service(cls, auth: AuthSchema, table_name: str) -> None:
        """同步数据库"""
        gen_table = await GenTableCRUD(auth).get_gen_table_by_name(table_name)
        table = GenTableSchema(**CamelCaseUtil.transform_result(gen_table))
        # 处理table.columns为None的情况
        table_columns = table.columns or []
        table_column_map = {column.column_name: column for column in table_columns}
        query_db_table_columns = await GenTableColumnCRUD(auth).get_gen_db_table_columns_by_name(table_name)
        # 直接使用查询结果，因为get_gen_db_table_columns_by_name已经返回GenTableColumnOutSchema对象列表
        db_table_columns = query_db_table_columns
        if not db_table_columns:
            raise CustomException(msg='同步数据失败，原表结构不存在')
        db_table_column_names = [column.column_name for column in db_table_columns]
        try:
            for column in db_table_columns:
                GenUtils.init_column_field(column, table)
                if column.column_name in table_column_map:
                    prev_column = table_column_map[column.column_name]
                    # 处理column.id为None的情况
                    if hasattr(prev_column, 'id') and prev_column.id:
                        column.id = prev_column.id
                    if column.list:
                        column.dict_type = prev_column.dict_type
                        column.query_type = prev_column.query_type
                    if (
                        hasattr(prev_column, 'is_required') and prev_column.is_required != ''
                        and not column.pk
                        and (column.insert or column.edit)
                        and (column.usable_column or column.super_column)
                    ):
                        column.is_required = prev_column.is_required
                        column.html_type = prev_column.html_type
                    # 处理column.id为None的情况
                    if hasattr(column, 'id') and column.id:
                        await GenTableColumnCRUD(auth).update_gen_table_column_crud(column.id, column)
                else:
                    await GenTableColumnCRUD(auth).create_gen_table_column_crud(column)
            del_columns = [column for column in table_columns if column.column_name not in db_table_column_names]
            if del_columns:
                for column in del_columns:
                    # 处理column.id为None的情况
                    if hasattr(column, 'id') and column.id:
                        await GenTableColumnCRUD(auth).delete_gen_table_column_by_column_id_dao(
                            GenTableColumnDeleteSchema(column_ids=[column.id])
                        )
        except Exception as e:
            raise e


    @classmethod
    async def set_sub_table(cls, auth: AuthSchema, gen_table: GenTableOutSchema) -> None:
        """设置主子表信息"""
        if gen_table.sub_table_name:
            gen_table_dao = GenTableCRUD(auth=auth)
            sub_table = await gen_table_dao.get_gen_table_by_name(gen_table.sub_table_name)
            if sub_table:
                gen_table.sub_table = GenTableOutSchema(**CamelCaseUtil.transform_result(sub_table))

    @classmethod
    async def set_pk_column(cls, gen_table: GenTableOutSchema) -> None:
        """设置主键列信息"""
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
    async def set_table_from_options(cls, gen_table: GenTableOutSchema) -> GenTableOutSchema:
        """设置代码生成其他选项值"""
        # 处理gen_table.options为None的情况
        if gen_table.options:
            try:
                params_obj = json.loads(gen_table.options)
            except json.JSONDecodeError:
                params_obj = {}
        else:
            params_obj = {}
            
        if params_obj:
            gen_table.tree_code = params_obj.get(GenConstant.TREE_CODE)
            gen_table.tree_parent_code = params_obj.get(GenConstant.TREE_PARENT_CODE)
            gen_table.tree_name = params_obj.get(GenConstant.TREE_NAME)
            gen_table.parent_menu_id = params_obj.get(GenConstant.PARENT_MENU_ID)
            gen_table.parent_menu_name = params_obj.get(GenConstant.PARENT_MENU_NAME)

        return gen_table

    @classmethod
    async def validate_edit(cls, edit_gen_table: GenTableSchema) -> None:
        """编辑保存参数校验"""
        if edit_gen_table.tpl_category == GenConstant.TPL_TREE:
            # 从options字段获取参数，而不是params
            if not edit_gen_table.options:
                raise CustomException(msg='树表参数不能为空')
            
            # 处理json解析异常
            try:
                params_obj = json.loads(edit_gen_table.options)
            except json.JSONDecodeError:
                raise CustomException(msg='树表参数格式不正确')

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

    @classmethod
    async def __get_gen_render_info(cls, auth: AuthSchema, table_name: str) -> List[Any]:
        """
        获取生成代码渲染模板相关信息

        :param auth: 认证对象
        :param table_name: 业务表名称
        :return: 生成代码渲染模板相关信息
        """
        gen_table = await GenTableCRUD(auth=auth).get_gen_table_by_name(table_name)
        # 检查表是否存在
        if gen_table is None:
            raise CustomException(msg=f"业务表 {table_name} 不存在")
            
        # 确保CamelCaseUtil.transform_result返回的是字典
        transformed_result = CamelCaseUtil.transform_result(gen_table)
        if transformed_result is None:
            raise CustomException(msg=f"业务表 {table_name} 数据转换失败")
            
        gen_table_schema = GenTableOutSchema(**transformed_result)
        await cls.set_sub_table(auth, gen_table_schema)
        await cls.set_pk_column(gen_table_schema)
        context = Jinja2TemplateUtil.prepare_context(gen_table_schema)
        template_list = Jinja2TemplateUtil.get_template_list(
            gen_table_schema.tpl_category or "", 
            gen_table_schema.tpl_web_type or ""
        )
        # 修复：确保get_file_name返回的文件名不为空
        output_files = []
        for template in template_list:
            file_name = Jinja2TemplateUtil.get_file_name([template], gen_table_schema)
            if file_name:  # 只有当文件名不为空时才添加到列表中
                output_files.append(file_name)

        return [template_list, output_files, context, gen_table_schema]
        

    @classmethod
    def __get_gen_path(cls, gen_table: GenTableOutSchema, template: str) -> Optional[str]:
        """根据GenTableModel对象和模板名称生成路径"""
        try:
            gen_path = gen_table.gen_path or ""
            file_name = Jinja2TemplateUtil.get_file_name([template], gen_table)
            # 修复：检查文件名是否为空
            if not file_name:
                return None
            if gen_path == '/':
                return os.path.join(os.getcwd(), GEN_PATH, file_name)
            else:
                return os.path.join(gen_path, file_name)
        except Exception:
            return None


class GenTableColumnService:
    """代码生成业务表字段服务层"""

    @classmethod
    async def get_gen_table_column_list_by_table_id_service(cls, auth: AuthSchema, table_id: int) -> List[GenTableColumnOutSchema]:
        """获取业务表字段列表信息"""
        gen_table_column_list_result = await GenTableColumnCRUD(auth).list_gen_table_column_crud({"table_id": table_id})
        return [
            GenTableColumnOutSchema(**gen_table_column)
            for gen_table_column in CamelCaseUtil.transform_result(gen_table_column_list_result)
        ]