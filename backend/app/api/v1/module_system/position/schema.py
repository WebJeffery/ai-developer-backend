# -*- coding: utf-8 -*-

from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.core.base_schema import BaseSchema
from app.core.validator import DateTimeStr

class PositionCreateSchema(BaseModel):
    """岗位创建模型"""
    name: str = Field(..., max_length=40, description="岗位名称")
    order: Optional[int] = Field(default=1, ge=1, description='显示排序')
    status: bool = Field(default=True, description="是否启用(True:启用 False:禁用)")
    description: Optional[str] = Field(default=None, max_length=255, description="描述")

    @field_validator('name')
    @classmethod
    def _validate_name(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError('岗位名称不能为空')
        return v

    @model_validator(mode='before')
    @classmethod
    def _normalize(cls, data):
        if isinstance(data, dict):
            for key in ('name', 'description'):
                val = data.get(key)
                if isinstance(val, str):
                    val = val.strip()
                    if key == 'description' and val == '':
                        val = None
                    data[key] = val
            # order字符串转为整数
            order_val = data.get('order')
            if isinstance(order_val, str) and order_val.strip().isdigit():
                data['order'] = int(order_val.strip())
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


class PositionUpdateSchema(PositionCreateSchema):
    """岗位更新模型"""
    ...


class PositionOutSchema(PositionCreateSchema, BaseSchema):
    """岗位信息响应模型"""
    model_config = ConfigDict(from_attributes=True)
    ...
