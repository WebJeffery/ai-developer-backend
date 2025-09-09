# -*- coding: utf-8 -*-

import uuid
import json
from pathlib import Path
from typing import Dict, List
from sqlalchemy import inspect, select, func
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


    async def __init_data(self, db: AsyncSession) -> None:
        """初始化基础数据"""
        for model in self.prepare_init_models:
            table_name = model.__tablename__
            
            # 检查表中是否已经有数据
            count_result = await db.execute(select(func.count()).select_from(model))
            existing_count = count_result.scalar()
            
            if existing_count > 0:
                logger.warning(f"跳过 {table_name} 表数据初始化（表已存在 {existing_count} 条记录）")
                continue

            data = await self.__get_data(table_name)
            if not data:
                logger.warning(f"跳过 {table_name} 表，无初始化数据")
                continue
            
            try:
                # 表为空，直接插入全部数据
                objs = [model(**item) for item in data]
                db.add_all(objs)
                await db.flush()
                logger.info(f"已向 {table_name} 表写入 {len(objs)} 条记录")

            except Exception as e:
                logger.error(f"初始化 {table_name} 表数据失败: {str(e)}")
                raise

    async def __get_data(self, filename: str) -> List[Dict]:
        """读取初始化数据文件"""
        json_path = Path.joinpath(settings.SCRIPT_DIR, f'{filename}.json')
        if not json_path.exists():
            return []

        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                return json.loads(f.read())
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
        await self.__init_data(db)

