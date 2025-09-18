# -*- coding: utf-8 -*-

from fastapi import APIRouter, Body, Depends, Path
from fastapi.responses import JSONResponse

from app.common.response import SuccessResponse
from app.common.request import PaginationService
from app.core.base_params import PaginationQueryParam
from app.core.dependencies import AuthPermission
from app.core.router_class import OperationLogRoute
from app.core.base_schema import BatchSetAvailable
from app.core.logger import logger
from app.api.v1.module_system.auth.schema import AuthSchema
from .param import ApplicationQueryParam
from .service import ApplicationService
from .schema import (
    ApplicationCreateSchema,
    ApplicationUpdateSchema
)


MyAppRouter = APIRouter(route_class=OperationLogRoute, prefix="/application", tags=["应用管理"])

@MyAppRouter.get("/detail/{id}", summary="获取应用详情", description="获取应用详情")
async def get_obj_detail_controller(
    id: int = Path(..., description="应用ID"),
    auth: AuthSchema = Depends(AuthPermission(permissions=["application:myapp:query"]))
) -> JSONResponse:
    result_dict = await ApplicationService.get_application_detail_service(id=id, auth=auth)
    logger.info(f"获取应用详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取应用详情成功")

@MyAppRouter.get("/list", summary="查询应用列表", description="查询应用列表")
async def get_obj_list_controller(
    page: PaginationQueryParam = Depends(),
    search: ApplicationQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(permissions=["application:myapp:query"]))
) -> JSONResponse:
    result_dict_list = await ApplicationService.get_application_list_service(auth=auth, search=search, order_by=page.order_by)
    result_dict = await PaginationService.paginate(data_list=result_dict_list, page_no=page.page_no, page_size=page.page_size)
    logger.info(f"查询应用列表成功")
    return SuccessResponse(data=result_dict, msg="查询应用列表成功")

@MyAppRouter.post("/create", summary="创建应用", description="创建应用")
async def create_obj_controller(
    data: ApplicationCreateSchema,
    auth: AuthSchema = Depends(AuthPermission(permissions=["application:myapp:create"]))
) -> JSONResponse:
    result_dict = await ApplicationService.create_application_service(auth=auth, data=data)
    logger.info(f"创建应用成功: {result_dict}")
    return SuccessResponse(data=result_dict, msg="创建应用成功")

@MyAppRouter.put("/update/{id}", summary="修改应用", description="修改应用")
async def update_obj_controller(
    data: ApplicationUpdateSchema,
    id: int = Path(..., description="应用ID"),
    auth: AuthSchema = Depends(AuthPermission(permissions=["application:myapp:update"]))
) -> JSONResponse:
    result_dict = await ApplicationService.update_application_service(auth=auth, id=id, data=data)
    logger.info(f"修改应用成功: {result_dict}")
    return SuccessResponse(data=result_dict, msg="修改应用成功")

@MyAppRouter.delete("/delete", summary="删除应用", description="删除应用")
async def delete_obj_controller(
    ids: list[int] = Body(..., description="ID列表"),
    auth: AuthSchema = Depends(AuthPermission(permissions=["application:myapp:delete"]))
) -> JSONResponse:
    await ApplicationService.delete_application_service(auth=auth, ids=ids)
    logger.info(f"删除应用成功: {ids}")
    return SuccessResponse(msg="删除应用成功")

@MyAppRouter.patch("/available/setting", summary="批量修改应用状态", description="批量修改应用状态")
async def batch_set_available_obj_controller(
    data: BatchSetAvailable,
    auth: AuthSchema = Depends(AuthPermission(permissions=["application:myapp:patch"]))
) -> JSONResponse:
    await ApplicationService.set_application_available_service(auth=auth, data=data)
    logger.info(f"批量修改应用状态成功: {data.ids}")
    return SuccessResponse(msg="批量修改应用状态成功")