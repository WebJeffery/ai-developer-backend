# -*- coding: utf-8 -*-

import uuid
import json
from pathlib import Path
from typing import Dict, List
from sqlalchemy import inspect, select, func, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.base_model import MappedBase
from app.core.logger import logger
from app.config.setting import settings

from app.api.v1.module_system.user.model import UserModel, UserRolesModel, UserPositionsModel
from app.api.v1.module_system.role.model import RoleModel, RoleDeptsModel, RoleMenusModel
from app.api.v1.module_system.position.model import PositionModel
from app.api.v1.module_system.dept.model import DeptModel
from app.api.v1.module_system.menu.model import MenuModel
from app.api.v1.module_system.log.model import OperationLogModel
from app.api.v1.module_system.notice.model import NoticeModel
from app.api.v1.module_system.config.model import ConfigModel
from app.api.v1.module_system.dict.model import DictTypeModel, DictDataModel
from app.api.v1.module_monitor.job.model import JobModel, JobLogModel
from app.api.v1.module_example.demo.model import DemoModel
from app.api.v1.module_application.myapp.model import ApplicationModel


class InitializeData:
    """
    初始化数据库和基础数据
    """

    def __init__(self) -> None:
        # 按照依赖关系排序：先创建基础表，再创建关联表
        self.prepare_init_models = [
            # 部门表（自引用，需要先创建）
            DeptModel,
            # 菜单表（自引用，需要先创建）
            MenuModel,
            # 用户表（依赖部门和角色）
            UserModel,
            # 角色表（依赖菜单和部门）
            RoleModel,
            # 岗位表（无外键依赖）
            PositionModel,
            # 基础表（无外键依赖）
            ConfigModel,
            DictTypeModel,
            NoticeModel,
            OperationLogModel,
            DictDataModel,
            JobModel,
            JobLogModel,
            DemoModel,
            ApplicationModel,
            # 关联表（依赖基础表）
            UserPositionsModel,
            UserRolesModel,
            RoleDeptsModel,
            RoleMenusModel,
        ]
        # 需要更新序列的模型（排除关联表模型，因为它们没有id字段）
        self.models_with_id = [
            DeptModel,
            MenuModel,
            UserModel,
            RoleModel,
            PositionModel,
            ConfigModel,
            DictTypeModel,
            NoticeModel,
            OperationLogModel,
            DictDataModel,
            JobModel,
            JobLogModel,
            DemoModel,
            ApplicationModel,
        ]
        self.created_tables = set()
        
    async def __get_existing_tables(self, db: AsyncSession) -> List[str]:
        return await db.run_sync(
            lambda sync_db: inspect(sync_db.get_bind()).get_table_names()
        )

    async def __init_model(self, db: AsyncSession) -> None:
        """初始化数据库表结构"""
        try:
            # 获取所有模型元数据
            metadata = MappedBase.metadata
            
            # 只创建不存在的表
            for table in metadata.sorted_tables:
                if table.name not in await self.__get_existing_tables(db):
                    await db.run_sync(lambda sync_db: table.create(sync_db.bind))
                    self.created_tables.add(table.name)
                    logger.info(f"已创建表: {table.name}")

            await self.__init_data(db)
        except Exception as e:
            logger.error(f"初始化数据库结构失败: {str(e)}")
            raise

    async def __init_data(self, db: AsyncSession) -> None:
        """初始化基础数据"""
        try:
            inserted_data = False  # 标记是否有数据插入
            
            for model in self.prepare_init_models:
                table_name = model.__tablename__
                
                # 检查表中是否已经有数据
                count_result = await db.execute(select(func.count()).select_from(model))
                existing_count = count_result.scalar()
                
                logger.info(f"检查表 {table_name} 数据: 已存在 {existing_count} 条记录")
                
                if existing_count > 0:
                    logger.warning(f"跳过 {table_name} 表数据初始化（表已存在 {existing_count} 条记录）")
                    continue

                data = await self.__get_data(table_name)
                if not data:
                    logger.warning(f"跳过 {table_name} 表，无初始化数据")
                    continue
                
                try:
                    # 表为空，直接插入全部数据
                    logger.info(f"准备向 {table_name} 表插入 {len(data)} 条记录")
                    objs = [model(**item) for item in data]
                    db.add_all(objs)
                    inserted_data = True
                    
                    # 对于 PostgreSQL，更新序列值
                    if settings.DATABASE_TYPE == "postgresql" and model in self.models_with_id and len(objs) > 0:
                        await self.__update_postgresql_sequence_for_model(db, model, table_name)
                    
                    logger.info(f"已向 {table_name} 表写入 {len(objs)} 条记录")

                except Exception as e:
                    logger.error(f"初始化 {table_name} 表数据失败: {str(e)}")
                    raise
            
            # 只有在有数据插入时才提交事务
            if inserted_data:
                await db.commit()
                logger.info("数据初始化事务已提交")
            else:
                logger.info("没有新数据需要插入，跳过事务提交")
                
        except Exception as e:
            logger.error(f"初始化数据过程中出现错误: {str(e)}")
            # 如果出现错误，回滚事务
            await db.rollback()
            raise

    async def __update_postgresql_sequence_for_model(self, db: AsyncSession, model, table_name: str) -> None:
        """为特定模型更新 PostgreSQL 序列值"""
        try:
            # 检查模型是否有id属性
            if not hasattr(model, 'id'):
                return
                
            # 获取表中最大的 ID 值
            max_id_result = await db.execute(select(func.max(model.id)).select_from(model))
            max_id = max_id_result.scalar()
            
            if max_id is not None and max_id > 0:
                # 更新序列值
                sequence_name = f"{table_name}_id_seq"
                await db.execute(text(f"SELECT setval('{sequence_name}', {max_id}, true)"))
                logger.info(f"已更新 {table_name} 表的序列 {sequence_name} 值为 {max_id}")
        except Exception as e:
            logger.error(f"更新 {table_name} 表的 PostgreSQL 序列值失败: {str(e)}")
            # 不抛出异常，因为序列更新失败不应该导致整个初始化失败

    async def __get_data(self, table_name: str) -> List[Dict]:
        """读取初始化数据文件"""
        json_path = Path.joinpath(settings.SCRIPT_DIR, f'{table_name}.json')
        logger.info(f"尝试读取初始化数据文件: {json_path}")
        if not json_path.exists():
            logger.warning(f"初始化数据文件不存在: {json_path}")
            return []

        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.loads(f.read())
                logger.info(f"成功读取 {table_name} 数据文件，包含 {len(data)} 条记录")
                return data
        except json.JSONDecodeError as e:
            logger.error(f"解析 {json_path} 失败: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"读取 {json_path} 失败: {str(e)}")
            raise

    async def init_db(self, db: AsyncSession) -> None:
        """
        执行完整初始化流程
        """
        logger.info("开始执行数据库初始化流程")
        await self.__init_model(db)
        # 刷新session以确保数据可见性
        await db.flush()
        logger.info("数据库初始化流程完成")