# -*- coding: utf-8 -*-

from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.core.base_schema import BaseSchema


class DemoCreateSchema(BaseModel):
    """新增模型"""
    name: str = Field(..., max_length=50, description='名称')
    status: bool = Field(True, description="是否启用(True:启用 False:禁用)")
    description: Optional[str] = Field(default=None, max_length=255, description="描述")

    @field_validator('name')
    @classmethod
    def _validate_name(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError('名称不能为空')
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
            # status兼容
            val = data.get('status')
            if isinstance(val, str):
                lowered = val.strip().lower()
                if lowered in {'true', '1', 'y', 'yes'}:
                    data['status'] = True
                elif lowered in {'false', '0', 'n', 'no'}:
                    data['status'] = False
            elif isinstance(val, int):
                data['status'] = bool(val)
        return data

    @model_validator(mode='wrap')
    @classmethod
    def _wrap(cls, data, handler):
        # 进一步处理：压缩名称/描述中的多余空白，并支持更多 status 同义词
        if isinstance(data, dict):
            name = data.get('name')
            if isinstance(name, str):
                data['name'] = ' '.join(name.split())
            status_val = data.get('status')
            if isinstance(status_val, str):
                lowered = status_val.strip().lower()
                if lowered in {'enabled', 'enable', 'on'}:
                    data['status'] = True
                elif lowered in {'disabled', 'disable', 'off'}:
                    data['status'] = False
            desc = data.get('description')
            if isinstance(desc, str):
                data['description'] = ' '.join(desc.split())
        result = handler(data)
        return result

    @model_validator(mode='after')
    def _check_disabled_requires_description(self):
        # 业务示例：禁用时必须填写描述
        if self.status is False and (self.description is None or (isinstance(self.description, str) and self.description.strip() == '')):
            raise ValueError('禁用时必须填写描述')
        return self


class DemoUpdateSchema(DemoCreateSchema):
    """更新模型"""
    ...


class DemoOutSchema(DemoCreateSchema, BaseSchema):
    """响应模型"""
    model_config = ConfigDict(from_attributes=True)
