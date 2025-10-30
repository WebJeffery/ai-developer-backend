# -*- coding: utf-8 -*-

from starlette.responses import HTMLResponse
from typing import Any, AsyncGenerator
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.concurrency import asynccontextmanager
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html
)

from app.config.setting import settings
from app.core.ap_scheduler import SchedulerUtil
from app.core.logger import logger
from app.utils.common_util import import_module, import_modules_async
from app.core.exceptions import handle_exception
from app.scripts.initialize import InitializeData
from app.api.v1.module_system.params.service import ParamsService
from app.api.v1.module_system.dict.service import DictDataService
from app.api.v1 import router
from app.utils.console import run as console_run


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[Any, Any]:
    """
    自定义 FastAPI 应用生命周期。

    参数:
    - app (FastAPI): FastAPI 应用实例。

    返回:
    - AsyncGenerator[Any, Any]: 生命周期上下文生成器。
    """
    logger.info(settings.BANNER + '\n' + f'{settings.TITLE} 服务开始启动...')
    
    await InitializeData().init_db()
    logger.info(f"✅️ 初始化 {settings.DATABASE_TYPE} 数据库初始化完成...")
    await import_modules_async(modules=settings.EVENT_LIST, desc="全局事件", app=app, status=True)
    logger.info("✅️ 初始化全局事件完成...")
    # 当 Redis 未连接时，跳过依赖 Redis 的初始化，保证应用可启动
    redis_client = getattr(app.state, 'redis', None)
    if redis_client:
        await ParamsService().init_config_service(redis=redis_client)
        logger.info("✅️ 初始化Redis系统配置完成...")
        await DictDataService().init_dict_service(redis=redis_client)
        logger.info('✅️ 初始化Redis数据字典完成...')
    else:
        logger.warning('未检测到Redis连接，跳过系统配置与数据字典的Redis初始化（降级为无Redis模式）')
    await SchedulerUtil.init_system_scheduler()
    logger.info('✅️ 初始化定时任务完成...')

    logger.info(f'✅️ {settings.TITLE} 服务成功启动...')
    # 控制台输出优化：展示服务信息与文档地址
    console_run(settings.SERVER_HOST, settings.SERVER_PORT, settings.RELOAD, settings.WORKERS)

    yield

    await import_modules_async(modules=settings.EVENT_LIST, desc="全局事件", app=app, status=False)
    await SchedulerUtil.close_system_scheduler()
    logger.info(f'{settings.TITLE} 服务关闭...')

def register_middlewares(app: FastAPI) -> None:
    """
    注册全局中间件。

    参数:
    - app (FastAPI): FastAPI 应用实例。

    返回:
    - None
    """
    for middleware in settings.MIDDLEWARE_LIST[::-1]:
        if not middleware:
            continue
        middleware = import_module(middleware, desc="中间件")
        app.add_middleware(middleware)

def register_exceptions(app: FastAPI) -> None:
    """
    统一注册异常处理器。

    参数:
    - app (FastAPI): FastAPI 应用实例。

    返回:
    - None
    """
    handle_exception(app)

def register_routers(app: FastAPI) -> None:
    """
    注册根路由。

    参数:
    - app (FastAPI): FastAPI 应用实例。

    返回:
    - None
    """
    app.include_router(router=router)

def register_files(app: FastAPI) -> None:
    """
    注册静态资源挂载和文件相关配置。

    参数:
    - app (FastAPI): FastAPI 应用实例。

    返回:
    - None
    """
    # 挂载静态文件目录
    if settings.STATIC_ENABLE:
        # 确保日志目录存在
        settings.STATIC_ROOT.mkdir(parents=True, exist_ok=True)
        app.mount(path=settings.STATIC_URL, app=StaticFiles(directory=settings.STATIC_ROOT), name=settings.STATIC_DIR)

def reset_api_docs(app: FastAPI) -> None:
    """
    使用本地静态资源自定义 API 文档页面（Swagger UI 与 ReDoc）。

    参数:
    - app (FastAPI): FastAPI 应用实例。

    返回:
    - None
    """

    @app.get(settings.DOCS_URL, include_in_schema=False)
    async def custom_swagger_ui_html() -> HTMLResponse:
        return get_swagger_ui_html(
            openapi_url=str(app.root_path) + str(app.openapi_url),
            title=app.title + " - Swagger UI",
            oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
            swagger_js_url=settings.SWAGGER_JS_URL,
            swagger_css_url=settings.SWAGGER_CSS_URL,
            swagger_favicon_url=settings.FAVICON_URL,
        )

    @app.get(str(app.swagger_ui_oauth2_redirect_url), include_in_schema=False)
    async def swagger_ui_redirect():
        return get_swagger_ui_oauth2_redirect_html()

    @app.get(settings.REDOC_URL, include_in_schema=False)
    async def custom_redoc_html():
        return get_redoc_html(
            openapi_url=str(app.root_path) + str(app.openapi_url),
            title=app.title + " - ReDoc",
            redoc_js_url=settings.REDOC_JS_URL,
            redoc_favicon_url=settings.FAVICON_URL,
        )