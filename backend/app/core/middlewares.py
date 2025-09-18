# -*- coding: utf-8 -*-

import time
from typing import Any
from starlette.middleware.cors import CORSMiddleware
from starlette.types import ASGIApp
from starlette.requests import Request
from starlette.middleware.gzip import GZipMiddleware
from starlette.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from app.common.response import ErrorResponse
from app.config.setting import settings
from app.core.logger import logger
from app.core.exceptions import CustomException


class CustomCORSMiddleware(CORSMiddleware):
    """CORS跨域中间件"""
    def __init__(self, app: ASGIApp) -> None:
        CORSMiddlewareConfig: dict[str, Any]    = {
            "allow_origins": settings.ALLOW_ORIGINS,
            "allow_methods": settings.ALLOW_METHODS,
            "allow_headers": settings.ALLOW_HEADERS,
            "allow_credentials": settings.ALLOW_CREDENTIALS
        }
        super().__init__(app, **CORSMiddlewareConfig)


class RequestLogMiddleware(BaseHTTPMiddleware):
    """
    记录请求日志中间件: 提供一个基础的中间件类，允许你自定义请求和响应处理逻辑。
    """
    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        start_time = time.time()

        # 构建请求日志信息
        request_info = f"请求方法: {request.method}, 请求路径: {request.url.path}"
        if request.client:
            request_info = f"请求来源: {request.client.host}, {request_info}"
        logger.info(request_info)

        try:

            if settings.DEMO_ENABLE:
                # 在演示环境中，只有白名单内的IP或路径才能执行非GET请求
                if request.method != "GET":
                    path = request.scope.get("path")

                    request_ip = None
                    x_forwarded_for = request.headers.get('X-Forwarded-For')
                    if x_forwarded_for:
                        # 取第一个 IP 地址，通常为客户端真实 IP
                        request_ip = x_forwarded_for.split(',')[0].strip()
                    else:
                        # 若没有 X-Forwarded-For 头，则使用 request.client.host
                        request_ip = request.client.host if request.client else None

                    # 检查IP是否在白名单，或路径是否在白名单，或用户是否在白名单
                    if (request_ip in settings.DEMO_IP_WHITE_LIST) or (path in settings.DEMO_WHITE_LIST_PATH):
                        response = await call_next(request)
                    else:
                        # 非白名单用户，禁止操作
                        return ErrorResponse(msg="演示环境，禁止操作")
                else:
                    # GET请求在演示环境中总是允许的
                    response = await call_next(request)
            else:
                # 非演示环境，正常处理请求
                response = await call_next(request)
            process_time = round(time.time() - start_time, 5)
            response.headers["X-Process-Time"] = str(process_time)
            
            # 构建响应日志信息
            session_id = request.scope.get('session_id')
            content_length = response.headers.get('content-length', '0')
            response_info = (
                f"会话ID: {session_id}, "
                f"响应状态: {response.status_code}, "
                f"响应内容长度: {content_length}, "
                f"处理时间: {process_time}s"
            )
            logger.info(response_info)
            
            return response
        
        except CustomException as e:
            logger.error(f"系统异常: {str(e)}")
            return ErrorResponse(msg=f"系统异常，请联系管理员", data=str(e))


class CustomGZipMiddleware(GZipMiddleware):
    """GZip压缩中间件"""
    def __init__(self, app: ASGIApp) -> None:
        super().__init__(
            app,
            minimum_size=settings.GZIP_MIN_SIZE,
            compresslevel=settings.GZIP_COMPRESS_LEVEL
        )

