# -*- coding: utf-8 -*-

from fastapi import APIRouter

from .file.controller import FileRouter


CommonRouter = APIRouter(prefix="/common")

# 包含所有子路由
CommonRouter.include_router(FileRouter)