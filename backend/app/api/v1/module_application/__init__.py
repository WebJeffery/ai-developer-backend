# -*- coding: utf-8 -*-

from fastapi import APIRouter

from .myapp.controller import MyAppRouter


ApplicationRouter = APIRouter(prefix="/application")

# 包含所有子路由
ApplicationRouter.include_router(MyAppRouter)