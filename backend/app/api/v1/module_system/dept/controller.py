# -*- coding: utf-8 -*-

from fastapi import APIRouter, Body, Depends, Path, Query
from fastapi.responses import JSONResponse

from app.common.response import SuccessResponse
from app.common.request import PaginationService
from app.core.router_class import OperationLogRoute
from app.core.dependencies import AuthPermission
from app.core.base_schema import BatchSetAvailable
from app.core.logger import logger
from app.core.base_params import PaginationQueryParams
from ..auth.schema import AuthSchema
from .param import DeptQueryParams
from .service import DeptService
from .schema import (
    DeptCreateSchema,
    DeptUpdateSchema
)


DeptRouter = APIRouter(route_class=OperationLogRoute, prefix="/dept", tags=["部门管理"])


@DeptRouter.get("/tree", summary="查询部门树", description="查询部门树")
async def get_dept_tree_controller(
    search: DeptQueryParams = Depends(),
    auth: AuthSchema = Depends(AuthPermission(permissions=["system:dept:query"]))
) -> JSONResponse:
    result_dict_list = await DeptService.get_dept_tree_service(search=search, auth=auth)
    logger.info(f"查询部门树成功")
    return SuccessResponse(data=result_dict_list, msg="查询部门树成功")


@DeptRouter.get("/detail/{id}", summary="查询部门详情", description="查询部门详情")
async def get_obj_detail_controller(
    id: int = Path(..., description="部门ID"),
    auth: AuthSchema = Depends(AuthPermission(permissions=["system:dept:query"]))
) -> JSONResponse:
    result_dict = await DeptService.get_dept_detail_service(id=id, auth=auth)
    logger.info(f"查询部门详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="查询部门详情成功")


@DeptRouter.post("/create", summary="创建部门", description="创建部门")
async def create_obj_controller(
    data: DeptCreateSchema,
    auth: AuthSchema = Depends(AuthPermission(permissions=["system:dept:create"]))
) -> JSONResponse:
    result_dict = await DeptService.create_dept_service(data=data, auth=auth)
    logger.info(f"创建部门成功: {result_dict}")
    return SuccessResponse(data=result_dict, msg="创建部门成功")


@DeptRouter.put("/update/{id}", summary="修改部门", description="修改部门")
async def update_obj_controller(
    data: DeptUpdateSchema,
    id: int = Path(..., description="部门ID"),
    auth: AuthSchema = Depends(AuthPermission(permissions=["system:dept:update"]))
) -> JSONResponse:
    result_dict = await DeptService.update_dept_service(auth=auth, id=id, data=data)
    logger.info(f"修改部门成功: {result_dict}")
    return SuccessResponse(data=result_dict, msg="修改部门成功")


@DeptRouter.delete("/delete", summary="删除部门", description="删除部门")
async def delete_obj_controller(
    ids: list[int] = Body(..., description="ID列表"),
    auth: AuthSchema = Depends(AuthPermission(permissions=["system:dept:delete"]))
) -> JSONResponse:
    await DeptService.delete_dept_service(ids=ids, auth=auth)
    logger.info(f"删除部门成功: {ids}")
    return SuccessResponse(msg="删除部门成功")


@DeptRouter.patch("/available/setting", summary="批量修改部门状态", description="批量修改部门状态")
async def batch_set_available_obj_controller(
    data: BatchSetAvailable,
    auth: AuthSchema = Depends(AuthPermission(permissions=["system:dept:patch"]))
) -> JSONResponse:
    await DeptService.batch_set_available_service(data=data, auth=auth)
    logger.info(f"批量修改部门状态成功: {data.ids}")
    return SuccessResponse(msg="批量修改部门状态成功")
