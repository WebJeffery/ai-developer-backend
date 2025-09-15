# -*- coding: utf-8 -*-

from fastapi import APIRouter
from .auth.controller import AuthRouter
from .user.controller import UserRouter
from .role.controller import RoleRouter
from .menu.controller import MenuRouter
from .dept.controller import DeptRouter
from .position.controller import PositionRouter
from .dict.controller import DictRouter
from .params.controller import ParamsRouter
from .notice.controller import NoticeRouter
from .log.controller import LogRouter
from .version.controller import VersionRouter
from .ticket.controller import TicketRouter


SystemRouter = APIRouter(prefix="/system")

# 包含所有子路由
SystemRouter.include_router(AuthRouter)
SystemRouter.include_router(UserRouter)
SystemRouter.include_router(RoleRouter)
SystemRouter.include_router(MenuRouter)
SystemRouter.include_router(DeptRouter)
SystemRouter.include_router(PositionRouter)
SystemRouter.include_router(DictRouter)
SystemRouter.include_router(ParamsRouter)
SystemRouter.include_router(NoticeRouter)
SystemRouter.include_router(LogRouter)
SystemRouter.include_router(VersionRouter)
SystemRouter.include_router(TicketRouter)