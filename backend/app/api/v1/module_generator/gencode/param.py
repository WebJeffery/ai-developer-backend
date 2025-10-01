# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Optional
from fastapi import Query

from app.core.validator import DateTimeStr


class GenTableQueryParam:
    """数据库表查询参数"""

    def __init__(
        self,
        table_name: Optional[str] = Query(None, description="表名称"),
        table_comment: Optional[str] = Query(None, description="表注释"),
        creator: Optional[int] = Query(None, description="创建人"),
        start_time: Optional[DateTimeStr] = Query(None, description="开始时间", example="2023-01-01 00:00:00"),
        end_time: Optional[DateTimeStr] = Query(None, description="结束时间", example="2023-12-31 23:59:59"),
    ) -> None:        
        # 存储查询条件，不直接赋值给父类属性
        self.table_name = ("like", table_name)
        self.table_comment = ("like", table_comment)

        # 精确查询字段
        self.creator_id = creator

        # 时间范围查询
        if start_time and end_time:
            start_datetime = datetime.strptime(str(start_time), '%Y-%m-%d %H:%M:%S')
            end_datetime = datetime.strptime(str(end_time), '%Y-%m-%d %H:%M:%S')
            self.created_at = ("between", (start_datetime, end_datetime))


class GenTableColumnQueryParam:
    """数据库表字段查询参数"""

    def __init__(
        self,
        column_name: Optional[str] = Query(None, description="列名称"),
        creator: Optional[int] = Query(None, description="创建人"),
        start_time: Optional[DateTimeStr] = Query(None, description="开始时间", example="2023-01-01 00:00:00"),
        end_time: Optional[DateTimeStr] = Query(None, description="结束时间", example="2023-12-31 23:59:59"),
    ) -> None:        
        # 存储查询条件，不直接赋值给父类属性
        self.column_name = ("like", column_name)

        # 精确查询字段
        self.creator_id = creator

        # 时间范围查询
        if start_time and end_time:
            start_datetime = datetime.strptime(str(start_time), '%Y-%m-%d %H:%M:%S')
            end_datetime = datetime.strptime(str(end_time), '%Y-%m-%d %H:%M:%S')
            self.created_at = ("between", (start_datetime, end_datetime))