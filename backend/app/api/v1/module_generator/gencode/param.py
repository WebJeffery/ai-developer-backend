# -*- coding: utf-8 -*-

from typing import Optional
from fastapi import Query


class GenTableQueryParam:
    """代码生成业务表查询参数"""

    def __init__(
        self,
        table_name: Optional[str] = Query(None, description="表名称"),
        table_comment: Optional[str] = Query(None, description="表注释"),
    ) -> None:
        # 模糊查询字段
        self.table_name = table_name
        self.table_comment = table_comment


class GenTableColumnQueryParam:
    """代码生成业务表字段查询参数"""

    def __init__(
        self,
        column_name: Optional[str] = Query(None, description="列名称"),
    ) -> None:
        # 模糊查询字段
        self.column_name = ("like", column_name)
