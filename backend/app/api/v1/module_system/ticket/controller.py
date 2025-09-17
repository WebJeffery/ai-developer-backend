# -*- coding: utf-8 -*-

from fastapi import APIRouter, Body, Depends, Path
from fastapi.responses import JSONResponse

from app.common.response import SuccessResponse
from app.common.request import PaginationService
from app.core.router_class import OperationLogRoute
from app.core.base_params import PaginationQueryParam
from app.core.dependencies import AuthPermission
from app.core.logger import logger
from app.api.v1.module_system.auth.schema import AuthSchema
from .param import TicketQueryParam
from .service import TicketService
from .schema import TicketCreateSchema, TicketUpdateSchema


TicketRouter = APIRouter(route_class=OperationLogRoute, prefix="/ticket", tags=["工单管理"])


@TicketRouter.get("/detail/{id}", summary="获取工单详情", description="获取工单详情")
async def get_ticket_detail_controller(
    id: int = Path(..., description="工单ID"),
    auth: AuthSchema = Depends(AuthPermission(permissions=["system:ticket:query"]))
) -> JSONResponse:
    result_dict = await TicketService.get_ticket_detail_service(auth=auth, id=id)
    logger.info(f"获取工单详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取工单详情成功")


@TicketRouter.get("/list", summary="查询工单列表", description="查询工单列表")
async def get_ticket_list_controller(
    page: PaginationQueryParam = Depends(),
    search: TicketQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(permissions=["system:ticket:query"]))
) -> JSONResponse:
    result_dict_list = await TicketService.get_ticket_list_service(auth=auth, search=search, order_by=page.order_by)
    result_dict = await PaginationService.get_page_obj(data_list=result_dict_list, page_no=page.page_no, page_size=page.page_size)
    logger.info("查询工单列表成功")
    return SuccessResponse(data=result_dict, msg="查询工单列表成功")


@TicketRouter.post("/create", summary="创建工单", description="创建工单")
async def create_ticket_controller(
    data: TicketCreateSchema,
    auth: AuthSchema = Depends(AuthPermission(permissions=["system:ticket:create"]))
) -> JSONResponse:
    result_dict = await TicketService.create_ticket_service(auth=auth, data=data)
    logger.info(f"创建工单成功: {result_dict}")
    return SuccessResponse(data=result_dict, msg="创建工单成功")


@TicketRouter.put("/update/{id}", summary="修改工单", description="修改工单")
async def update_ticket_controller(
    data: TicketUpdateSchema,
    id: int = Path(..., description="工单ID"),
    auth: AuthSchema = Depends(AuthPermission(permissions=["system:ticket:update"]))
) -> JSONResponse:
    result_dict = await TicketService.update_ticket_service(auth=auth, id=id, data=data)
    logger.info(f"修改工单成功: {result_dict}")
    return SuccessResponse(data=result_dict, msg="修改工单成功")


@TicketRouter.delete("/delete", summary="删除工单", description="删除工单")
async def delete_ticket_controller(
    ids: list[int] = Body(..., description="ID列表"),
    auth: AuthSchema = Depends(AuthPermission(permissions=["system:ticket:delete"]))
) -> JSONResponse:
    await TicketService.delete_ticket_service(auth=auth, ids=ids)
    logger.info(f"删除工单成功: {ids}")
    return SuccessResponse(msg="删除工单成功")