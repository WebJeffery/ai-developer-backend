# -*- coding:utf-8 -*-

from datetime import datetime
from fastapi import APIRouter, Depends, Query, Request, Body
from fastapi.responses import StreamingResponse
from pydantic_validation_decorator import ValidateFields
from sqlalchemy.ext.asyncio import AsyncSession
from app.common.enums import BusinessType
from app.common.response import SuccessResponse, ErrorResponse, StreamResponse
from app.core.dependencies import AuthPermission
from app.core.router_class import OperationLogRoute
from app.core.base_params import PaginationQueryParam
from app.api.v1.module_system.auth.schema import AuthSchema
from app.api.v1.module_system.user.schema import UserOutSchema
from .param import GenTableQueryParam
from .schema import DeleteGenTableSchema, EditGenTableSchema, GenTableSchema
from .service import GenTableColumnService, GenTableService
from app.utils.common_util import bytes2file_response
from app.core.logger import logger


genController = APIRouter(route_class=OperationLogRoute, prefix='/tool/gen', tags=["代码生成模块"])


@genController.get('/list', summary="查询代码生成业务表列表", description="查询代码生成业务表列表")
async def get_gen_table_list(
    page: PaginationQueryParam = Depends(),
    search: GenTableQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(permissions=["tool:gen:list"]))
):
    # 获取分页数据
    gen_page_query_result = await GenTableService.get_gen_table_list_services(auth, search, is_page=True)
    logger.info('获取代码生成业务表列表成功')
    return SuccessResponse(data=gen_page_query_result, msg="获取代码生成业务表列表成功")


@genController.get('/db/list', summary="查询数据库表列表", description="查询数据库表列表")
async def get_gen_db_table_list(
    page: PaginationQueryParam = Depends(),
    search: GenTableQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(permissions=["tool:gen:list"]))
):
    # 获取分页数据
    gen_page_query_result = await GenTableService.get_gen_db_table_list_services(auth, search, is_page=True)
    logger.info('获取数据库表列表成功')
    return SuccessResponse(data=gen_page_query_result, msg="获取数据库表列表成功")


@genController.post('/importTable', summary="导入表结构", description="导入表结构")
@ValidateFields(validate_model='edit_gen_table')
async def import_gen_table(
    tables: str = Query(..., description="表名列表"),
    auth: AuthSchema = Depends(AuthPermission(permissions=["tool:gen:import"])),
    current_user: UserOutSchema = Depends(lambda auth: auth.user)
):
    table_names = tables.split(',') if tables else []
    add_gen_table_list = await GenTableService.get_gen_db_table_list_by_name_services(auth, table_names)
    result = await GenTableService.import_gen_table_services(auth, add_gen_table_list, current_user)
    logger.info('导入表结构成功')
    return result


@genController.put('', summary="编辑业务表信息", description="编辑业务表信息")
@ValidateFields(validate_model='edit_gen_table')
async def edit_gen_table(
    data: EditGenTableSchema,
    auth: AuthSchema = Depends(AuthPermission(permissions=["tool:gen:edit"])),
    current_user: UserOutSchema = Depends(lambda auth: auth.user)
):
    data.update_by = current_user.username
    data.update_time = datetime.now()
    await GenTableService.validate_edit(data)
    edit_gen_result = await GenTableService.edit_gen_table_services(auth, data)
    logger.info('编辑业务表信息成功')
    return SuccessResponse(data=edit_gen_result, msg="编辑业务表信息成功")


@genController.delete('/{table_ids}', summary="删除业务表信息", description="删除业务表信息")
async def delete_gen_table(
    table_ids: str,
    auth: AuthSchema = Depends(AuthPermission(permissions=["tool:gen:remove"]))
):
    delete_gen_table = DeleteGenTableSchema(table_ids=table_ids)
    result = await GenTableService.delete_gen_table_services(auth, delete_gen_table)
    logger.info('删除业务表信息成功')
    return result


@genController.post('/createTable', summary="创建表结构", description="创建表结构")
async def create_table(
    sql: str = Query(..., description="SQL语句"),
    auth: AuthSchema = Depends(AuthPermission(permissions=["tool:gen:create"])),
    current_user: UserOutSchema = Depends(lambda auth: auth.user)
):
    result = await GenTableService.create_table_services(auth, sql, current_user)
    logger.info('创建表结构成功')
    return result


@genController.get('/batchGenCode', summary="批量生成代码", description="批量生成代码")
async def batch_gen_code(
    tables: str = Query(..., description="表名列表"),
    auth: AuthSchema = Depends(AuthPermission(permissions=["tool:gen:code"]))
):
    table_names = tables.split(',') if tables else []
    batch_gen_code_result = await GenTableService.batch_gen_code_services(auth, table_names)
    logger.info('批量生成代码成功')
    return StreamResponse(
        data=bytes2file_response(batch_gen_code_result),
        media_type='application/zip',
        headers={'Content-Disposition': 'attachment; filename=code.zip'}
    )


@genController.get('/genCode/{table_name}', summary="生成代码到指定路径", description="生成代码到指定路径")
async def gen_code_local(
    table_name: str,
    auth: AuthSchema = Depends(AuthPermission(permissions=["tool:gen:code"]))
):
    from app.config.setting import settings
    if not settings.allow_overwrite:
        logger.error('【系统预设】不允许生成文件覆盖到本地')
        return ErrorResponse(msg='【系统预设】不允许生成文件覆盖到本地')
    result = await GenTableService.generate_code_services(auth, table_name)
    logger.info('生成代码到指定路径成功')
    return result


@genController.get('/{table_id}', summary="获取业务表详细信息", description="获取业务表详细信息")
async def query_detail_gen_table(
    table_id: int,
    auth: AuthSchema = Depends(AuthPermission(permissions=["tool:gen:query"]))
):
    gen_table = await GenTableService.get_gen_table_by_id_services(auth, table_id)
    gen_tables = await GenTableService.get_gen_table_all_services(auth)
    gen_columns = await GenTableColumnService.get_gen_table_column_list_by_table_id_services(auth, table_id)
    gen_table_detail_result = dict(info=gen_table, rows=gen_columns, tables=gen_tables)
    logger.info(f'获取table_id为{table_id}的信息成功')
    return SuccessResponse(data=gen_table_detail_result, msg="获取业务表详细信息成功")


@genController.get('/preview/{table_id}', summary="预览代码", description="预览代码")
async def preview_code(
    table_id: int,
    auth: AuthSchema = Depends(AuthPermission(permissions=["tool:gen:preview"]))
):
    preview_code_result = await GenTableService.preview_code_services(auth, table_id)
    logger.info('预览代码成功')
    return SuccessResponse(data=preview_code_result, msg="预览代码成功")


@genController.get('/synchDb/{table_name}', summary="同步数据库", description="同步数据库")
async def sync_db(
    table_name: str,
    auth: AuthSchema = Depends(AuthPermission(permissions=["tool:gen:edit"]))
):
    result = await GenTableService.sync_db_services(auth, table_name)
    logger.info('同步数据库成功')
    return result