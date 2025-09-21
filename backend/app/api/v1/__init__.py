# -*- coding: utf-8 -*-

from fastapi import APIRouter

# 系统管理模块
from .module_system import SystemRouter

# 监控管理模块
from .module_monitor import MonitorRouter

# 通用模块
from .module_common import CommonRouter

# 资源管理模块
from .module_resource import ResourceRouter

# 示例模块
from .module_example import ExampleRouter

# 应用模块
from .module_application import ApplicationRouter

# AI模块
from .module_ai import AIRouter

# 代码生成模块
from .module_generator import GeneratorRouter


# 创建主路由
router = APIRouter()

# 注册各模块路由
router.include_router(SystemRouter)
router.include_router(MonitorRouter)
router.include_router(CommonRouter)
router.include_router(ResourceRouter)
router.include_router(ExampleRouter)
router.include_router(ApplicationRouter)
router.include_router(AIRouter)
router.include_router(GeneratorRouter)