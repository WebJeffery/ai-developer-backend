# -*- coding:utf-8 -*-

from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, Query, Body, Path
from fastapi.responses import StreamingResponse, JSONResponse

from app.common.response import SuccessResponse, ErrorResponse, StreamResponse
from app.core.dependencies import AuthPermission
from app.core.router_class import OperationLogRoute
from app.core.base_params import PaginationQueryParam
from app.common.request import PaginationService
from app.api.v1.module_system.auth.schema import AuthSchema
from app.api.v1.module_system.user.schema import UserOutSchema
from .param import GenTableQueryParam
from .schema import GenTableDeleteSchema, GenTableUpdateSchema, GenTableOutSchema
from .service import GenTableColumnService, GenTableService
from app.utils.common_util import bytes2file_response
from app.core.logger import logger


GenRouter = APIRouter(route_class=OperationLogRoute, prefix='/gencode', tags=["代码生成模块"])


@GenRouter.get("/detail/{table_id}", summary="获取业务表详细信息", description="获取业务表详细信息")
async def get_gen_table_detail_controller(
    table_id: int = Path(..., description="业务表ID"),
    auth: AuthSchema = Depends(AuthPermission(permissions=["generator:gencode:query"]))
) -> JSONResponse:
    gen_table = await GenTableService.get_gen_table_by_id_service(auth, table_id)
    gen_tables = await GenTableService.get_gen_table_all_service(auth)
    gen_columns = await GenTableColumnService.get_gen_table_column_list_by_table_id_service(auth, table_id)
    gen_table_detail_result = dict(info=gen_table, rows=gen_columns, tables=gen_tables)
    logger.info(f'获取table_id为{table_id}的信息成功')
    return SuccessResponse(data=gen_table_detail_result, msg="获取业务表详细信息成功")


@GenRouter.get("/list", summary="查询代码生成业务表列表", description="查询代码生成业务表列表")
async def get_gen_table_list_controller(
    page: PaginationQueryParam = Depends(),
    search: GenTableQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(permissions=["generator:gencode:query"]))
) -> JSONResponse:
    result_dict_list = await GenTableService.get_gen_table_list_service(auth=auth, query_object=search, is_page=False)
    result_dict = await PaginationService.paginate(data_list=result_dict_list["items"], page_no=page.page_no, page_size=page.page_size)
    logger.info('获取代码生成业务表列表成功')
    return SuccessResponse(data=result_dict, msg="获取代码生成业务表列表成功")


@GenRouter.post("/create", summary="创建表结构", description="创建表结构")
async def create_table_controller(
    sql: str = Query(..., description="SQL语句"),
    auth: AuthSchema = Depends(AuthPermission(permissions=["generator:gencode:create"])),
    current_user: UserOutSchema = Depends(lambda auth: auth.user)
) -> JSONResponse:
    result = await GenTableService.create_table_service(auth, sql, current_user)
    logger.info('创建表结构成功')
    return SuccessResponse(msg="创建表结构成功", data=result)


@GenRouter.put("/update/{table_id}", summary="编辑业务表信息", description="编辑业务表信息")
async def update_gen_table_controller(
    table_id: int = Path(..., description="业务表ID"),
    data: GenTableUpdateSchema = Body(..., description="业务表信息"),
    auth: AuthSchema = Depends(AuthPermission(permissions=["generator:gencode:update"])),
    current_user: UserOutSchema = Depends(lambda auth: auth.user)
) -> JSONResponse:
    # 创建一个新的字典来包含所有数据，包括审计字段
    update_data = data.model_dump()
    update_data['update_by'] = current_user.username
    update_data['updated_at'] = datetime.now()
    
    # 创建一个新的GenTableUpdateSchema实例
    updated_data = GenTableUpdateSchema(**update_data)
    
    await GenTableService.validate_edit(updated_data)
    edit_gen_result = await GenTableService.update_gen_table_service(auth, updated_data, table_id)
    logger.info('编辑业务表信息成功')
    return SuccessResponse(data=edit_gen_result, msg="编辑业务表信息成功")


@GenRouter.delete("/delete", summary="删除业务表信息", description="删除业务表信息")
async def delete_gen_table_controller(
    table_ids: str = Body(..., description="ID列表，用逗号分隔"),
    auth: AuthSchema = Depends(AuthPermission(permissions=["generator:gencode:delete"]))
) -> JSONResponse:
    delete_gen_table = GenTableDeleteSchema(table_ids=table_ids)
    result = await GenTableService.delete_gen_table_service(auth, delete_gen_table)
    logger.info('删除业务表信息成功')
    return result


@GenRouter.post("/import", summary="导入表结构", description="导入表结构")
async def import_gen_table_controller(
    tables: List[str] = Body(..., description="表名列表", embed=True),
    auth: AuthSchema = Depends(AuthPermission(permissions=["generator:gencode:import"])),
    current_user: UserOutSchema = Depends(lambda auth: auth.user)
) -> JSONResponse:
    table_names = tables if tables else []
    add_gen_table_list = await GenTableService.get_gen_db_table_list_by_name_service(auth, table_names)
    result = await GenTableService.import_gen_table_service(auth, add_gen_table_list, current_user)
    logger.info('导入表结构成功')
    return result


@GenRouter.patch("/batch/out", summary="批量生成代码", description="批量生成代码")
async def batch_gen_code_controller(
    tables: str = Query(..., description="表名列表，用逗号分隔"),
    auth: AuthSchema = Depends(AuthPermission(permissions=["generator:gencode:operate"]))
) -> StreamResponse:
    table_names = tables.split(',') if tables else []
    batch_gen_code_result = await GenTableService.batch_gen_code_service(auth, table_names)
    logger.info('批量生成代码成功')
    return StreamResponse(
        data=bytes2file_response(batch_gen_code_result),
        media_type='application/zip',
        headers={'Content-Disposition': 'attachment; filename=code.zip'}
    )


@GenRouter.post("/out/path/{table_name}", summary="生成代码到指定路径", description="生成代码到指定路径")
async def gen_code_local_controller(
    table_name: str = Path(..., description="表名"),
    auth: AuthSchema = Depends(AuthPermission(permissions=["generator:gencode:code"]))
) -> JSONResponse:
    from app.config.setting import settings
    if not settings.allow_overwrite:
        logger.error('【系统预设】不允许生成文件覆盖到本地')
        return ErrorResponse(msg='【系统预设】不允许生成文件覆盖到本地')
    result = await GenTableService.generate_code_service(auth, table_name)
    logger.info('生成代码到指定路径成功')
    return SuccessResponse(msg="生成代码到指定路径成功", data=result)


@GenRouter.get("/preview/{table_id}", summary="预览代码", description="预览代码")
async def preview_code_controller(
    table_id: int = Path(..., description="业务表ID"),
    auth: AuthSchema = Depends(AuthPermission(permissions=["generator:gencode:query"]))
) -> JSONResponse:
    preview_code_result = await GenTableService.preview_code_service(auth, table_id)
    logger.info('预览代码成功')
    return SuccessResponse(data=preview_code_result, msg="预览代码成功")


@GenRouter.get("/db/list", summary="查询数据库表列表", description="查询数据库表列表")
async def get_gen_db_table_list_controller(
    page: PaginationQueryParam = Depends(),
    search: GenTableQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(permissions=["generator:dblist:query"]))
) -> JSONResponse:
    result_dict_list = await GenTableService.get_gen_db_table_list_service(auth=auth, search=search, order_by=page.order_by)
    result_dict = await PaginationService.paginate(data_list=result_dict_list, page_no=page.page_no, page_size=page.page_size)
    logger.info('获取数据库表列表成功')
    return SuccessResponse(data=result_dict, msg="获取数据库表列表成功")


@GenRouter.post("/sync/db/{table_name}", summary="同步数据库", description="同步数据库")
async def sync_db_controller(
    table_name: str = Path(..., description="表名"),
    auth: AuthSchema = Depends(AuthPermission(permissions=["generator:db:sync"]))
) -> JSONResponse:
    result = await GenTableService.sync_db_service(auth, table_name)
    logger.info('同步数据库成功')
    return SuccessResponse(msg="同步数据库成功", data=result)
