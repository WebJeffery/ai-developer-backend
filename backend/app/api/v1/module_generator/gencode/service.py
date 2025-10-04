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
from .schema import GenTableSchema, GenTableOutSchema, GenTableOutSchema, GenTableDeleteSchema, GenTableColumnSchema,  GenTableColumnOutSchema, GenTableColumnDeleteSchema
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
        return [GenTableOutSchema(**gen_table) for gen_table in CamelCaseUtil.transform_result(gen_db_table_list_result)]

    @classmethod
    async def import_gen_table_service(
        cls, auth: AuthSchema, gen_table_list: List[GenTableOutSchema]
    )  -> Literal[True] | None:
        """导入表结构"""
        try:
            for table in gen_table_list:
                table_name = table.table_name
                GenUtils.init_table(table)
                add_gen_table = await GenTableCRUD(auth).add_gen_table(table)
                if add_gen_table:
                    table.table_id = add_gen_table.id
                    gen_table_columns = await GenTableColumnCRUD(auth).get_gen_db_table_columns_by_name(table_name)
                    for column in [
                        GenTableColumnSchema(**gen_table_column)
                        for gen_table_column in CamelCaseUtil.transform_result(gen_table_columns)
                    ]:
                        GenUtils.init_column_field(column, table)
                        await GenTableColumnCRUD(auth).create_gen_table_column_crud(column)
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
                table_names.append(sql_statement.find(Table).name)
        return table_names

    @classmethod
    async def update_gen_table_service(cls, auth: AuthSchema, data: GenTableSchema, table_id: int) -> Dict[str, Any]:
        """编辑业务表信息"""        
        edit_gen_table = data.model_dump(exclude_unset=True, by_alias=True)
        gen_table_info = await cls.get_gen_table_by_id_service(auth, table_id)
        if gen_table_info.id:
            try:
                edit_gen_table['options'] = json.dumps(edit_gen_table.get('params'))
                result = await GenTableCRUD(auth).edit_gen_table(table_id, edit_gen_table)
                for gen_table_column in data.columns:
                    await GenTableColumnCRUD(auth).update_gen_table_column_crud(table_id, gen_table_column)
                return result.model_dump()
            except Exception as e:
                raise CustomException(msg=f'更新失败: {str(e)}')
        else:
            raise CustomException(msg='业务表不存在')

    @classmethod
    async def delete_gen_table_service(cls, auth: AuthSchema, data: GenTableDeleteSchema) -> None:
        """删除业务表信息"""
        try:
            await GenTableCRUD(auth=auth).delete_gen_table(data)
            await GenTableColumnCRUD(auth=auth).delete_gen_table_column_by_table_id_dao(data)
        except Exception as e:
            raise CustomException(msg=f'删除失败: {str(e)}')

    @classmethod
    async def get_gen_table_by_id_service(cls, auth: AuthSchema, table_id: int) -> GenTableOutSchema:
        """获取需要生成的业务表详细信息"""
        gen_table = await GenTableCRUD(auth=auth).get_gen_table_by_id(table_id)
        if gen_table:
            result = await cls.set_table_from_options(GenTableOutSchema(**CamelCaseUtil.transform_result(gen_table)))
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
        template_list = Jinja2TemplateUtil.get_template_list(gen_table.tpl_category, gen_table.tpl_web_type)
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
        table_columns = table.columns
        table_column_map = {column.column_name: column for column in table_columns}
        query_db_table_columns = await GenTableColumnCRUD(auth).get_gen_db_table_columns_by_name(table_name)
        db_table_columns = [
            GenTableColumnOutSchema(**column) for column in CamelCaseUtil.transform_result(query_db_table_columns)
        ]
        if not db_table_columns:
            raise CustomException(msg='同步数据失败，原表结构不存在')
        db_table_column_names = [column.column_name for column in db_table_columns]
        try:
            for column in db_table_columns:
                GenUtils.init_column_field(column, table)
                if column.column_name in table_column_map:
                    prev_column = table_column_map[column.column_name]
                    column.id = prev_column.id
                    if column.list:
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
                    await GenTableColumnCRUD(auth).update_gen_table_column_crud(column.id,column)
                else:
                    await GenTableColumnCRUD(auth).create_gen_table_column_crud(column)
            del_columns = [column for column in table_columns if column.column_name not in db_table_column_names]
            if del_columns:
                for column in del_columns:
                    await GenTableColumnCRUD(auth).delete_gen_table_column_by_column_id_dao(column.id)
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
        params_obj = json.loads(gen_table.options) if gen_table.options else None
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
            
            params_obj = json.loads(edit_gen_table.options)

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
        gen_table_schema = GenTableOutSchema(**CamelCaseUtil.transform_result(gen_table))
        await cls.set_sub_table(auth, gen_table_schema)
        await cls.set_pk_column(gen_table_schema)
        context = Jinja2TemplateUtil.prepare_context(gen_table_schema)
        template_list = Jinja2TemplateUtil.get_template_list(
            gen_table_schema.tpl_category or "", 
            gen_table_schema.tpl_web_type or ""
        )
        output_files = [Jinja2TemplateUtil.get_file_name([template], gen_table_schema)[0] for template in template_list]

        return [template_list, output_files, context, gen_table_schema]
        

    @classmethod
    def __get_gen_path(cls, gen_table: GenTableOutSchema, template: str) -> Optional[str]:
        """根据GenTableModel对象和模板名称生成路径"""
        try:
            gen_path = gen_table.gen_path or ""
            if gen_path == '/':
                file_name = Jinja2TemplateUtil.get_file_name([template], gen_table)[0]
                return os.path.join(os.getcwd(), GEN_PATH, file_name)
            else:
                file_name = Jinja2TemplateUtil.get_file_name([template], gen_table)[0]
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