# -*- coding: utf-8 -*-

from fastapi import APIRouter

from .cache.controller import CacheRouter
from .job.controller import JobRouter
from .online.controller import OnlineRouter
from .server.controller import ServerRouter
from .resource.controller import ResourceRouter


MonitorRouter = APIRouter(prefix="/monitor")

# 包含所有子路由
MonitorRouter.include_router(CacheRouter)
MonitorRouter.include_router(JobRouter)
MonitorRouter.include_router(OnlineRouter)
MonitorRouter.include_router(ServerRouter)
MonitorRouter.include_router(ResourceRouter)