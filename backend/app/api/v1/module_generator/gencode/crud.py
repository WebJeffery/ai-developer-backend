# -*- coding:utf-8 -*-

from sqlalchemy.engine.row import Row
from sqlalchemy import and_, delete, select, text, update
from sqlalchemy.orm import selectinload
from sqlglot.expressions import Expression
from typing import List, Optional, Sequence, Dict

from app.core.logger import logger
from app.config.setting import settings
from app.core.base_crud import CRUDBase
from app.api.v1.module_system.auth.schema import AuthSchema
from .param import GenTableQueryParam, GenTableColumnQueryParam
from .model import GenTableModel, GenTableColumnModel
from .schema import (
    GenTableSchema,
    GenTableOutSchema,
    GenTableDeleteSchema,
    GenTableColumnSchema,
    GenTableColumnOutSchema,
    GenTableColumnDeleteSchema,
    GenDBTableSchema,
)


class GenTableCRUD(CRUDBase[GenTableModel, GenTableSchema, GenTableSchema]):
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

        :return: 所有业务表信息列表
        """
        gen_table_all = (
            await self.db.execute(
                select(GenTableModel)
                .options(selectinload(GenTableModel.columns))
                )
            ).scalars().all()

        return gen_table_all

    async def get_gen_table_list(self, search: Optional[GenTableQueryParam] = None) -> Sequence[GenTableModel]:
        """
        根据查询参数获取代码生成业务表列表信息

        :param search: 查询参数对象
        :return: 代码生成业务表列表信息对象
        """
        # 构建查询条件
        conditions = await self.__build_conditions(**search.__dict__) if search else []
        query = (
            select(GenTableModel)
            .options(selectinload(GenTableModel.columns))
            .where(*conditions)
            .order_by(GenTableModel.created_at.desc())
            .distinct()
        )

        # 获取所有数据
        result = await self.db.execute(query)
        gen_table_all = result.scalars().all()

        return gen_table_all

    async def add_gen_table(self, add_model: GenTableSchema) -> GenTableModel:
        """
        增加
        """
        gen_table = GenTableModel(
            **add_model.model_dump(exclude_unset=True, exclude={"sub", "tree", "crud"})
        )
        self.db.add(gen_table)
        await self.db.flush()
        return gen_table
    
    async def edit_gen_table(self, table_id: int, edit_model: GenTableSchema) -> GenTableSchema:
        """
        修改
        """
        edit_dict_data = edit_model.model_dump(exclude_unset=True)
        await self.db.execute(
            update(GenTableModel)
            .where(GenTableModel.id == table_id)
            .values(**edit_dict_data)
        )
        await self.db.flush()
        await self.db.commit()
        return edit_model

    async def delete_gen_table(self, data: GenTableDeleteSchema) -> None:
        """
        删除
        """
        await self.db.execute(
            delete(GenTableModel).where(GenTableModel.id.in_(data.table_ids))
        )
        await self.db.flush()

    async def get_db_table_list(self, search: Optional[GenTableQueryParam] = None) -> list[Dict]:
        """
        根据查询参数获取数据库列表信息

        :param search: 查询参数对象
        :return: 数据库列表信息对象
        """

        # 使用更健壮的方式检测数据库方言
        if settings.DATABASE_TYPE == "postgresql":
            query_sql = (
                select(
                    text("table_catalog as database_name"),
                    text("table_name as table_name"),
                    text("table_type as table_type"),
                    text("table_comment as table_comment"),
                )
                .select_from(text("information_schema.tables"))
                .where(
                    and_(
                        text("table_catalog = (select current_database())"),
                        text("is_insertable_into = 'YES'"),
                        text("table_schema = 'public'"),

                    )
                )
            )
        elif settings.DATABASE_TYPE == "mysql":
            query_sql = (
                select(
                    text("table_schema as database_name"),
                    text("table_name as table_name"),
                    text("table_type as table_type"),
                    text("table_comment as table_comment"),
                )
                .select_from(text("information_schema.tables"))
                .where(
                    and_(
                        text("table_schema = (select database())"),
                    )
                )
            )
        else:
            query_sql = (
                select(
                    text(f"{settings.DATABASE_NAME} as database_name"),
                    text("name as table_name"),
                    text("type as table_type"),
                    text("tbl_name as table_comment"),
                )
                .select_from(text("sqlite_master"))
                .where(
                    and_(
                        text("type = 'table'"),
                    )
                )
            )
        
        # 动态条件构造
        if search and search.table_name:
            query_sql = query_sql.where(
                text("lower(table_name) like lower(:table_name)")
            )
        if search and search.table_comment:
            query_sql = query_sql.where(
                text("lower(table_comment) like lower(:table_comment)")
            )

        # 执行查询
        all_data =(await self.db.execute(query_sql)).fetchall()

        # 将Row对象转换为字典列表，解决JSON序列化问题
        dict_data = []
        for row in all_data:
            # 检查row是否为Row对象
            if isinstance(row, Row):
                # 使用._mapping获取字典
                dict_row = GenDBTableSchema(**dict(row._mapping)).model_dump()
                dict_data.append(dict_row)
            else:
                dict_row = GenDBTableSchema(**dict(row)).model_dump()
                dict_data.append(dict_row)
        return dict_data

    async def get_db_table_list_by_names(self, table_names: List[str]) -> list[GenDBTableSchema]:
        """
        根据业务表名称组获取数据库列表信息

        :param table_names: 业务表名称组
        :return: 数据库列表信息对象
        """
        # 使用更健壮的方式检测数据库方言
        if settings.DATABASE_TYPE == "postgresql":
            query_sql = (
                select(
                    text("table_catalog as database_name"),
                    text("table_name as table_name"),
                    text("table_type as table_type"),
                    text("table_comment as table_comment"),
                )
                .select_from(text("information_schema.tables"))
                .where(
                    and_(
                        text("table_catalog = (select current_database())"),
                        text("is_insertable_into = 'YES'"),
                        text("table_schema = 'public'"),

                    )
                )
            )
        elif settings.DATABASE_TYPE == "mysql":
            query_sql = (
                select(
                    text("table_schema as database_name"),
                    text("table_name as table_name"),
                    text("table_type as table_type"),
                    text("table_comment as table_comment"),
                )
                .select_from(text("information_schema.tables"))
                .where(
                    and_(
                        text("table_schema = (select database())"),
                    )
                )
            )
        else:
            query_sql = (
                select(
                    text(f"{settings.DATABASE_NAME} as database_name"),
                    text("name as table_name"),
                    text("type as table_type"),
                    text("tbl_name as table_comment"),
                )
                .select_from(text("sqlite_master"))
                .where(
                    and_(
                        text("type = 'table'"),
                    )   
                )
            )
        
        query_sql = query_sql.where(
            text(f"table_name in :{table_names}")
        )
        gen_db_table_list = (await self.db.execute(query_sql)).fetchall()
        
        # 将Row对象转换为字典列表，解决JSON序列化问题
        dict_data = []
        for row in gen_db_table_list:
            # 检查row是否为Row对象
            if isinstance(row, Row):
                # 使用._mapping获取字典
                dict_row = GenDBTableSchema(**dict(row._mapping))
                dict_data.append(dict_row)
            else:
                dict_row = GenDBTableSchema(**dict(row))
                dict_data.append(dict_row)
        return dict_data

    async def create_table_by_sql(self, sql_statements: List[Expression | None]) -> None:
        """
        根据sql语句创建表结构

        :param db: orm对象
        :param sql_statements: sql语句的ast列表
        :return:
        """
        try:
            for sql_statement in sql_statements:
                # 检查sql_statement是否为空
                if not sql_statement:
                    continue
                sql = sql_statement.sql(dialect=settings.DATABASE_TYPE)
                await self.db.execute(text(sql))
        except Exception as e:
            # 如果发生异常，回滚事务
            await self.db.rollback()
            logger.error(f"创建表时发生错误: {e}")


class GenTableColumnCRUD(CRUDBase[GenTableColumnModel, GenTableColumnSchema, GenTableColumnSchema]):
    """代码生成业务表字段模块数据库操作层"""

    def __init__(self, auth: AuthSchema) -> None:
        """初始化CRUD"""
        super().__init__(model=GenTableColumnModel, auth=auth)

    async def get_gen_table_column_list_by_table_id(self, table_id: int) -> Optional[GenTableColumnModel]:
        """根据业务表ID获取业务表字段列表信息"""
        return await self.get(table_id=table_id)
    
    async def get_gen_db_table_columns_by_name(self, table_name: str | None) -> List[GenTableColumnOutSchema]:
        """
        根据业务表名称获取业务表字段列表信息

        :param table_name: 业务表名称
        :return: 业务表字段列表信息对象
        """
        # 检查表名是否为空
        if not table_name:
            raise ValueError("数据表名称不能为空")

        # 兼容SQLite和MySQL/PostgreSQL
        if settings.DATABASE_TYPE == "postgresql":
            query_sql = """
                SELECT
                    column_name,
                    (CASE WHEN (is_nullable = 'no' AND column_key != 'PRI') THEN '1' ELSE '0' END) AS is_required,
                    (CASE WHEN column_key = 'PRI' THEN '1' ELSE '0' END) AS is_pk,
                    ordinal_position AS sort,
                    column_comment,
                    (CASE WHEN extra = 'auto_increment' THEN '1' ELSE '0' END) AS is_increment,
                    column_type
                FROM 
                    information_schema.tables
                WHERE 
                    table_catalog = (select current_database())
                    AND is_insertable_into = 'YES'
                    AND table_schema = 'public'
                    AND table_name = :table_name
            """
        elif settings.DATABASE_TYPE == "mysql":
            query_sql = """
                SELECT
                    column_name,
                    (CASE WHEN (is_nullable = 'no' AND column_key != 'PRI') THEN '1' ELSE '0' END) AS is_required,
                    (CASE WHEN column_key = 'PRI' THEN '1' ELSE '0' END) AS is_pk,
                    ordinal_position AS sort,
                    column_comment,
                    (CASE WHEN extra = 'auto_increment' THEN '1' ELSE '0' END) AS is_increment,
                    column_type
                FROM 
                    information_schema.tables
                WHERE 
                    table_schema = (SELECT DATABASE())
                    AND table_name = :table_name
            """
        else:
            query_sql = f"""
                SELECT
                    column_name,
                    (CASE WHEN (is_nullable = 'no' AND column_key != 'PRI') THEN '1' ELSE '0' END) AS is_required,
                    (CASE WHEN column_key = 'PRI' THEN '1' ELSE '0' END) AS is_pk,
                    ordinal_position AS sort,
                    column_comment,
                    (CASE WHEN extra = 'auto_increment' THEN '1' ELSE '0' END) AS is_increment,
                    column_type
                FROM 
                    sqlite_master
                WHERE 
                    type = 'table'
                    AND name = :table_name
            """

        query = text(query_sql).bindparams(table_name=table_name)
        gen_db_table_columns_raw = (
            await self.db.execute(query)
        ).fetchall()

        return [
            GenTableColumnOutSchema(
                column_name=row[0],
                is_required=row[1],
                is_pk=row[2],
                sort=row[3],
                column_comment=row[4],
                is_increment=row[5],
                column_type=row[6],
            )
            for row in gen_db_table_columns_raw
        ]

    async def list_gen_table_column_crud(self, search: Optional[Dict] = None, order_by: Optional[List[Dict[str, str]]] = None) -> Sequence[GenTableColumnModel]:
        """根据业务表ID查询业务表字段列表"""
        return await self.list(search=search, order_by=order_by)

    async def create_gen_table_column_crud(self, data: GenTableColumnSchema) -> Optional[GenTableColumnModel]:
        """创建业务表字段"""
        return await self.create(data=data)

    async def update_gen_table_column_crud(self, id: int, data: GenTableColumnSchema) -> Optional[GenTableColumnModel]:
        """更新业务表字段"""
        return await self.update(id=id, data=data)

    async def delete_gen_table_column_by_table_id_dao(self, data: GenTableDeleteSchema) -> None:
        """根据业务表ID批量删除"""
        return await self.delete(ids=data.table_ids)

    async def delete_gen_table_column_by_column_id_dao(self, data: GenTableColumnDeleteSchema) -> None:
        """根据业务表字段ID批量删除"""
        return await self.delete(ids=data.column_ids)
