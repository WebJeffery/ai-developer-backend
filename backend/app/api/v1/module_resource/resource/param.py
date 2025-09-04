# -*- coding: utf-8 -*-

from typing import Optional, List
from pydantic import BaseModel, Field
from enum import Enum


class ResourceType(Enum):
    """资源类型枚举"""
    IMAGE = "image"  # 图片
    VIDEO = "video"  # 视频
    AUDIO = "audio"  # 音频
    DOCUMENT = "document"  # 文档
    ARCHIVE = "archive"  # 压缩包
    OTHER = "other"  # 其他


class ResourceQueryParams(BaseModel):
    """资源查询参数模型"""
    path: Optional[str] = Field(None, description="文件路径")
    keyword: Optional[str] = Field(None, description="关键词搜索")
    resource_type: Optional[ResourceType] = Field(None, description="资源类型")
    file_extension: Optional[str] = Field(None, description="文件扩展名")
    min_size: Optional[int] = Field(None, ge=0, description="最小文件大小")
    max_size: Optional[int] = Field(None, ge=0, description="最大文件大小")
    include_hidden: bool = Field(False, description="包含隐藏文件")
    recursive: bool = Field(True, description="递归搜索")
    max_depth: int = Field(10, description="最大搜索深度")
    sort_by: Optional[str] = Field("name", description="排序字段(name/size/modified_time)")
    sort_order: Optional[str] = Field("asc", description="排序方式(asc/desc)")

    class Config:
        use_enum_values = True