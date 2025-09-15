# -*- coding: utf-8 -*-

from fastapi import APIRouter

from .demo.controller import DemoRouter


ExampleRouter = APIRouter(prefix="/example")

# 包含所有子路由
ExampleRouter.include_router(DemoRouter)