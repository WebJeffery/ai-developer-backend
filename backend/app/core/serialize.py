# -*- coding: utf-8 -*-

from pydantic import BaseModel
from typing import TypeVar, Dict, Any, Type, Generic
from sqlalchemy.orm import DeclarativeBase

ModelType = TypeVar("ModelType", bound=DeclarativeBase)
SchemaType = TypeVar("SchemaType", bound=BaseModel)


class Serialize(Generic[ModelType, SchemaType]):
    """
    序列化工具类，提供模型、Schema和字典之间的转换功能
    """
    
    @classmethod
    def schema_to_model(cls,schema: Type[SchemaType], model: Type[ModelType]) -> ModelType:
        """
        将Pydantic Schema转换为SQLAlchemy模型
        
        Args:
            schema: Pydantic Schema实例
            model: SQLAlchemy模型类
            
        Returns:
            SQLAlchemy模型实例
            
        Raises:
            Exception: 转换过程中可能抛出的异常
        """
        try:
            return model(**cls.model_to_dict(model, schema))
        except Exception as e:
            raise ValueError(f"序列化失败: {str(e)}")

    @classmethod
    def model_to_dict(cls, model: Type[ModelType], schema: Type[SchemaType]) -> Dict[str, Any]:
        """
        将SQLAlchemy模型转换为Pydantic Schema
        
        Args:
            model: SQLAlchemy模型实例
            schema: Pydantic Schema类
            
        Returns:
            包含模型数据的字典
            
        Raises:
            Exception: 转换过程中可能抛出的异常
        """
        try:
            return schema.model_validate(model).model_dump()
        except Exception as e:
            raise ValueError(f"反序列化失败: {str(e)}")

