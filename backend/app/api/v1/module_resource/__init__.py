# -*- coding: utf-8 -*-

from fastapi import APIRouter

from .resource.controller import ResourceFileRouter


ResourceRouter = APIRouter(prefix="/resource")

# 包含所有子路由
ResourceRouter.include_router(ResourceFileRouter)