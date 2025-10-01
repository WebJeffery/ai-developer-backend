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
    
    @staticmethod
    def schema_to_model(schema: SchemaType, model: Type[ModelType]) -> ModelType:
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
            return model(**schema.model_dump())
        except Exception as e:
            raise ValueError(f"序列化失败: {str(e)}")

    @staticmethod
    def model_to_schema(model: ModelType, schema: Type[SchemaType]) -> SchemaType:
        """
        将SQLAlchemy模型转换为Pydantic Schema
        
        Args:
            model: SQLAlchemy模型实例
            schema: Pydantic Schema类
            
        Returns:
            Pydantic Schema实例
            
        Raises:
            Exception: 转换过程中可能抛出的异常
        """
        try:
            return schema.model_validate(model)
        except Exception as e:
            raise ValueError(f"反序列化失败: {str(e)}")
    
    @staticmethod
    def schema_to_dict(
        schema: SchemaType, 
    ) -> Dict[str, Any]:
        """
        将Pydantic Schema转换为字典
        
        Args:
            schema: Pydantic Schema实例
            include: 包含的字段
            exclude: 排除的字段
            
        Returns:
            包含Schema数据的字典
        """
        return schema.model_dump()