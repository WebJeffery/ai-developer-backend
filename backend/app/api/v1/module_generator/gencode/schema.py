# -*- coding:utf-8 -*-

from typing import Any, List, Literal, Optional
from pydantic import BaseModel, ConfigDict, Field, model_validator
from pydantic.alias_generators import to_camel

from app.utils.string_util import StringUtil
from app.common.constant import GenConstant
from app.core.base_schema import BaseSchema


class GenTableOptionModel(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    parent_menu_id: Optional[int] = Field(default=None, description='所属父级分类')
    tree_code: Optional[str] = Field(default=None, description='tree_code')
    tree_name: Optional[str] = Field(default=None, description='tree_name')
    tree_parent_code: Optional[str] = Field(default=None, description='tree_parent_code')

class GenDBTableSchema(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    database_name: Optional[str] = Field(default=None, description='数据库名称')
    table_name: Optional[str] = Field(default=None, description='表名称')
    table_type: Optional[str] = Field(default=None, description='表类型')
    table_comment: Optional[str] = Field(default=None, description='表描述')


class GenTableBaseSchema(BaseModel):
    """
    代码生成业务表创建模型
    """
    model_config = ConfigDict(from_attributes=True)

    table_name: Optional[str] = Field(default=None, description='表名称')
    table_comment: Optional[str] = Field(default=None, description='表描述')
    sub_table_name: Optional[str] = Field(default=None, description='关联子表的表名')
    sub_table_fk_name: Optional[str] = Field(default=None, description='子表关联的外键名')
    class_name: Optional[str] = Field(default=None, description='实体类名称')
    tpl_category: Optional[Literal['crud', 'tree']] = Field(default=None, description='使用的模板（crud单表操作 tree树表操作）')
    tpl_web_type: Optional[str] = Field(default=None, description='前端模板类型（element-ui模版 element-plus模版）')
    package_name: Optional[str] = Field(default=None, description='生成包路径')
    module_name: Optional[str] = Field(default=None, description='生成模块名')
    business_name: Optional[str] = Field(default=None, description='生成业务名')
    function_name: Optional[str] = Field(default=None, description='生成功能名')
    function_author: Optional[str] = Field(default=None, description='生成功能作者')
    gen_type: Optional[Literal['0', '1']] = Field(default=None, description='生成代码方式（0zip压缩包 1自定义路径）')
    gen_path: Optional[str] = Field(default=None, description='生成路径（不填默认项目路径）')
    options: Optional[str] = Field(default=None, description='其它生成选项')
    description: Optional[str] = Field(default=None, description='功能描述')

    params: Optional[Any] = Field(default=None, description='前端传递过来的表附加信息，转换成json字符串后放到options')


class GenTableSchema(GenTableBaseSchema):
    """
    代码生成业务表更新模型
    """
    pk_column: Optional['GenTableColumnSchema'] = Field(default=None, description='主键信息')
    sub_table: Optional['GenTableSchema'] = Field(default=None, description='子表信息')
    columns: Optional[List['GenTableColumnSchema']] = Field(default=None, description='表列信息')
    tree_code: Optional[str] = Field(default=None, description='树编码字段tree_code')
    tree_parent_code: Optional[str] = Field(default=None, description='树父编码字段')
    tree_name: Optional[str] = Field(default=None, description='树名称字段ree_name')
    parent_menu_id: Optional[int] = Field(default=None, description='上级菜单ID字段')
    parent_menu_name: Optional[str] = Field(default=None, description='上级菜单名称字段')
    sub: Optional[bool] = Field(default=None, description='是否为子表')
    tree: Optional[bool] = Field(default=None, description='是否为树表')
    crud: Optional[bool] = Field(default=None, description='是否为单表')

    @model_validator(mode='after')
    def check_some_is(self) -> 'GenTableSchema':
        self.sub = True if self.tpl_category and self.tpl_category == GenConstant.TPL_SUB else False
        self.tree = True if self.tpl_category and self.tpl_category == GenConstant.TPL_TREE else False
        self.crud = True if self.tpl_category and self.tpl_category == GenConstant.TPL_CRUD else False
        return self


class GenTableDeleteSchema(BaseModel):
    """
    删除代码生成业务表模型
    """
    model_config = ConfigDict(alias_generator=to_camel)

    table_ids: str = Field(..., description='需要删除的代码生成业务表ID')


class GenTableColumnSchema(BaseModel):
    """
    代码生成业务表字段创建模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    table_id: Optional[int] = Field(default=None, description='归属表编号')
    column_name: Optional[str] = Field(default=None, description='列名称')
    column_comment: Optional[str] = Field(default=None, description='列描述')
    column_type: Optional[str] = Field(default=None, description='列类型')
    python_type: Optional[str] = Field(default=None, description='PYTHON类型')
    python_field: Optional[str] = Field(default=None, description='PYTHON字段名')
    is_pk: Optional[str] = Field(default=None, description='是否主键（1是）')
    is_increment: Optional[str] = Field(default=None, description='是否自增（1是）')
    is_required: Optional[str] = Field(default=None, description='是否必填（1是）')
    is_unique: Optional[str] = Field(default=None, description='是否唯一（1是）')
    is_insert: Optional[str] = Field(default=None, description='是否为插入字段（1是）')
    is_edit: Optional[str] = Field(default=None, description='是否编辑字段（1是）')
    is_list: Optional[str] = Field(default=None, description='是否列表字段（1是）')
    is_query: Optional[str] = Field(default=None, description='是否查询字段（1是）')
    query_type: Optional[str] = Field(default=None, description='查询方式（等于、不等于、大于、小于、范围）')
    html_type: Optional[str] = Field(default=None, description='显示类型（文本框、文本域、下拉框、复选框、单选框、日期控件）')
    dict_type: Optional[str] = Field(default=None, description='字典类型')
    sort: Optional[int] = Field(default=None, description='排序')
    description: Optional[str] = Field(default=None, description='功能描述')


class GenTableColumnDeleteSchema(BaseModel):
    """
    删除代码生成业务表字段模型
    """
    model_config = ConfigDict(from_attributes=True)

    column_ids: List[int] = Field(..., description='需要删除的代码生成业务表字段ID')