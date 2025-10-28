# -*- coding: utf-8 -*-

from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.core.base_schema import BaseSchema


class DeptCreateSchema(BaseModel):
    """部门创建模型"""
    name: str = Field(..., max_length=40, description="部门名称")
    order: int = Field(default=1, ge=0, description="显示顺序")
    code: Optional[str] = Field(default=None, max_length=60, description="部门编码")
    status: bool = Field(default=True, description="是否启用(True:启用 False:禁用)")
    parent_id: Optional[int] = Field(default=None, ge=0, description="父部门ID")
    description: Optional[str] = Field(default=None, max_length=255, description="备注说明")

    @field_validator('name')
    @classmethod
    def validate_name(cls, value: str):
        if not value or len(value.strip()) == 0:
            raise ValueError("部门名称不能为空")
        value = value.replace(" ", "")
        return value

    @field_validator('code')
    @classmethod
    def validate_code(cls, value: Optional[str]):
        if value is None:
            return value
        v = value.strip()
        if v == "":
            return None
        import re
        if not re.match(r'^[A-Za-z][A-Za-z0-9_]*$', v):
            raise ValueError("部门编码必须以字母开头，且仅包含字母/数字/下划线")
        return v

    @model_validator(mode='before')
    @classmethod
    def _normalize(cls, data):
        if isinstance(data, dict):
            for key in ('code', 'description'):
                val = data.get(key)
                if isinstance(val, str):
                    val = val.strip()
                    if key == 'description' and val == '':
                        val = None
                    data[key] = val
            pid = data.get('parent_id')
            if isinstance(pid, str) and pid.strip().isdigit():
                data['parent_id'] = int(pid.strip())
            # status兼容
            status_val = data.get('status')
            if isinstance(status_val, str):
                lowered = status_val.strip().lower()
                if lowered in {'true', '1', 'y', 'yes'}:
                    data['status'] = True
                elif lowered in {'false', '0', 'n', 'no'}:
                    data['status'] = False
            elif isinstance(status_val, int):
                data['status'] = bool(status_val)
        return data


class DeptUpdateSchema(DeptCreateSchema):
    """部门更新模型"""
    ...


class DeptOutSchema(DeptCreateSchema, BaseSchema):
    """部门响应模型"""
    model_config = ConfigDict(from_attributes=True)
    
    parent_name: Optional[str] = Field(default=None, max_length=40, description="父部门名称")
