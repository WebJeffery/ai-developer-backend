# -*- coding: utf-8 -*-

from typing import Any, Optional, List, Tuple, Union
from fastapi import Request, status
from fastapi.exceptions import RequestValidationError, ResponseValidationError
from pydantic_validation_decorator import FieldValidationError
from starlette.responses import JSONResponse
from starlette.exceptions import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from pydantic_core import ErrorDetails
from pydantic import ValidationError

from app.common.constant import RET
from app.common.response import ErrorResponse
from app.core.logger import logger


class CustomException(Exception):
    """自定义异常基类"""

    def __init__(
        self,
        msg: Optional[str] = RET.EXCEPTION.msg,
        code: int = RET.EXCEPTION.code,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        data: Optional[Any] = None,
        success: bool = False
    ) -> None:
        """
        初始化异常
        :param msg: 错误消息
        :param code: 业务状态码
        :param status_code: HTTP状态码
        :param data: 附加数据
        """
        super().__init__(msg)  # 调用父类初始化方法
        self.status_code = status_code
        self.code = code
        self.msg = msg
        self.data = data
        self.success = success

    def __str__(self) -> str:
        """返回异常消息"""
        return self.msg


async def CustomExceptionHandler(request: Request, exc: CustomException) -> JSONResponse:
    """自定义异常处理器"""
    logger.error(f"请求地址: {request.url}, 错误信息: {exc.msg}, 错误详情: {exc.data}")
    return ErrorResponse(msg=exc.msg, code=exc.code, status_code=exc.status_code, data=exc.data)


async def HttpExceptionHandler(request: Request, exc: HTTPException) -> JSONResponse:
    """HTTP异常处理器"""
    logger.error(f"请求地址: {request.url}, 错误详情: {exc.detail}")
    return ErrorResponse(msg=exc.detail, status_code=exc.status_code)


async def ValidationExceptionHandler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """请求参数验证异常处理器"""
    msg:List[ErrorDetails] = custom_convert_errors(exc)

    logger.error(f"请求地址: {request.url}, 错误信息: {msg}, 错误详情: {exc}")
    return ErrorResponse(msg=str(msg), status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, data=exc.body)

async def ResponseValidationHandle(request: Request, exc: ResponseValidationError) -> JSONResponse:
    logger.error(f"请求地址: {request.url}, 错误详情: {exc}")
    return ErrorResponse(msg=str(exc), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, data=exc.body)

async def SQLAlchemyExceptionHandler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
    """数据库异常处理器"""
    error_msg = f'数据库操作失败: {exc}'
    logger.error(f"请求地址: {request.url}, 错误详情: {error_msg}")
    return ErrorResponse(msg=error_msg, status_code=status.HTTP_400_BAD_REQUEST, data=str(exc))


async def ValueExceptionHandler(request: Request, exc: ValueError) -> JSONResponse:
    """值异常处理器"""
    logger.error(f"请求地址: {request.url}, 错误详情: {exc}")
    return ErrorResponse(msg=str(exc))


async def FieldValidationExceptionHandler(request: Request, exc: FieldValidationError) -> JSONResponse:
    """字段验证异常处理器"""
    logger.error(f"请求地址: {request.url}, 错误信息: {exc.message}, 错误详情: {exc}")
    return ErrorResponse(msg=str(exc))


async def AllExceptionHandler(request: Request, exc: Exception) -> JSONResponse:
    """全局异常处理器"""
    logger.error(f"请求地址: {request.url}, 错误详情: {exc}")
    return ErrorResponse(msg='服务器内部错误', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, data=str(exc))

ERROR_MAPPING = {
    "missing": "请求失败，缺少必填项！",
    # 字符串
    "string_pattern_mismatch": "值错误，提交参数不满足正则表达式{pattern}！",
    "string_too_long": "值错误，提交参数长度必须小于等于{max_length}！",
    "string_too_short": "值错误，提交参数长度必须大于等于{min_length}！",
    "string_type": "类型错误，提交参数应该为字符串！",
    # 列表
    "list_type": "类型错误，提交参数应该为列表！",
    # 字典
    "dict_type": "类型错误，提交参数应该为字典！",
    # 集合
    "set_type": "类型错误，提交参数应该为集合！",
    # 元组
    "tuple_type": "类型错误，提交参数应该为元组！",
    # 元素数量
    "too_long": "数量错误，提交参数的元素数量必须小于等于{max_length}！",
    "too_short": "数量错误，提交参数的元素数量必须大于等于{min_length}！",
    # 大小比值
    "less_than_equal": "值错误，提交参数必须小于等于{le}！",
    "greater_than_equal": "值错误，提交参数必须大于等于{ge}！",
    "less_than": "值错误，提交参数必须小于{lt}！",
    "greater_than": "值错误，提交参数必须大于{gt}！",
    # 布尔值
    "bool_type": "类型错误，提交参数应该为布尔值！",
    "bool_parsing": "类型错误，提交参数应该为布尔值！",
    # 字节
    "bytes_type": "类型错误，提交参数应该为字节！",
    "bytes_too_long": "值错误，提交参数长度必须小于等于{max_length}！",
    "bytes_too_short": "值错误，提交参数长度必须大于等于{min_length}！",
    # 整数
    "int_parsing": "类型错误，提交参数应该为整数！",
    "int_type": "类型错误，提交参数应该为整数！",
    # 浮点数
    "float_parsing": "类型错误，提交参数应该为浮点数！",
    "float_type": "类型错误，提交参数应该为浮点数！",
    # 日期时间
    "date_parsing": "类型错误，提交参数应该为日期！",
    "date_type": "类型错误，提交参数应该为日期！",
    "time_parsing": "类型错误，提交参数应该为时间！",
    "time_type": "类型错误，提交参数应该为时间！",
    # 其他
    "literal_error": "值错误，提交参数值在为{expected}中一个！",
    "extra_forbidden": "值错误，提交参数值不在允许范围内！",
}

def custom_convert_errors(e: ValidationError | RequestValidationError) -> List[ErrorDetails]:
    new_errors: List[ErrorDetails] = []
    for error in e.errors():
        error['loc'] = loc_to_dot_sep(error['loc'])
        custom_message = ERROR_MAPPING.get(error['type'])
        if custom_message:
            ctx = error.get('ctx')
            error['msg'] = (
                custom_message.format(**ctx) if ctx else custom_message
            )
        new_errors.append(error)
    return new_errors

def loc_to_dot_sep(loc: Tuple[Union[str, int], ...]) -> str:
    path = ''
    for i, x in enumerate(loc):
        if isinstance(x, str):
            if i > 0:
                path += '.'
            path += x
        elif isinstance(x, int):
            path += f'[{x}]'
        else:
            raise TypeError('Unexpected type')
    return path
