# -*- coding:utf-8 -*-

from datetime import datetime, time
import json
from sqlalchemy.engine.row import Row
from sqlalchemy import delete, func, select, text, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from typing import List, Optional, Sequence, Any, Dict

from app.api.v1.module_system.params.schema import ParamsCreateSchema
from app.core.logger import logger

from .model import GenTableModel, GenTableColumnModel
from app.config.setting import settings
from app.common.request import PaginationService
from .schema import GenTableCreateSchema, GenTableUpdateSchema, GenTableOutSchema, GenTableDeleteSchema, GenTableColumnCreateSchema, GenTableColumnUpdateSchema, GenTableColumnOutSchema, GenTableColumnDeleteSchema, GenDBTableSchema
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

        :param table_id: 业务表id
        :return: 需要生成的业务表信息对象
        """
        gen_table = (
            (
                await self.db.execute(
                    select(GenTableModel)
                    .options(selectinload(GenTableModel.columns))
                    .where(GenTableModel.id == table_id)
                )
            )
            .scalars()
            .first()
        )

        return gen_table

    async def get_gen_table_by_name(self, table_name: str) -> Optional[GenTableModel]:
        """
        根据业务表名称获取需要生成的业务表信息

        :param table_name: 业务表名称
        :return: 需要生成的业务表信息对象
        """
        gen_table = (
            (
                await self.db.execute(
                    select(GenTableModel)
                    .options(selectinload(GenTableModel.columns))
                    .where(GenTableModel.table_name == table_name)
                )
            )
            .scalars()
            .first()
        )

        return gen_table

    async def get_gen_table_all(self) -> Sequence[GenTableModel]:
        """
        获取所有业务表信息

        :param db: orm对象
        :return: 所有业务表信息
        """
        gen_table_all = (
            await self.db.execute(
                select(GenTableModel)
                .options(selectinload(GenTableModel.columns)))
            ).scalars().all()

        return gen_table_all
    
    async def get_gen_table_list(self, search: Optional[GenTableQueryParam] = None):
        """
        根据查询参数获取代码生成业务表列表信息

        :param query_object: 查询参数对象
        :return: 代码生成业务表列表信息对象
        """
        # 构建查询条件
        conditions = await self.__build_conditions(**search.__dict__) if search else []
        query = (
            select(GenTableModel)
            .options(selectinload(GenTableModel.columns))
            .where(
                *conditions
            )
            .order_by(GenTableModel.created_at.desc())
            .distinct()
        )
        
        # 获取所有数据
        result = await self.db.execute(query)
        gen_table_all = list(result.scalars().all())
        
        return gen_table_all

    async def create_table_by_sql(self, sql: str) -> bool:
        """
        根据sql语句创建表结构

        :param db: orm对象
        :param sql_statements: sql语句的ast列表
        :return:
        """
        await self.db.execute(text(sql))
        try:
            await self.db.execute(text(sql))
            # 提交事务
            await self.db.commit()
            await self.db.flush()
            return True
        except Exception as e:
            # 如果发生异常，回滚事务
            await self.db.rollback()
            logger.error(f"创建表时发生错误: {e}")
            return False

    async def add_gen_table(self, add_model: GenTableCreateSchema) -> GenTableModel:
        """
        增加
        """
        gen_table = GenTableModel(**add_model.model_dump(exclude_unset=True, exclude={'sub', 'tree', 'crud'}))
        self.db.add(gen_table)
        await self.db.flush()
        return gen_table
    
    async def delete_gen_table(self, delete_model: GenTableDeleteSchema) -> None:
        """
        删除
        """
        await self.db.execute(delete(GenTableModel).where(GenTableModel.id.in_(delete_model.table_ids)))
        await self.db.flush()
    
    async def edit_gen_table(self, table_id: int, edit_model: GenTableUpdateSchema, auto_commit: bool = True):
        """
        修改
        """
        edit_dict_data = edit_model.model_dump(exclude_unset=True)
        await self.db.execute(update(GenTableModel).where(GenTableModel.id == table_id).values(**edit_dict_data))
        await self.db.flush()
        if auto_commit:
            await self.db.commit()
        return edit_model

    async def get_gen_db_table_list(self, table_name: Optional[str] = None) -> list[Any]:
        """
        根据查询参数获取数据库列表信息

        :param db: orm对象
        :param search: 查询参数对象
        :param order_by: 排序字段
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
                dict_row = GenDBTableSchema(**dict(row._mapping)).model_dump()
                if table_name:
                    dict_row['table_name'] = table_name
                dict_data.append(dict_row)
            else:
                dict_row = GenDBTableSchema(**dict(row)).model_dump()
                dict_data.append(dict_row)
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

    async def get_by_id_crud(self, column_id: int) -> Optional[GenTableColumnModel]:
        """详情"""
        return await self.get(id=column_id)
    
    async def get_list_crud(self, search: Optional[Dict] = None, order_by: Optional[List[Dict[str, str]]] = None) -> Sequence[GenTableColumnModel]:
        """列表查询"""
        return await self.list(search=search, order_by=order_by)
    
    async def create_crud(self, data: GenTableColumnCreateSchema) -> Optional[GenTableColumnModel]:
        """创建"""
        return await self.create(data=data)
    
    async def update_crud(self, id: int, data: GenTableColumnUpdateSchema) -> Optional[GenTableColumnModel]:
        """更新"""
        return await self.update(id=id, data=data)
    
    async def delete_crud(self, data: GenTableColumnDeleteSchema) -> None:
        """批量删除"""
        return await self.delete(ids=data.column_ids)

    async def get_gen_table_column_list_by_table_id_crud(self, table_id: int) -> Sequence[GenTableColumnModel]:
        """根据业务表id获取需要生成的业务表字段列表信息"""
        return await self.list(search={"table_id": table_id})

    async def get_gen_table_column_list_by_table_id(self, table_id: int) -> Sequence[GenTableColumnModel]:
        """
        根据业务表id获取需要生成的业务表字段列表信息

        :param table_id: 业务表id
        :return: 需要生成的业务表字段列表信息对象
        """
        gen_table_column_list = (
            (
                await self.db.execute(
                    select(GenTableColumnModel)
                    .where(GenTableColumnModel.table_id == table_id)
                    .order_by(GenTableColumnModel.sort)
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