# -*- coding: utf-8 -*-

from fastapi import APIRouter

from .module_system.auth.controller import AuthRouter
from .module_system.menu.controller import MenuRouter
from .module_system.dept.controller import DeptRouter
from .module_system.role.controller import RoleRouter
from .module_system.user.controller import UserRouter
from .module_system.log.controller import LogRouter
from .module_system.position.controller import PositionRouter
from .module_system.notice.controller import NoticeRouter
from .module_system.config.controller import ConfigRouter
from .module_system.dict.controller import DictRouter

from .module_monitor.cache.controller import CacheRouter
from .module_monitor.job.controller import JobRouter
from .module_monitor.online.controller import OnlineRouter
from .module_monitor.server.controller import ServerRouter

from .module_common.file.controller import FileRouter

from .module_example.demo.controller import DemoRouter


# 定义路由模块映射，按模块分组
SYSTEM_MODULES = [
    {"router": AuthRouter},
    {"router": MenuRouter},
    {"router": DeptRouter},
    {"router": RoleRouter},
    {"router": UserRouter},
    {"router": LogRouter},
    {"router": PositionRouter},
    {"router": NoticeRouter},
    {"router": ConfigRouter},
    {"router": DictRouter},
]

MONITOR_MODULES = [
    {"router": JobRouter},
    {"router": CacheRouter},
    {"router": OnlineRouter},
    {"router": ServerRouter},
]

COMMON_MODULES = [{"router": FileRouter}]

EXAMPLE_MODULES = [{"router": DemoRouter}]


router = APIRouter()
for module in SYSTEM_MODULES:
    router.include_router(
        router=module["router"], prefix="/system"
    )

for module in MONITOR_MODULES:
    router.include_router(
        router=module["router"], prefix="/monitor"
    )

for module in COMMON_MODULES:
    router.include_router(
        router=module["router"], prefix="/common"
    )

for module in EXAMPLE_MODULES:
    router.include_router(
        router=module["router"], prefix="/example"
    )
