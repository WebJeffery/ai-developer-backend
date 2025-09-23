# -*- coding: utf-8 -*-

from fastapi import APIRouter
from .gencode.controller import GenRouter

# 创建代码生成模块路由
GeneratorRouter = APIRouter(prefix="/generator")

# 包含代码生成路由
GeneratorRouter.include_router(GenRouter)