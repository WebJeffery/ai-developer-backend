# -*- coding: utf-8 -*-
"""
AI模块初始化文件
"""

from fastapi import APIRouter

from .mcp.controller import MCPRouter


AIRouter = APIRouter(prefix="/ai")

# 包含所有子路由
AIRouter.include_router(MCPRouter)