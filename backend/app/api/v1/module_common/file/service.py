# -*- coding: utf-8 -*-

from pathlib import Path
from typing import Dict
from fastapi import UploadFile, BackgroundTasks

from app.core.exceptions import CustomException
from app.core.base_schema import UploadResponseSchema, DownloadFileSchema
from app.utils.upload_util import UploadUtil

class FileService:
    """
    文件管理服务层
    """

    @classmethod
    async def upload_service(cls, base_url: str, file: UploadFile, upload_type: str = 'local') -> Dict:
        """ 上传文件"""
        if not file:
            raise CustomException(msg="请选择要上传的文件")
        if upload_type == 'local':
            filename, filepath, file_url = await UploadUtil.upload_file(file=file, base_url=base_url)
        elif upload_type == 'oss':
            filename, filepath, file_url = await UploadUtil.upload_file_oss(file=file, oss_folder=file.filename)
        else:
            raise CustomException(msg="上传类型错误")
        
        return UploadResponseSchema(
            file_path=f'{filepath}',
            file_name=filename,
            origin_name=file.filename,
            file_url=f'{file_url}',
        ).model_dump()
        

    @classmethod
    async def download_service(cls, file_path: str) -> DownloadFileSchema:
        """
        下载文件
        :param file_path: 文件路径
        :return: 结果
        """
        if not file_path:
            raise CustomException(msg="请选择要下载的文件")
        if not UploadUtil.check_file_exists(file_path):
            raise CustomException(msg="文件不存在")
        file_name = UploadUtil.download_file(file_path)

        return DownloadFileSchema(
            file_path=file_path,
            file_name=str(file_name),
        )