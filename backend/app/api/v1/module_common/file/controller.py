# -*- coding: utf-8 -*-

from pathlib import Path
from fastapi import APIRouter, BackgroundTasks, Body, Depends, UploadFile, Request
from fastapi.responses import JSONResponse, FileResponse

from app.core.dependencies import AuthPermission
from app.core.router_class import OperationLogRoute
from app.core.logger import logger
from app.common.response import SuccessResponse, UploadFileResponse
from app.utils.upload_util import UploadUtil
from .service import FileService

FileRouter = APIRouter(route_class=OperationLogRoute, prefix="/file", tags=["文件管理"])

@FileRouter.post("/upload", summary="上传文件", description="上传文件",dependencies=[Depends(AuthPermission(["common:file:upload"]))])
async def upload_controller(
    file: UploadFile,
    request: Request,
) -> JSONResponse:
    result_dict = await FileService.upload_service(base_url=str(request.base_url), file=file)
    logger.info(f"上传文件成功 {result_dict}")
    return SuccessResponse(data=result_dict, msg="上传文件成功")

@FileRouter.post("/download", summary="下载文件", description="下载文件", dependencies=[Depends(AuthPermission(["common:file:download"]))])
async def download_controller(
    background_tasks: BackgroundTasks,
    file_path: str = Body(..., description="文件路径"), 
    delete: bool = Body(False, description="是否删除文件"),
) -> FileResponse:
    
    result = await FileService.download_service(file_path=file_path)
    if delete:
        background_tasks.add_task(UploadUtil.delete_file, Path(file_path))
    logger.info(f"下载文件成功")
    return UploadFileResponse(file_path=result.file_path, filename=result.file_name)
