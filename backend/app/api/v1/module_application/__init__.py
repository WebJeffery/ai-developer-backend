# -*- coding: utf-8 -*-

from fastapi import APIRouter

from .myapp.controller import MyAppRouter
from .ai.controller import AIRouter
from .job.controller import JobRouter


ApplicationRouter = APIRouter(prefix="/application")

# 包含所有子路由
ApplicationRouter.include_router(MyAppRouter)
ApplicationRouter.include_router(AIRouter)
ApplicationRouter.include_router(JobRouter)