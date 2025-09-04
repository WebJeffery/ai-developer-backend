# -*- coding: utf-8 -*-

from fastapi import APIRouter, Body, Depends, Path, UploadFile
from fastapi.responses import JSONResponse, StreamingResponse
import urllib.parse

from app.common.response import StreamResponse, SuccessResponse
from app.common.request import PaginationService
from app.utils.common_util import bytes2file_response
from app.core.base_params import PaginationQueryParams
from app.core.dependencies import AuthPermission
from app.core.router_class import OperationLogRoute
from app.core.base_schema import BatchSetAvailable
from app.core.logger import logger
from app.api.v1.module_system.auth.schema import AuthSchema
from .param import DemoQueryParams
from .service import DemoService
from .schema import (
    DemoCreateSchema,
    DemoUpdateSchema
)


DemoRouter = APIRouter(route_class=OperationLogRoute, prefix="/demo", tags=["示例模块"])

@DemoRouter.get("/detail/{id}", summary="获取示例详情", description="获取示例详情")
async def get_obj_detail_controller(
    id: int = Path(..., description="示例ID"),
    auth: AuthSchema = Depends(AuthPermission(permissions=["demo:example:query"]))
) -> JSONResponse:
    result_dict = await DemoService.get_demo_detail_service(id=id, auth=auth)
    logger.info(f"获取示例详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取示例详情成功")

@DemoRouter.get("/list", summary="查询示例列表", description="查询示例列表")
async def get_obj_list_controller(
    page: PaginationQueryParams = Depends(),
    search: DemoQueryParams = Depends(),
    auth: AuthSchema = Depends(AuthPermission(permissions=["demo:example:query"]))
) -> JSONResponse:
    result_dict_list = await DemoService.get_demo_list_service(auth=auth, search=search, order_by=page.order_by)
    result_dict = await PaginationService.get_page_obj(data_list= result_dict_list, page_no= page.page_no, page_size = page.page_size)
    logger.info(f"查询示例列表成功")
    return SuccessResponse(data=result_dict, msg="查询公告列表成功")

@DemoRouter.post("/create", summary="创建示例", description="创建示例")
async def create_obj_controller(
    data: DemoCreateSchema,
    auth: AuthSchema = Depends(AuthPermission(permissions=["demo:example:create"]))
) -> JSONResponse:
    result_dict = await DemoService.create_demo_service(auth=auth, data=data)
    logger.info(f"创建示例成功: {result_dict}")
    return SuccessResponse(data=result_dict, msg="创建示例成功")

@DemoRouter.put("/update/{id}", summary="修改示例", description="修改示例")
async def update_obj_controller(
    data: DemoUpdateSchema,
    id: int = Path(..., description="示例ID"),
    auth: AuthSchema = Depends(AuthPermission(permissions=["demo:example:update"]))
) -> JSONResponse:
    result_dict = await DemoService.update_demo_service(auth=auth, id=id, data=data)
    logger.info(f"修改示例成功: {result_dict}")
    return SuccessResponse(data=result_dict, msg="修改示例成功")

@DemoRouter.delete("/delete", summary="删除示例", description="删除示例")
async def delete_obj_controller(
    ids: list[int] = Body(..., description="ID列表"),
    auth: AuthSchema = Depends(AuthPermission(permissions=["demo:example:delete"]))
) -> JSONResponse:
    await DemoService.delete_demo_service(auth=auth, ids=ids)
    logger.info(f"删除示例成功: {ids}")
    return SuccessResponse(msg="删除示例成功")

@DemoRouter.patch("/available/setting", summary="批量修改示例状态", description="批量修改示例状态")
async def batch_set_available_obj_controller(
    data: BatchSetAvailable,
    auth: AuthSchema = Depends(AuthPermission(permissions=["demo:example:patch"]))
) -> JSONResponse:
    await DemoService.set_demo_available_service(auth=auth, data=data)
    logger.info(f"批量修改示例状态成功: {data.ids}")
    return SuccessResponse(msg="批量修改示例状态成功")

@DemoRouter.post('/export', summary="导出示例", description="导出示例")
async def export_obj_list_controller(
    search: DemoQueryParams = Depends(),
    auth: AuthSchema = Depends(AuthPermission(permissions=["demo:example:export"]))
) -> StreamingResponse:
    # 获取全量数据
    result_dict_list = await DemoService.get_demo_list_service(search=search, auth=auth)
    export_result = await DemoService.batch_export_service(obj_list=result_dict_list)
    logger.info('导出示例成功')

    return StreamResponse(
        data=bytes2file_response(export_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers = {
            'Content-Disposition': 'attachment; filename=example.xlsx'
        }
    )

@DemoRouter.post('/import', summary="导入示例", description="导入示例")
async def import_obj_list_controller(
    file: UploadFile,
    auth: AuthSchema = Depends(AuthPermission(permissions=["demo:example:import"]))
) -> JSONResponse:
    batch_import_result = await DemoService.batch_import_service(file=file, auth=auth, update_support=True)
    logger.info(f"导入示例成功: {batch_import_result}")
    return SuccessResponse(data=batch_import_result, msg="导入示例成功")

@DemoRouter.post('/download/template', summary="获取示例导入模板", description="获取示例导入模板", dependencies=[Depends(AuthPermission(permissions=["demo:example:download"]))])
async def export_obj_template_controller()-> StreamingResponse:
    example_import_template_result = await DemoService.import_template_download_service()
    logger.info('获取示例导入模板成功')

    return StreamResponse(
        data=bytes2file_response(example_import_template_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers = {
            'Content-Disposition': f'attachment; filename={urllib.parse.quote("示例导入模板.xlsx")}',
            'Access-Control-Expose-Headers': 'Content-Disposition'
        }
    )