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
from app.utils.gen_util import GenUtils
from app.utils.jinja2_template_util import Jinja2TemplateInitializerUtil, Jinja2TemplateUtil
from .schema import GenTableOptionSchema, GenTableSchema, GenTableOutSchema, GenTableOutSchema, GenTableColumnSchema,  GenTableColumnOutSchema, GenTableColumnDeleteSchema
from .param import GenTableQueryParam
from .crud import GenTableColumnCRUD, GenTableCRUD


# 定义默认的GenConfig值
GEN_PATH = "generated_code"  # 默认生成路径


class GenTableService:
    """代码生成业务表服务层"""

    @classmethod
    async def get_gen_table_detail_service(cls, auth: AuthSchema, table_id: int) -> Dict:
        """获取业务表详细信息。

        参数:
        - auth (AuthSchema): 认证信息。
        - table_id (int): 业务表ID。

        返回:
        - Dict: 包含业务表详细信息、字段列表和所有业务表的字典。
        """
        gen_table = await cls.get_gen_table_by_id_service(auth, table_id)
        gen_tables = await cls.get_gen_table_all_service(auth)
        gen_columns = await GenTableColumnService.get_gen_table_column_list_by_table_id_service(auth, table_id)
        if gen_table.options:
            table_options = GenTableOptionSchema(**json.loads(gen_table.options))
            gen_table.parent_menu_id = table_options.parent_menu_id
        gen_table.columns = gen_columns
        return dict(info=gen_table, rows=gen_columns, tables=gen_tables)

    @classmethod
    async def get_gen_table_list_service(cls, auth: AuthSchema, search: GenTableQueryParam) -> List[Dict]:
        """
        获取代码生成业务表列表信息。

        参数:
        - auth (AuthSchema): 认证信息。
        - search (GenTableQueryParam): 查询参数模型。

        返回:
        - List[Dict]: 包含业务表列表信息的字典列表。
        """
        gen_table_list_result = await GenTableCRUD(auth=auth).get_gen_table_list(search)
        return [GenTableOutSchema.model_validate(obj).model_dump() for obj in gen_table_list_result]

    @classmethod
    async def get_gen_db_table_list_service(cls, auth: AuthSchema, search: GenTableQueryParam, order_by: Optional[List[Dict[str, str]]] = None) -> list[Any]:
        """获取数据库列表信息。

        参数:
        - auth (AuthSchema): 认证信息。
        - search (GenTableQueryParam): 查询参数模型。
        - order_by (Optional[List[Dict[str, str]]]): 排序参数列表，默认值为None。

        返回:
        - list[Any]: 包含数据库列表信息的任意类型列表。
        """
        # 确保db是AsyncSession类型
        gen_db_table_list_result = await GenTableCRUD(auth=auth).get_db_table_list(search)
        return gen_db_table_list_result

    @classmethod
    async def get_gen_db_table_list_by_name_service(cls, auth: AuthSchema, table_names: List[str]) -> List[GenTableOutSchema]:
        """根据表名称组获取数据库列表信息。

        参数:
        - auth (AuthSchema): 认证信息。
        - table_names (List[str]): 业务表名称列表。

        返回:
        - List[GenTableOutSchema]: 包含业务表列表信息的模型列表。
        """
        gen_db_table_list_result = await GenTableCRUD(auth=auth).get_db_table_list_by_names(table_names)
        
        # 检查是否有未找到的表
        found_table_names = [table.table_name for table in gen_db_table_list_result]
        missing_tables = [name for name in table_names if name not in found_table_names]
        if missing_tables:
            raise CustomException(msg=f"以下数据表不存在: {', '.join(missing_tables)}")

        # 修复：将GenDBTableSchema对象转换为字典后再传递给GenTableOutSchema
        result = []
        for gen_table in gen_db_table_list_result:
            result.append(GenTableOutSchema(**gen_table.model_dump()))
        
        return result

    @classmethod
    async def import_gen_table_service(cls, auth: AuthSchema, gen_table_list: List[GenTableOutSchema])  -> Literal[True] | None:
        """导入表结构
        
        参数:
        - auth (AuthSchema): 认证对象。
        - gen_table_list (List[GenTableOutSchema]): 要导入的业务表列表。
        
        返回:
        - Literal[True] | None: 导入成功返回True，否则返回None。
        
        异常:
        - CustomException: 当没有可导入的表结构、表已存在或导入过程中发生错误时抛出。
        """
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
        """创建表结构。

        参数:
        - auth (AuthSchema): 认证信息。
        - sql (str): 包含建表SQL语句的字符串。

        返回:
        - Literal[True] | None: 创建成功返回True，否则返回None。

        异常:
        - CustomException: 当SQL语句不是合法的建表语句、创建表失败或导入表结构失败时抛出。
        """
        try:
            sql_statements = sqlglot_parse(sql, dialect=settings.DATABASE_TYPE)
            # 校验sql语句是否为合法的建表语句
            if not cls.__is_valid_create_table(sql_statements):
                raise CustomException(msg='sql语句不是合法的建表语句')
            table_names = cls.__get_table_names(sql_statements)
            # 执行SQL语句创建表
            result = await GenTableCRUD(auth=auth).create_table_by_sql(sql)
            if not result:
                raise CustomException(msg='创建表失败，请检查SQL语句，请确保语法是否符合标准，并检查后端日志')
            gen_table_list = await cls.get_gen_db_table_list_by_name_service(auth, table_names)
            import_result = await cls.import_gen_table_service(auth, gen_table_list)
            return import_result
        except Exception as e:
            raise CustomException(msg=f'创建表结构失败: {str(e)}')
    
    @classmethod
    def __is_valid_create_table(cls, sql_statements: List[Expression | None]) -> bool:
        """
        校验SQL语句是否为合法的建表语句。
    
        参数:
        - sql_statements (List[Expression | None]): SQL的AST列表。
    
        返回:
        - bool: 校验结果。
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
        获取SQL语句中所有的建表表名。
    
        参数:
        - sql_statements (List[Expression | None]): SQL的AST列表。
    
        返回:
        - List[str]: 建表表名列表。
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
        """编辑业务表信息。

        参数:
        - auth (AuthSchema): 认证信息。
        - data (GenTableSchema): 包含业务表更新信息的模型。
        - table_id (int): 业务表ID。

        返回:
        - Dict[str, Any]: 更新后的业务表信息字典。

        异常:
        - CustomException: 当业务表不存在、更新失败或处理字段参数时抛出。
        """        
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
        """删除业务表信息。

        参数:
        - auth (AuthSchema): 认证信息。
        - ids (List[int]): 业务表ID列表。

        返回:
        - None

        异常:
        - CustomException: 当删除失败时抛出。
        """
        try:
            # 先删除相关的字段信息
            await GenTableColumnCRUD(auth=auth).delete_gen_table_column_by_table_id_dao(ids)
            # 再删除表信息
            await GenTableCRUD(auth=auth).delete_gen_table(ids)
        except Exception as e:
            raise CustomException(msg=f'删除失败: {str(e)}')

    @classmethod
    async def get_gen_table_by_id_service(cls, auth: AuthSchema, table_id: int) -> GenTableOutSchema:
        """获取需要生成代码的业务表详细信息。

        参数:
        - auth (AuthSchema): 认证信息。
        - table_id (int): 业务表ID。

        返回:
        - GenTableOutSchema: 包含业务表详细信息的模型。

        异常:
        - CustomException: 当业务表不存在时抛出。
        """
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
        """获取所有业务表信息。

        参数:
        - auth (AuthSchema): 认证信息。

        返回:
        - List[GenTableOutSchema]: 包含所有业务表详细信息的模型列表。
        """
        gen_table_all = await GenTableCRUD(auth=auth).get_gen_table_all()
        gen_table_all_dict = [GenTableOutSchema.model_validate(gen_table).model_dump() for gen_table in gen_table_all]
        result = [GenTableOutSchema(**gen_table) for gen_table in gen_table_all_dict]
        return result

    @classmethod
    async def preview_code_service(cls, auth: AuthSchema, table_id: int) -> Dict[Any, Any]:
        """
        预览代码。
    
        参数:
        - auth (AuthSchema): 认证对象。
        - table_id (int): 业务表ID。
    
        返回:
        - Dict[Any, Any]: 模版文件名到渲染内容的映射。
        """
        gen_table = GenTableOutSchema.model_validate(
            await GenTableCRUD(auth).get_gen_table_by_id(table_id)
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
            render_content = await env.get_template(template).render_async(**context)
            preview_code_result[template] = render_content
        return preview_code_result

    @classmethod
    async def generate_code_service(cls, auth: AuthSchema, table_name: str) -> SuccessResponse:
        """生成代码至指定路径。

        参数:
        - auth (AuthSchema): 认证对象。
        - table_name (str): 业务表名称。

        返回:
        - SuccessResponse: 成功响应模型。

        异常:
        - CustomException: 当渲染模板失败时抛出。
        """
        env = Jinja2TemplateInitializerUtil.init_jinja2()
        render_info = await cls.__get_gen_render_info(auth, table_name)
        gen_table_schema = render_info[3]
        skipped = 0
        for template in render_info[0]:
            try:
                render_content = await env.get_template(template).render_async(**render_info[2])
                gen_path = cls.__get_gen_path(gen_table_schema, template)
                if gen_path:
                    # 只允许写入到项目根目录及其子目录
                    project_root = os.path.realpath(str(settings.BASE_DIR.parent))
                    target_path = os.path.realpath(gen_path)
                    if not target_path.startswith(project_root):
                        raise CustomException(msg='生成路径不允许，请选择项目目录内路径')

                    os.makedirs(os.path.dirname(gen_path), exist_ok=True)

                    # 覆盖控制：存在且不允许覆盖则跳过
                    if os.path.exists(gen_path) and not settings.allow_overwrite:
                        skipped += 1
                        continue

                    with open(gen_path, 'w', encoding='utf-8') as f:
                        f.write(render_content)
            except Exception as e:
                raise CustomException(msg=f'渲染模板失败，表名：{gen_table_schema.table_name}，详细错误信息：{str(e)}')

        msg = '生成代码成功'
        if skipped:
            msg += f'（已跳过 {skipped} 个已存在文件）'
        return SuccessResponse(msg=msg)

    @classmethod
    async def batch_gen_code_service(cls, auth: AuthSchema, table_names: List[str]) -> bytes:
        """
        批量生成代码并打包为ZIP。
    
        参数:
        - auth (AuthSchema): 认证对象。
        - table_names (List[str]): 业务表名称组。
    
        返回:
        - bytes: 下载代码的ZIP二进制数据。
        """
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for table_name in table_names:
                env = Jinja2TemplateInitializerUtil.init_jinja2()
                render_info = await cls.__get_gen_render_info(auth, table_name)
                for template_file, output_file in zip(render_info[0], render_info[1]):
                    render_content = await env.get_template(template_file).render_async(**render_info[2])
                    zip_file.writestr(output_file, render_content)

        zip_data = zip_buffer.getvalue()
        zip_buffer.close()
        return zip_data

    @classmethod
    async def sync_db_service(cls, auth: AuthSchema, table_name: str) -> None:
        """同步数据库表结构。

        参数:
        - auth (AuthSchema): 认证对象。
        - table_name (str): 业务表名称。

        返回:
        - None

        异常:
        - CustomException: 当业务表不存在时抛出。
        """
        gen_table = await GenTableCRUD(auth).get_gen_table_by_name(table_name)
        if not gen_table:
            raise CustomException(msg='业务表不存在')
        table = GenTableSchema.model_validate(gen_table)
        # 关键修复：确保 table.table_id 正确设置为持久化的表ID，否则列无法关联到该表
        if getattr(table, 'table_id', None) is None:
            table.table_id = getattr(gen_table, 'id', None)
        table_columns = table.columns or []
        table_column_map = {column.column_name: column for column in table_columns}
        db_table_columns = await GenTableColumnCRUD(auth).get_gen_db_table_columns_by_name(table_name)
        db_table_column_names = [column.column_name for column in db_table_columns]
        try:
            for column in db_table_columns:
                # 仅在缺省时初始化默认属性（包含 table_id 关联）
                GenUtils.init_column_field(column, table)
                if column.column_name in table_column_map:
                    prev_column = table_column_map[column.column_name]
                    # 复用旧记录ID，确保执行更新
                    if hasattr(prev_column, 'id') and prev_column.id:
                        column.id = prev_column.id

                    # 保留用户配置的显示与查询属性
                    if getattr(prev_column, 'dict_type', None):
                        column.dict_type = prev_column.dict_type
                    if getattr(prev_column, 'query_type', None):
                        column.query_type = prev_column.query_type
                    if getattr(prev_column, 'html_type', None):
                        column.html_type = prev_column.html_type

                    # 保留 is_* 标志（旧值非空则保留），主键不设置必填
                    def keep_str(orig, current):
                        return orig if (orig is not None and orig != '') else current

                    is_pk_bool = bool(getattr(prev_column, 'pk', False)) or (prev_column.is_pk == '1')
                    if not is_pk_bool:
                        column.is_required = keep_str(prev_column.is_required, column.is_required)
                    column.is_unique = keep_str(prev_column.is_unique, column.is_unique)
                    column.is_insert = keep_str(prev_column.is_insert, column.is_insert)
                    column.is_edit = keep_str(prev_column.is_edit, column.is_edit)
                    column.is_list = keep_str(prev_column.is_list, column.is_list)
                    column.is_query = keep_str(prev_column.is_query, column.is_query)

                    if hasattr(column, 'id') and column.id:
                        await GenTableColumnCRUD(auth).update_gen_table_column_crud(column.id, column)
                    else:
                        await GenTableColumnCRUD(auth).create_gen_table_column_crud(column)
                else:
                    await GenTableColumnCRUD(auth).create_gen_table_column_crud(column)
            del_columns = [column for column in table_columns if column.column_name not in db_table_column_names]
            if del_columns:
                for column in del_columns:
                    if hasattr(column, 'id') and column.id:
                        await GenTableColumnCRUD(auth).delete_gen_table_column_by_column_id_dao(
                            GenTableColumnDeleteSchema(column_ids=[column.id])
                        )
        except Exception as e:
            raise CustomException(msg=f'同步失败: {str(e)}')

    @classmethod
    async def set_sub_table(cls, auth: AuthSchema, gen_table: GenTableOutSchema) -> None:
        """设置主子表信息。

        参数:
        - auth (AuthSchema): 认证对象。
        - gen_table (GenTableOutSchema): 业务表详细信息模型。

        返回:
        - None

        异常:
        - CustomException: 当子表不存在时抛出。
        """
        if gen_table.sub_table_name:
            gen_table_dao = GenTableCRUD(auth=auth)
            sub_table = await gen_table_dao.get_gen_table_by_name(gen_table.sub_table_name)
            if sub_table:
                gen_table.sub_table = GenTableOutSchema.model_validate(sub_table)

    @classmethod
    async def set_pk_column(cls, gen_table: GenTableOutSchema) -> None:
        """设置主键列信息。

        参数:
        - gen_table (GenTableOutSchema): 业务表详细信息模型。

        返回:
        - None
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
    async def set_table_from_options(cls, gen_table: GenTableOutSchema) -> GenTableOutSchema:
        """设置代码生成其他选项值。

        参数:
        - gen_table (GenTableOutSchema): 业务表详细信息模型。

        返回:
        - GenTableOutSchema: 更新后的业务表详细信息模型。
        """
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
        """编辑保存参数校验。

        参数:
        - edit_gen_table (GenTableSchema): 编辑后的业务表模型。

        返回:
        - None

        异常:
        - CustomException: 当参数校验失败时抛出。
        """
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
        获取生成代码渲染模板相关信息。
    
        参数:
        - auth (AuthSchema): 认证对象。
        - table_name (str): 业务表名称。
    
        返回:
        - List[Any]: [模板列表, 输出文件名列表, 渲染上下文, 业务表对象]。
    
        异常:
        - CustomException: 当业务表不存在或数据转换失败时抛出。
        """
        gen_table = await GenTableCRUD(auth=auth).get_gen_table_by_name(table_name)
        # 检查表是否存在
        if gen_table is None:
            raise CustomException(msg=f"业务表 {table_name} 不存在")
            
        # 确保CamelCaseUtil.transform_result返回的是字典
        transformed_result = gen_table
        if transformed_result is None:
            raise CustomException(msg=f"业务表 {table_name} 数据转换失败")
            
        gen_table_schema = GenTableOutSchema.model_validate(transformed_result)
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
            file_name = Jinja2TemplateUtil.get_file_name(template, gen_table_schema)
            if file_name:  # 只有当文件名不为空时才添加到列表中
                output_files.append(file_name)

        return [template_list, output_files, context, gen_table_schema]

    @classmethod
    def __get_gen_path(cls, gen_table: GenTableOutSchema, template: str) -> Optional[str]:
        """根据GenTableOutSchema对象和模板名称生成路径。

        参数:
        - gen_table (GenTableOutSchema): 业务表详细信息模型。
        - template (str): 模板名称。

        返回:
        - Optional[str]: 生成的文件路径，若失败则返回None。
        """
        try:
            gen_path = (gen_table.gen_path or '').strip()
            file_name = Jinja2TemplateUtil.get_file_name(template, gen_table)
            if not file_name:
                return None
            # 默认写入到项目根目录（backend的上一级）
            project_root = str(settings.BASE_DIR.parent)
            if gen_path in ['', '/']:
                return os.path.join(project_root, file_name)
            else:
                return os.path.join(gen_path, file_name)
        except Exception:
            return None


class GenTableColumnService:
    """代码生成业务表字段服务层"""

    @classmethod
    async def get_gen_table_column_list_by_table_id_service(cls, auth: AuthSchema, table_id: int) -> List[GenTableColumnOutSchema]:
        """获取业务表字段列表信息。

        参数:
        - auth (AuthSchema): 认证对象。
        - table_id (int): 业务表ID。

        返回:
        - List[GenTableColumnOutSchema]: 业务表字段详细信息模型列表。
        """
        gen_table_column_list_result = await GenTableColumnCRUD(auth).list_gen_table_column_crud({"table_id": table_id})
        return [
            GenTableColumnOutSchema.model_validate(gen_table_column)
            for gen_table_column in gen_table_column_list_result
        ]