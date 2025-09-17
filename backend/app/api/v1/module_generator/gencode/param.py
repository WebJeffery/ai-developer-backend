# -*- coding:utf-8 -*-

@as_query
class GenTablePageQuerySchema(GenTableQuerySchema):
    """
    代码生成业务表分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


@as_query
class GenTableColumnPageQuerySchema(GenTableColumnQuerySchema):
    """
    代码生成业务表字段分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')
