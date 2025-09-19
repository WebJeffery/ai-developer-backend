# -*- coding:utf-8 -*-

from datetime import datetime, time
from sqlalchemy import delete, func, select, text, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from typing import List, Optional, Sequence, Any, Dict

from .model import GenTableModel, GenTableColumnModel
from app.config.setting import settings
from app.common.request import PaginationService
from .schema import (
    GenTableBaseSchema,
    GenTableColumnBaseSchema,
    GenTableColumnSchema,
    GenTableSchema,
)
from .param import GenTableQueryParam
from app.core.base_crud import CRUDBase
from app.api.v1.module_system.auth.schema import AuthSchema


class GenTableDao(CRUDBase[GenTableModel, GenTableBaseSchema, GenTableBaseSchema]):
    """
    代码生成业务表模块数据库操作层
    """

    def __init__(self, auth: AuthSchema) -> None:
        """初始化CRUD"""
        super().__init__(model=GenTableModel, auth=auth)

    async def get_gen_table_by_id(self, db: AsyncSession, table_id: int) -> Optional[GenTableModel]:
        """
        根据业务表id获取需要生成的业务表信息

        :param db: orm对象
        :param table_id: 业务表id
        :return: 需要生成的业务表信息对象
        """
        gen_table_info = (
            (
                await db.execute(
                    select(GenTableModel).options(selectinload(GenTableModel.columns)).where(GenTableModel.table_id == table_id)
                )
            )
            .scalars()
            .first()
        )

        return gen_table_info

    async def get_gen_table_by_name(self, db: AsyncSession, table_name: str) -> Optional[GenTableModel]:
        """
        根据业务表名称获取需要生成的业务表信息

        :param db: orm对象
        :param table_name: 业务表名称
        :return: 需要生成的业务表信息对象
        """
        gen_table_info = (
            (
                await db.execute(
                    select(GenTableModel).options(selectinload(GenTableModel.columns)).where(GenTableModel.table_name == table_name)
                )
            )
            .scalars()
            .first()
        )

        return gen_table_info

    async def get_gen_table_all(self, db: AsyncSession) -> Sequence[GenTableModel]:
        """
        获取所有业务表信息

        :param db: orm对象
        :return: 所有业务表信息
        """
        gen_table_all = (await db.execute(select(GenTableModel).options(selectinload(GenTableModel.columns)))).scalars().all()

        return gen_table_all

    async def create_table_by_sql_dao(self, db: AsyncSession, sql_statements: List) -> None:
        """
        根据sql语句创建表结构

        :param db: orm对象
        :param sql_statements: sql语句的ast列表
        :return:
        """
        for sql_statement in sql_statements:
            sql = sql_statement.sql(dialect=settings.DATABASE_TYPE)
            await db.execute(text(sql))

    async def get_gen_table_list(self, db: AsyncSession, query_object: GenTableQueryParam, is_page: bool = False):
        """
        根据查询参数获取代码生成业务表列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 代码生成业务表列表信息对象
        """
        # 构建查询条件
        conditions = []
        
        # 访问name属性而不是table_name
        if query_object.name:
            conditions.append(func.lower(GenTableModel.table_name).like(f'%{str(query_object.name).lower()}%'))
            
        # 访问table_comment属性
        if query_object.table_comment:
            conditions.append(func.lower(GenTableModel.table_comment).like(f'%{str(query_object.table_comment).lower()}%'))
            
        # 访问created_at属性而不是start_time和end_time
        if hasattr(query_object, 'created_at') and query_object.created_at:
            if isinstance(query_object.created_at, tuple) and query_object.created_at[0] == "between":
                conditions.append(GenTableModel.create_time.between(*query_object.created_at[1]))

        query = (
            select(GenTableModel)
            .options(selectinload(GenTableModel.columns))
            .where(*conditions)
            .distinct()
        )
        
        # 获取所有数据
        result = await db.execute(query)
        all_data = list(result.scalars().all())
        
        # 使用PaginationService.paginate进行分页
        if is_page and query_object.page_no is not None and query_object.page_size is not None:
            paginated_result = await PaginationService.paginate(
                data_list=all_data, 
                page_no=query_object.page_no, 
                page_size=query_object.page_size
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

    async def get_gen_db_table_list(self, db: AsyncSession, query_object: GenTableQueryParam, is_page: bool = False):
        """
        根据查询参数获取数据库列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 数据库列表信息对象
        """
        if settings.DATABASE_TYPE == 'postgresql':
            query_sql = """
                table_name as table_name, 
                table_comment as table_comment, 
                create_time as create_time, 
                update_time as update_time
            from 
                list_table
            where 
                table_name not like 'apscheduler_%' 
                and table_name not like 'gen_%'
                and table_name not in (select table_name from gen_table)
            """
        else:
            query_sql = """
                table_name as table_name, 
                table_comment as table_comment, 
                create_time as create_time, 
                update_time as update_time
            from 
                information_schema.tables
            where 
                table_schema = (select database())
                and table_name not like 'apscheduler\_%' 
                and table_name not like 'gen\_%'
                and table_name not in (select table_name from gen_table)
            """
        if query_object.name:
            query_sql += """and lower(table_name) like lower(concat('%', :table_name, '%'))"""
        if query_object.table_comment:
            query_sql += """and lower(table_comment) like lower(concat('%', :table_comment, '%'))"""
        if hasattr(query_object, 'created_at') and query_object.created_at:
            if isinstance(query_object.created_at, tuple) and query_object.created_at[0] == "between":
                # 这里需要特殊处理时间范围查询
                pass
        query_sql += """order by create_time desc"""
        query = select(
            text(query_sql).bindparams(
                **{
                    k: v
                    for k, v in query_object.model_dump(exclude_none=True, exclude={'page_no', 'page_size'}).items()
                }
            )
        )
        
        # 执行查询
        result = await db.execute(query)
        all_data = list(result.fetchall())
        
        # 使用PaginationService.paginate进行分页
        if is_page and query_object.page_no is not None and query_object.page_size is not None:
            paginated_result = await PaginationService.paginate(
                data_list=all_data, 
                page_no=query_object.page_no, 
                page_size=query_object.page_size
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

    async def get_gen_db_table_list_by_names(self, db: AsyncSession, table_names: List[str]):
        """
        根据业务表名称组获取数据库列表信息

        :param db: orm对象
        :param table_names: 业务表名称组
        :return: 数据库列表信息对象
        """
        if settings.DATABASE_TYPE == 'postgresql':
            query_sql = """
            select
                table_name as table_name, 
                table_comment as table_comment, 
                create_time as create_time, 
                update_time as update_time 
            from 
                list_table
            where 
                table_name not like 'qrtz_%' 
                and table_name not like 'gen_%' 
                and table_name = any(:table_names)
            """
        else:
            query_sql = """
            select
                table_name as table_name, 
                table_comment as table_comment, 
                create_time as create_time, 
                update_time as update_time 
            from 
                information_schema.tables
            where 
                table_name not like 'qrtz\_%' 
                and table_name not like 'gen\_%' 
                and table_schema = (select database())
                and table_name in :table_names
            """
        query = text(query_sql).bindparams(table_names=tuple(table_names))
        gen_db_table_list = (await db.execute(query)).fetchall()

        return gen_db_table_list


class GenTableColumnDao(CRUDBase[GenTableColumnModel, GenTableColumnBaseSchema, GenTableColumnBaseSchema]):
    """
    代码生成业务表字段模块数据库操作层
    """

    def __init__(self, auth: AuthSchema) -> None:
        """初始化CRUD"""
        super().__init__(model=GenTableColumnModel, auth=auth)

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

    async def get_gen_db_table_columns_by_name(self, db: AsyncSession, table_name: str):
        """
        根据业务表名称获取业务表字段列表信息

        :param db: orm对象
        :param table_name: 业务表名称
        :return: 业务表字段列表信息对象
        """
        if settings.DATABASE_TYPE == 'postgresql':
            query_sql = """
            select
                column_name, is_required, is_pk, sort, column_comment, is_increment, column_type
            from
                list_column
            where
                table_name = :table_name
            """
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