# -*- coding: utf-8 -*-

from typing import Any, Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.base_schema import BaseSchema


class DeptCreateSchema(BaseModel):
    """部门创建模型"""
    name: str = Field(..., max_length=40, description="部门名称")
    order: int = Field(default=1, ge=0, description="显示顺序")
    status: bool = Field(default=True, description="是否启用(True:启用 False:禁用)")
    parent_id: Optional[int] = Field(default=None, ge=0, description="父部门ID")
    description: Optional[str] = Field(default=None, max_length=500, description="备注说明")

    @field_validator('name')
    @classmethod
    def validate_name(cls, value: str):
        if not value or len(value.strip()) == 0:
            raise ValueError("部门名称不能为空")
        value = value.replace(" ", "")
        return value


class DeptUpdateSchema(DeptCreateSchema):
    """部门更新模型"""
    id: int = Field(..., ge=1, description="部门ID")


class DeptOutSchema(DeptCreateSchema, BaseSchema):
    """部门响应模型"""
    model_config = ConfigDict(from_attributes=True)
    
    parent_name: Optional[str] = Field(default=None, max_length=40, description="父部门名称")
