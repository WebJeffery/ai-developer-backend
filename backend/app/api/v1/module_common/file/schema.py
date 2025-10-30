from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from pydantic.alias_generators import to_camel
from typing import Optional


class ImportFieldModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)
    base_column: Optional[str] = Field(description='数据库字段名')
    excel_column: Optional[str] = Field(description='excel字段名', default=None)
    default_value: Optional[str] = Field(description='默认值', default=None)
    is_required: Optional[str] = Field(description='是否必传')
    selected: Optional[bool] = Field(description='是否勾选')

    @model_validator(mode='before')
    @classmethod
    def _normalize(cls, data):
        if isinstance(data, dict):
            for key in ('base_column', 'excel_column', 'default_value'):
                val = data.get(key)
                if isinstance(val, str):
                    val = val.strip()
                    if val == '':
                        val = None
                    data[key] = val
            # is_required 兼容转换
            val = data.get('is_required')
            if isinstance(val, str):
                lowered = val.strip().lower()
                if lowered in {'true', '1', 'y', 'yes'}:
                    data['is_required'] = True
                elif lowered in {'false', '0', 'n', 'no'}:
                    data['is_required'] = False
        return data

    @model_validator(mode='after')
    def _validate(self):
        if self.selected and not (self.base_column and self.base_column.strip()):
            raise ValueError('选中字段必须提供数据库字段名')
        if self.is_required and not (self.excel_column and self.excel_column.strip()):
            raise ValueError('必传字段必须提供excel字段名')
        return self


class ImportModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)
    table_name: Optional[str] = Field(description='表名')
    sheet_name: Optional[str] = Field(description='Sheet名')
    filed_info: Optional[list[ImportFieldModel]] = Field(description='字段关联表')
    file_name: Optional[str] = Field(description='文件名')

    @model_validator(mode='before')
    @classmethod
    def _normalize(cls, data):
        if isinstance(data, dict):
            for key in ('table_name', 'sheet_name', 'file_name'):
                val = data.get(key)
                if isinstance(val, str):
                    val = val.strip()
                    if val == '':
                        val = None
                    data[key] = val
        return data

    @model_validator(mode='after')
    def _validate(self):
        # excel_column 不重复（忽略 None）
        if self.filed_info:
            seen = set()
            for f in self.filed_info:
                if f.excel_column:
                    key = f.excel_column.strip()
                    if key in seen:
                        raise ValueError('excel字段名存在重复')
                    seen.add(key)
        return self

