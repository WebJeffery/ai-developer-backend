# -*- coding: utf-8 -*-

from fastapi import APIRouter, Body, Depends, Path
from fastapi.responses import JSONResponse

from app.common.response import SuccessResponse
from app.common.request import PaginationService
from app.core.router_class import OperationLogRoute
from app.core.base_params import PaginationQueryParams
from app.core.dependencies import AuthPermission
from app.core.logger import logger
from app.api.v1.module_system.auth.schema import AuthSchema
from .param import VersionQueryParams
from .service import VersionService
from .schema import VersionCreateSchema, VersionUpdateSchema


VersionRouter = APIRouter(route_class=OperationLogRoute, prefix="/versions", tags=["版本管理"])


@VersionRouter.get("/detail/{id}", summary="获取版本详情", description="获取版本详情")
async def get_version_detail_controller(
    id: int = Path(..., description="版本ID"),
    auth: AuthSchema = Depends(AuthPermission(permissions=["system:version:query"]))
) -> JSONResponse:
    result_dict = await VersionService.get_version_detail_service(auth=auth, id=id)
    logger.info(f"获取版本详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取版本详情成功")


@VersionRouter.get("/list", summary="查询版本列表", description="查询版本列表")
async def get_version_list_controller(
    page: PaginationQueryParams = Depends(),
    search: VersionQueryParams = Depends(),
    auth: AuthSchema = Depends(AuthPermission(permissions=["system:version:query"]))
) -> JSONResponse:
    result_dict_list = await VersionService.get_version_list_service(auth=auth, search=search, order_by=page.order_by)
    result_dict = await PaginationService.get_page_obj(data_list=result_dict_list, page_no=page.page_no, page_size=page.page_size)
    logger.info("查询版本列表成功")
    return SuccessResponse(data=result_dict, msg="查询版本列表成功")


@VersionRouter.post("/create", summary="创建版本", description="创建版本")
async def create_version_controller(
    data: VersionCreateSchema,
    auth: AuthSchema = Depends(AuthPermission(permissions=["system:version:create"]))
) -> JSONResponse:
    result_dict = await VersionService.create_version_service(auth=auth, data=data)
    logger.info(f"创建版本成功: {result_dict}")
    return SuccessResponse(data=result_dict, msg="创建版本成功")


@VersionRouter.put("/update/{id}", summary="修改版本", description="修改版本")
async def update_version_controller(
    data: VersionUpdateSchema,
    id: int = Path(..., description="版本ID"),
    auth: AuthSchema = Depends(AuthPermission(permissions=["system:version:update"]))
) -> JSONResponse:
    result_dict = await VersionService.update_version_service(auth=auth, id=id, data=data)
    logger.info(f"修改版本成功: {result_dict}")
    return SuccessResponse(data=result_dict, msg="修改版本成功")


@VersionRouter.delete("/delete", summary="删除版本", description="删除版本")
async def delete_version_controller(
    ids: list[int] = Body(..., description="ID列表"),
    auth: AuthSchema = Depends(AuthPermission(permissions=["system:version:delete"]))
) -> JSONResponse:
    await VersionService.delete_version_service(auth=auth, ids=ids)
    logger.info(f"删除版本成功: {ids}")
    return SuccessResponse(msg="删除版本成功")
