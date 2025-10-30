# -*- coding: utf-8 -*-

from typing import Any, Optional
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError, ResponseValidationError
from pydantic_validation_decorator import FieldValidationError
from starlette.responses import JSONResponse
from starlette.exceptions import HTTPException
from sqlalchemy.exc import SQLAlchemyError

from app.common.constant import RET
from app.common.response import ErrorResponse
from app.core.logger import logger


class CustomException(Exception):
    """自定义异常基类"""

    def __init__(
        self,
        msg: str = RET.EXCEPTION.msg,
        code: int = RET.EXCEPTION.code,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        data: Optional[Any] = None,
        success: bool = False
    ) -> None:
        """
        初始化异常对象。
        
        参数:
        - msg (str): 错误消息。
        - code (int): 业务状态码。
        - status_code (int): HTTP 状态码。
        - data (Any | None): 附加数据。
        - success (bool): 是否成功标记，默认 False。
        
        返回:
        - None
        """
        super().__init__(msg)  # 调用父类初始化方法
        self.status_code = status_code
        self.code = code
        self.msg = msg
        self.data = data
        self.success = success

    def __str__(self) -> str:
        """返回异常消息
        
        返回:
        - str: 异常消息
        """
        return self.msg


def handle_exception(app: FastAPI):
    """
    注册全局异常处理器。
    
    参数:
    - app (FastAPI): 应用实例。
    
    返回:
    - None
    """
    @app.exception_handler(CustomException)
    async def CustomExceptionHandler(request: Request, exc: CustomException) -> JSONResponse:
        """自定义异常处理器
        
        参数:
        - request (Request): 请求对象。
        - exc (CustomException): 自定义异常实例。
        
        返回:
        - JSONResponse: 包含错误信息的 JSON 响应。
        """
        logger.error(f"请求地址: {request.url}, 错误信息: {exc.msg}, 错误详情: {exc.data}")
        return ErrorResponse(msg=exc.msg, code=exc.code, status_code=exc.status_code, data=exc.data)

    @app.exception_handler(HTTPException)
    async def HttpExceptionHandler(request: Request, exc: HTTPException) -> JSONResponse:
        """HTTP异常处理器
        
        参数:
        - request (Request): 请求对象。
        - exc (HTTPException): HTTP异常实例。
        
        返回:
        - JSONResponse: 包含错误信息的 JSON 响应。
        """
        logger.error(f"请求地址: {request.url}, 错误详情: {exc.detail}")
        return ErrorResponse(msg=exc.detail, status_code=exc.status_code)

    @app.exception_handler(RequestValidationError)
    async def ValidationExceptionHandler(request: Request, exc: RequestValidationError) -> JSONResponse:
        """请求参数验证异常处理器
        
        参数:
        - request (Request): 请求对象。
        - exc (RequestValidationError): 请求参数验证异常实例。
        
        返回:
        - JSONResponse: 包含错误信息的 JSON 响应。
        """
        error_mapping = {
            "Field required": "请求失败，缺少必填项！",
            "value is not a valid list": "类型错误，提交参数应该为列表！", 
            "value is not a valid int": "类型错误，提交参数应该为整数！",
            "value could not be parsed to a boolean": "类型错误，提交参数应该为布尔值！",
            "Input should be a valid list": "类型错误，输入应该是一个有效的列表！"
        }
        raw_msg = exc.errors()[0].get('msg')
        msg = error_mapping.get(raw_msg, raw_msg)
        # 去掉Pydantic默认的前缀“Value error”, 仅保留具体提示内容
        if isinstance(msg, str) and msg.startswith("Value error"):
            if "," in msg:
                msg = msg.split(",", 1)[1].strip()
            else:
                msg = msg.replace("Value error", "").strip()
        logger.error(f"请求地址: {request.url}, 错误信息: {msg}, 错误详情: {exc}")
        return ErrorResponse(msg=str(msg), status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, data=exc.body)

    @app.exception_handler(ResponseValidationError)
    async def ResponseValidationHandle(request: Request, exc: ResponseValidationError) -> JSONResponse:
        """响应参数验证异常处理器
        
        参数:
        - request (Request): 请求对象。
        - exc (ResponseValidationError): 响应参数验证异常实例。
        
        返回:
        - JSONResponse: 包含错误信息的 JSON 响应。
        """
        logger.error(f"请求地址: {request.url}, 错误详情: {exc}")
        return ErrorResponse(msg=str(exc), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, data=exc.body)

    @app.exception_handler(SQLAlchemyError)
    async def SQLAlchemyExceptionHandler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
        """数据库异常处理器
        
        参数:
        - request (Request): 请求对象。
        - exc (SQLAlchemyError): 数据库异常实例。
        
        返回:
        - JSONResponse: 包含错误信息的 JSON 响应。
        """
        error_msg = f'数据库操作失败: {exc}'
        logger.error(f"请求地址: {request.url}, 错误详情: {error_msg}")
        return ErrorResponse(msg=error_msg, status_code=status.HTTP_400_BAD_REQUEST, data=str(exc))

    @app.exception_handler(ValueError)
    async def ValueExceptionHandler(request: Request, exc: ValueError) -> JSONResponse:
        """值异常处理器
        
        参数:
        - request (Request): 请求对象。
        - exc (ValueError): 值异常实例。
        
        返回:
        - JSONResponse: 包含错误信息的 JSON 响应。
        """
        logger.error(f"请求地址: {request.url}, 错误详情: {exc}")
        return ErrorResponse(msg=str(exc))

    @app.exception_handler(FieldValidationError)
    async def FieldValidationExceptionHandler(request: Request, exc: FieldValidationError) -> JSONResponse:
        """字段验证异常处理器
        
        参数:
        - request (Request): 请求对象。
        - exc (FieldValidationError): 字段验证异常实例。
        
        返回:
        - JSONResponse: 包含错误信息的 JSON 响应。
        """
        logger.error(f"请求地址: {request.url}, 错误信息: {exc.message}, 错误详情: {exc}")
        return ErrorResponse(msg=str(exc))

    @app.exception_handler(Exception)
    async def AllExceptionHandler(request: Request, exc: Exception) -> JSONResponse:
        """全局异常处理器
        
        参数:
        - request (Request): 请求对象。
        - exc (Exception): 异常实例。
        
        返回:
        - JSONResponse: 包含错误信息的 JSON 响应。
        """
        logger.error(f"请求地址: {request.url}, 错误详情: {exc}")
        return ErrorResponse(msg='服务器内部错误', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, data=str(exc))
