# -*- coding: utf-8 -*-

from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

from app.core.base_schema import BaseSchema


class ParamsCreateSchema(BaseModel):
    """配置创建模型"""
    config_name: str = Field(..., max_length=500, description="参数名称")
    config_key: str = Field(..., max_length=500, description="参数键名")
    config_value: Optional[str] = Field(default=None, description="参数键值")
    config_type: bool = Field(default=False, description="系统内置(True:是 False:否)")
    status: bool = Field(default=True, description="状态(True:正常 False:停用)")
    description: Optional[str] = Field(default=None, max_length=500, description="描述")


class ParamsUpdateSchema(ParamsCreateSchema):
    """配置更新模型"""
    ...


class ParamsOutSchema(ParamsCreateSchema, BaseSchema):
    """配置响应模型"""
    model_config = ConfigDict(from_attributes=True)
