# -*- coding: utf-8 -*-

from rich import get_console
from rich.panel import Panel
from rich.prompt import IntPrompt
from rich.table import Table
from rich.text import Text

from app.config.setting import settings

console = get_console()

def run(host: str, port: int, reload: bool, workers: int) -> None:
    url = f'http://{host}:{port}'
    base_url = f'{url}{settings.ROOT_PATH}'
    docs_url = base_url + settings.DOCS_URL
    redoc_url = base_url + settings.REDOC_URL

    panel_content = Text()
    panel_content.append(f'当前版本: v{settings.VERSION}')
    panel_content.append(f'\n服务地址: {url}')
    panel_content.append(f'\n根路由前缀: {settings.ROOT_PATH}')
    panel_content.append(f'\n运行环境: {getattr(settings.ENVIRONMENT, "value", settings.ENVIRONMENT)}')
    panel_content.append(f'\n数据库类型: {settings.DATABASE_TYPE}')
    panel_content.append(f'\n日志级别: {settings.LOGGER_LEVEL}')
    panel_content.append(f'\n重载: {reload}  进程: {workers}')
    panel_content.append('\n官方地址: https://service.fastapiadmin.com')

    if settings.DEBUG:
        panel_content.append(f'\n\n📖 Swagger 文档: {docs_url}', style='yellow')
        panel_content.append(f'\n📚 Redoc   文档: {redoc_url}', style='blue')

    console.print(Panel(panel_content, title='FastAPI_Vue3_Admin 服务信息', border_style='purple', padding=(1, 2)))
