# -*- coding:utf-8 -*-

from datetime import datetime, time
import json
from sqlalchemy.engine.row import Row
from sqlalchemy import delete, func, select, text, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from typing import List, Optional, Sequence, Any, Dict

from .model import GenTableModel, GenTableColumnModel
from app.config.setting import settings
from app.common.request import PaginationService
from .schema import GenTableCreateSchema, GenTableUpdateSchema, GenTableOutSchema, GenTableDeleteSchema, GenTableColumnCreateSchema, GenTableColumnUpdateSchema, GenTableColumnOutSchema, GenTableColumnDeleteSchema
from .param import GenTableQueryParam
from app.core.base_crud import CRUDBase
from app.api.v1.module_system.auth.schema import AuthSchema


class GenTableCRUD(CRUDBase[GenTableModel, GenTableCreateSchema, GenTableUpdateSchema]):
    """代码生成业务表模块数据库操作层"""

    def __init__(self, auth: AuthSchema) -> None:
        """初始化CRUD"""
        super().__init__(model=GenTableModel, auth=auth)

    async def get_gen_table_by_id(self, table_id: int) -> Optional[GenTableModel]:
        """
        根据业务表id获取需要生成的业务表信息

        :param db: orm对象
        :param table_id: 业务表id
        :return: 需要生成的业务表信息对象
        """
        gen_table_info = (
            (
                await self.db.execute(
                    select(GenTableModel).options(selectinload(GenTableModel.columns)).where(GenTableModel.id == table_id)
                )
            )
            .scalars()
            .first()
        )

        return gen_table_info

    async def get_gen_table_by_name(self, table_name: str) -> Optional[GenTableModel]:
        """
        根据业务表名称获取需要生成的业务表信息

        :param db: orm对象
        :param table_name: 业务表名称
        :return: 需要生成的业务表信息对象
        """
        gen_table_info = (
            (
                await self.db.execute(
                    select(GenTableModel).options(selectinload(GenTableModel.columns)).where(GenTableModel.table_name == table_name)
                )
            )
            .scalars()
            .first()
        )

        return gen_table_info

    async def get_gen_table_all(self) -> Sequence[GenTableModel]:
        """
        获取所有业务表信息

        :param db: orm对象
        :return: 所有业务表信息
        """
        gen_table_all = (await self.db.execute(select(GenTableModel).options(selectinload(GenTableModel.columns)))).scalars().all()

        return gen_table_all

    async def create_table_by_sql(self, sql_statements: List) -> None:
        """
        根据sql语句创建表结构

        :param db: orm对象
        :param sql_statements: sql语句的ast列表
        :return:
        """
        for sql_statement in sql_statements:
            sql = sql_statement.sql(dialect=settings.DATABASE_TYPE)
            await self.db.execute(text(sql))

    async def get_gen_table_list(self, query_object: GenTableQueryParam, is_page: bool = False):
        """
        根据查询参数获取代码生成业务表列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 代码生成业务表列表信息对象
        """
        # 构建查询条件
        conditions = []
        
        # 访问table_name属性
        if getattr(query_object, 'table_name', None) and query_object.table_name[1]:
            conditions.append(func.lower(GenTableModel.table_name).like(f'%{str(query_object.table_name[1]).lower()}%'))
            
        # 访问table_comment属性
        if getattr(query_object, 'table_comment', None):
            conditions.append(func.lower(GenTableModel.table_comment).like(f'%{str(query_object.table_comment).lower()}%'))
            
        # 访问created_at属性而不是start_time和end_time
        if hasattr(query_object, 'created_at') and query_object.created_at:
            if isinstance(query_object.created_at, tuple) and query_object.created_at[0] == "between":
                conditions.append(GenTableModel.created_at.between(*query_object.created_at[1]))

        query = (
            select(GenTableModel)
            .options(selectinload(GenTableModel.columns))
            .where(*conditions)
            .order_by(GenTableModel.created_at.desc())
            .distinct()
        )
        
        # 获取所有数据
        result = await self.db.execute(query)
        all_data = list(result.scalars().all())
        
        # 使用PaginationService.paginate进行分页
        # 注意：这里假设query_object有page_no和page_size属性，如果没有需要从其他地方获取
        page_no = getattr(query_object, 'page_no', None)
        page_size = getattr(query_object, 'page_size', None)
        if is_page and page_no is not None and page_size is not None:
            paginated_result = await PaginationService.paginate(
                data_list=all_data, 
                page_no=page_no, 
                page_size=page_size
            )
            return paginated_result
        else:
            return {
                "items": all_data,
                "total": len(all_data),
                "page_no": None,
                "page_size": None,
                "has_next": False
            }

    async def get_gen_db_table_list(self, search: GenTableQueryParam, order_by: Optional[List[Dict[str, str]]] = None) -> list[Any]:
        """
        根据查询参数获取数据库列表信息

        :param db: orm对象
        :param search: 查询参数对象
        :param order_by: 排序字段
        :return: 数据库列表信息对象
        """
    #  pg数据库   
    # {
    #     "table_catalog": "fastapiadmin",
    #     "table_schema": "pg_catalog",
    #     "table_name": "pg_foreign_table",
    #     "table_type": "BASE TABLE",
    #     "self_referencing_column_name": null,
    #     "reference_generation": null,
    #     "user_defined_type_catalog": null,
    #     "user_defined_type_schema": null,
    #     "user_defined_type_name": null,
    #     "is_insertable_into": "YES",
    #     "is_typed": "NO",
    #     "commit_action": null
    #   }

    # mysql
    # {
    #     "TABLE_CATALOG": "def",
    #     "TABLE_SCHEMA": "fastapiadmin",
    #     "TABLE_NAME": "ai_mcp",
    #     "TABLE_TYPE": "BASE TABLE",
    #     "ENGINE": "InnoDB",
    #     "VERSION": 10,
    #     "ROW_FORMAT": "Dynamic",
    #     "TABLE_ROWS": 0,
    #     "AVG_ROW_LENGTH": 0,
    #     "DATA_LENGTH": 16384,
    #     "MAX_DATA_LENGTH": 0,
    #     "INDEX_LENGTH": 16384,
    #     "DATA_FREE": 0,
    #     "AUTO_INCREMENT": null,
    #     "CREATE_TIME": "2025-10-02T03:43:02",
    #     "UPDATE_TIME": null,
    #     "CHECK_TIME": null,
    #     "TABLE_COLLATION": "utf8mb4_0900_ai_ci",
    #     "CHECKSUM": null,
    #     "CREATE_OPTIONS": "",
    #     "TABLE_COMMENT": "MCP 服务器表"
    #   },

    # sqlite
    # {
    #   "type": "table",
    #     "name": "system_users",
    #     "tbl_name": "system_users",
    #     "rootpage": 47,
    #     "sql": "CREATE TABLE system_users (\n\tusername VARCHAR(32) NOT NULL, \n\tpassword VARCHAR(255) NOT NULL, \n\tname VARCHAR(32) NOT NULL, \n\tstatus BOOLEAN NOT NULL, \n\tmobile VARCHAR(20), \n\temail VARCHAR(64), \n\tgender VARCHAR(1), \n\tavatar VARCHAR(500), \n\tis_superuser BOOLEAN NOT NULL, \n\tlast_login DATETIME, \n\tdept_id INTEGER, \n\tcreator_id INTEGER, \n\tid INTEGER NOT NULL, \n\tdescription TEXT, \n\tcreated_at DATETIME, \n\tupdated_at DATETIME, \n\tPRIMARY KEY (id), \n\tUNIQUE (username), \n\tUNIQUE (mobile), \n\tUNIQUE (email), \n\tFOREIGN KEY(dept_id) REFERENCES system_dept (id) ON DELETE SET NULL ON UPDATE CASCADE\n)"
    #   },

        # 使用更健壮的方式检测数据库方言
        if settings.DATABASE_TYPE == 'postgresql':
            query_sql = """
                SELECT
                    table_catalog as database_name,
                    table_name as table_name,
                    table_type as table_type,
                    table_schema as table_comment
                from 
                    information_schema.tables
                where 
                    table_catalog = (select current_database())
                    and is_insertable_into = 'YES'
                    and table_schema = 'public'
            """
        elif settings.DATABASE_TYPE == 'mysql':
            query_sql = """
                SELECT
                    table_schema as database_name,
                    table_name as table_name,
                    table_type as table_type,
                    table_comment as table_comment
                from 
                    information_schema.tables
                where 
                    table_schema = (select database())
            """
        else:
            query_sql = f"""
                SELECT
                    '{settings.DATABASE_NAME}' as database_name,
                    name as table_name,
                    type as table_type,
                    tbl_name as table_comment
                from 
                    sqlite_master
                where 
                    type = 'table'
            """
        
        # 直接执行文本SQL查询，避免SQLAlchemy自动添加额外的SELECT )
        query = text(query_sql).bindparams()
        
        # 执行查询
        result = await self.db.execute(query)
        all_data = result.fetchall()

        # 将Row对象转换为字典列表，解决JSON序列化问题
        dict_data = []
        for row in all_data:
            # 检查row是否为Row对象
            if isinstance(row, Row):
                # 使用._mapping获取字典
                dict_row = dict(row._mapping)
                dict_data.append(dict_row)
            else:
                dict_data.append(row)
        return dict_data

    async def get_gen_db_table_list_by_names(self, table_names: List[str]):
        """
        根据业务表名称组获取数据库列表信息

        :param db: orm对象
        :param table_names: 业务表名称组
        :return: 数据库列表信息对象
        """
        # 使用更健壮的方式检测数据库方言
        if settings.DATABASE_TYPE == 'postgresql':
            query_sql = """
                SELECT
                    table_catalog as database_name,
                    table_name as table_name,
                    table_type as table_type,
                    table_schema as table_comment
                from 
                    information_schema.tables
                where 
                    table_catalog = (select current_database())
                    and is_insertable_into = 'YES'
                    and table_schema = 'public'
                    and table_name in :table_names
            """
        elif settings.DATABASE_TYPE == 'mysql':
            query_sql = """
                SELECT
                    table_schema as database_name,
                    table_name as table_name,
                    table_type as table_type,
                    table_comment as table_comment
                from 
                    information_schema.tables
                where 
                    table_schema = (select database())
                    and table_name in :table_names
            """
        else:
            query_sql = f"""
                SELECT
                    '{settings.DATABASE_NAME}' as database_name,
                    name as table_name,
                    type as table_type,
                    tbl_name as table_comment
                from 
                    sqlite_master
                where 
                    type = 'table'
                    and table_name in :table_names
            """
        
        query = text(query_sql).bindparams(table_names=tuple(table_names))
        gen_db_table_list = (await self.db.execute(query)).fetchall()

        return gen_db_table_list


class GenTableColumnCRUD(CRUDBase[GenTableColumnModel, GenTableColumnCreateSchema, GenTableColumnUpdateSchema]):
    """代码生成业务表字段模块数据库操作层"""

    def __init__(self, auth: AuthSchema) -> None:
        """初始化CRUD"""
        super().__init__(model=GenTableColumnModel, auth=auth)

    async def get_gen_table_column_list_by_table_id_crud(self, table_id: int) -> Sequence[GenTableColumnModel]:
        """根据业务表id获取需要生成的业务表字段列表信息"""
        return await self.list(search={"table_id": table_id})

    async def get_gen_table_column_list_by_table_id(self, db: AsyncSession, table_id: int) -> Sequence[GenTableColumnModel]:
        """
        根据业务表id获取需要生成的业务表字段列表信息

        :param db: orm对象
        :param table_id: 业务表id
        :return: 需要生成的业务表字段列表信息对象
        """
        gen_table_column_list = (
            (
                await db.execute(
                    select(GenTableColumnModel).where(GenTableColumnModel.table_id == table_id).order_by(GenTableColumnModel.sort)
                )
            )
            .scalars()
            .all()
        )

        return gen_table_column_list

    async def get_gen_db_table_columns_by_name(self, db: AsyncSession, table_name: str) -> Sequence[Row[Any]]:
        """
        根据业务表名称获取业务表字段列表信息

        :param db: orm对象
        :param table_name: 业务表名称
        :return: 业务表字段列表信息对象
        """
        # 兼容SQLite和MySQL/PostgreSQL
        if str(db.bind.dialect) == 'sqlite':
            query_sql = """
            pragma table_info(:table_name)
            """
            query = text(query_sql).bindparams(table_name=table_name)
            gen_db_table_columns_raw = (await db.execute(query)).fetchall()
            
            # 转换SQLite的pragma结果为与information_schema.columns兼容的格式
            gen_db_table_columns = []
            for col in gen_db_table_columns_raw:
                # col格式: (cid, name, type, notnull, dflt_value, pk)
                is_required = '1' if col[3] == 1 and col[5] == 0 else '0'
                is_pk = '1' if col[5] == 1 else '0'
                is_increment = '0'  # SQLite没有auto_increment标记，需要额外判断
                
                # 构建兼容的结果行
                gen_db_table_columns.append({
                    'column_name': col[1],
                    'is_required': is_required,
                    'is_pk': is_pk,
                    'sort': col[0],  # 使用cid作为排序
                    'column_comment': '',  # SQLite不存储列注释
                    'is_increment': is_increment,
                    'column_type': col[2]
                })
        else:
            query_sql = """
            select 
                column_name as column_name,
                case 
                    when is_nullable = 'no' and column_key != 'PRI' then '1' 
                    else '0' 
                end as is_required,
                case 
                    when column_key = 'PRI' then '1' 
                    else '0' 
                end as is_pk,
                ordinal_position as sort,
                column_comment as column_comment,
                case 
                    when extra = 'auto_increment' then '1' 
                    else '0' 
                end as is_increment,
                column_type as column_type
            from 
                information_schema.columns
            where 
                table_schema = (select database()) 
                and table_name = :table_name
            order by 
                ordinal_position
            """
            query = text(query_sql).bindparams(table_name=table_name)
            gen_db_table_columns = (await db.execute(query)).fetchall()

        return gen_db_table_columns