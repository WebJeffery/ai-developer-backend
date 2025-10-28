# -*- coding: utf-8 -*-

from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.core.base_schema import BaseSchema


class ParamsCreateSchema(BaseModel):
    """配置创建模型"""
    config_name: str = Field(..., max_length=500, description="参数名称")
    config_key: str = Field(..., max_length=500, description="参数键名")
    config_value: Optional[str] = Field(default=None, description="参数键值")
    config_type: bool = Field(default=False, description="系统内置(True:是 False:否)")
    status: bool = Field(default=True, description="状态(True:正常 False:停用)")
    description: Optional[str] = Field(default=None, max_length=500, description="描述")

    @model_validator(mode='before')
    @classmethod
    def _normalize(cls, data):
        """前置归一化：字符串去空格、空串转 None、布尔兼容转换，并规范键为小写。"""
        if isinstance(data, dict):
            for key in ('config_name', 'config_key', 'config_value', 'description'):
                val = data.get(key)
                if isinstance(val, str):
                    val = val.strip()
                    if key in ('config_value', 'description') and val == '':
                        val = None
                    data[key] = val
            # 规范键为小写
            if isinstance(data.get('config_key'), str):
                data['config_key'] = data['config_key'].lower()
            # 规范布尔
            for bkey in ('config_type', 'status'):
                val = data.get(bkey)
                if isinstance(val, str):
                    lowered = val.strip().lower()
                    if lowered in {'true', '1', 'y', 'yes'}:
                        data[bkey] = True
                    elif lowered in {'false', '0', 'n', 'no'}:
                        data[bkey] = False
                elif isinstance(val, int):
                    data[bkey] = bool(val)
        return data

    @field_validator('config_key')
    @classmethod
    def _validate_config_key(cls, v: str) -> str:
        v = v.strip().lower()
        import re
        if not re.match(r'^[a-z][a-z0-9_.-]*$', v):
            raise ValueError('参数键名必须以小写字母开头，仅包含小写字母/数字/_.-')
        return v


class ParamsUpdateSchema(ParamsCreateSchema):
    """配置更新模型"""
    ...


class ParamsOutSchema(ParamsCreateSchema, BaseSchema):
    """配置响应模型"""
    model_config = ConfigDict(from_attributes=True)
