# -*- coding: utf-8 -*-

from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, field_validator
from pathlib import Path
from enum import Enum


class ResourceType(Enum):
    """资源类型枚举"""
    IMAGE = "image"  # 图片
    VIDEO = "video"  # 视频
    AUDIO = "audio"  # 音频
    DOCUMENT = "document"  # 文档
    ARCHIVE = "archive"  # 压缩包
    OTHER = "other"  # 其他


class ResourceItemSchema(BaseModel):
    """资源项目模型"""
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
    
    name: str = Field(..., description="文件名")
    path: str = Field(..., description="文件路径")
    relative_path: str = Field(..., description="相对路径")
    is_file: bool = Field(..., description="是否为文件")
    is_dir: bool = Field(..., description="是否为目录")
    size: Optional[int] = Field(None, description="文件大小(字节)")
    file_type: Optional[str] = Field(None, description="文件类型")
    file_extension: Optional[str] = Field(None, description="文件扩展名")
    resource_type: Optional[ResourceType] = Field(None, description="资源类型")
    created_time: Optional[datetime] = Field(None, description="创建时间")
    modified_time: Optional[datetime] = Field(None, description="修改时间")
    accessed_time: Optional[datetime] = Field(None, description="访问时间")
    parent_path: Optional[str] = Field(None, description="父目录路径")
    depth: int = Field(0, description="目录深度")
    

class ResourceDirectorySchema(BaseModel):
    """资源目录模型"""
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
    
    path: str = Field(..., description="目录路径")
    name: str = Field(..., description="目录名称")
    items: List[ResourceItemSchema] = Field(default_factory=list, description="目录项")
    total_files: int = Field(0, description="文件总数")
    total_dirs: int = Field(0, description="目录总数")
    total_size: int = Field(0, description="总大小")
    

class ResourceStatsSchema(BaseModel):
    """资源统计模型"""
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
    
    mount_point: str = Field(..., description="挂载点")
    total_files: int = Field(0, description="文件总数")
    total_dirs: int = Field(0, description="目录总数")
    total_size: int = Field(0, description="总大小")
    free_space: int = Field(0, description="可用空间")
    used_space: int = Field(0, description="已用空间")
    total_space: int = Field(0, description="总空间")
    type_stats: Dict[str, int] = Field(default_factory=dict, description="类型统计")
    extension_stats: Dict[str, int] = Field(default_factory=dict, description="扩展名统计")
    

class ResourceSearchSchema(BaseModel):
    """资源搜索模型"""
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
    
    keyword: Optional[str] = Field(None, description="关键词")
    file_type: Optional[str] = Field(None, description="文件类型")
    resource_type: Optional[ResourceType] = Field(None, description="资源类型")
    min_size: Optional[int] = Field(None, description="最小文件大小")
    max_size: Optional[int] = Field(None, description="最大文件大小")
    start_date: Optional[datetime] = Field(None, description="开始日期")
    end_date: Optional[datetime] = Field(None, description="结束日期")
    extensions: Optional[List[str]] = Field(None, description="文件扩展名列表")
    include_hidden: bool = Field(False, description="包含隐藏文件")
    max_depth: int = Field(10, description="最大搜索深度")
    

class ResourceUploadSchema(BaseModel):
    """资源上传响应模型"""
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
    
    filename: str = Field(..., description="文件名")
    file_path: str = Field(..., description="文件路径")
    file_url: str = Field(..., description="访问URL")
    file_size: int = Field(..., description="文件大小")
    resource_type: ResourceType = Field(..., description="资源类型")
    upload_time: datetime = Field(..., description="上传时间")


class ResourceMoveSchema(BaseModel):
    """资源移动模型"""
    source_path: str = Field(..., description="源路径")
    target_path: str = Field(..., description="目标路径")
    overwrite: bool = Field(False, description="是否覆盖")
    
    @field_validator('source_path', 'target_path')
    @classmethod
    def validate_paths(cls, value: str):
        if not value or len(value.strip()) == 0:
            raise ValueError("路径不能为空")
        return value.strip()


class ResourceCopySchema(ResourceMoveSchema):
    """资源复制模型"""
    pass


class ResourceRenameSchema(BaseModel):
    """资源重命名模型"""
    old_path: str = Field(..., description="原路径")
    new_name: str = Field(..., description="新名称")
    
    @field_validator('old_path', 'new_name')
    @classmethod
    def validate_inputs(cls, value: str):
        if not value or len(value.strip()) == 0:
            raise ValueError("参数不能为空")
        return value.strip()


class ResourceCreateDirSchema(BaseModel):
    """创建目录模型"""
    parent_path: str = Field(..., description="父目录路径")
    dir_name: str = Field(..., description="目录名称")
    
    @field_validator('parent_path', 'dir_name')
    @classmethod
    def validate_inputs(cls, value: str):
        if not value or len(value.strip()) == 0:
            raise ValueError("参数不能为空")
        return value.strip()