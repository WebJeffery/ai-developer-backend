# -*- coding: utf-8 -*-
"""
基础模型模块
提供跨数据库兼容的基础模型类和类型装饰器
"""

from datetime import datetime
import re
from typing import Literal, Optional, Dict, Any, Union

from sqlalchemy import Boolean, String, Integer, DateTime, ForeignKey, Text, BigInteger
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, declared_attr, mapped_column, MappedAsDataclass
from sqlalchemy.engine.row import Row
from sqlalchemy.orm.collections import InstrumentedList


class MappedBase(AsyncAttrs, DeclarativeBase):
    """
    声明式基类

    `AsyncAttrs <https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.AsyncAttrs>`__

    `DeclarativeBase <https://docs.sqlalchemy.org/en/20/orm/declarative_config.html>`__

    `mapped_column() <https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column>`__

    兼容 SQLite、MySQL 和 PostgreSQL
    """

    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        """生成表名"""
        return cls.__name__.lower()

    @declared_attr.directive
    def __table_args__(cls) -> dict:
        """表配置"""
        return {'comment': cls.__doc__ or ''}


class ModelMixin(MappedBase):
    """
    基础模型混合类
    """
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment='主键ID')
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True, default=None, comment="备注/描述")
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, default=datetime.now, comment='创建时间')
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    

class CreatorMixin(ModelMixin):
    """
    创建人混合类
    """
    __abstract__ = True

    creator_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, index=True, comment="创建人ID")

    @declared_attr
    def creator(cls) -> Mapped[Optional["UserModel"]]:  # type: ignore
        """创建人关联关系（延迟加载，避免循环依赖）"""
        return relationship(
            "UserModel",
            primaryjoin=f"{cls.__name__}.creator_id == UserModel.id",
            lazy="selectin",
            foreign_keys=lambda: [cls.creator_id],  # type: ignore
            viewonly=True,
            uselist=False  # 明确指定返回单个对象
        )


class SqlalchemyUtil:
    """
    sqlalchemy工具类
    """

    @classmethod
    def base_to_dict(
        cls, obj: Union[MappedBase, Dict], transform_case: Literal['no_case', 'snake_to_camel', 'camel_to_snake'] = 'no_case'
    ) -> dict[str, Any] | dict[Any, Any]:
        """
        将sqlalchemy模型对象转换为字典

        :param obj: sqlalchemy模型对象或普通字典
        :param transform_case: 转换得到的结果形式，可选的有'no_case'(不转换)、'snake_to_camel'(下划线转小驼峰)、'camel_to_snake'(小驼峰转下划线)，默认为'no_case'
        :return: 字典结果
        """
        if isinstance(obj, MappedBase):
            base_dict = obj.__dict__.copy()
            base_dict.pop('_sa_instance_state', None)
            for name, value in base_dict.items():
                if isinstance(value, InstrumentedList):
                    base_dict[name] = cls.serialize_result(value, 'snake_to_camel')
        elif isinstance(obj, dict):
            base_dict = obj.copy()
        if transform_case == 'snake_to_camel':
            return {CamelCaseUtil.snake_to_camel(k): v for k, v in base_dict.items()}
        elif transform_case == 'camel_to_snake':
            return {SnakeCaseUtil.camel_to_snake(k): v for k, v in base_dict.items()}

        return base_dict

    @classmethod
    def serialize_result(
        cls, result: Any, transform_case: Literal['no_case', 'snake_to_camel', 'camel_to_snake'] = 'no_case'
    ) -> Any:
        """
        将sqlalchemy查询结果序列化

        :param result: sqlalchemy查询结果
        :param transform_case: 转换得到的结果形式，可选的有'no_case'(不转换)、'snake_to_camel'(下划线转小驼峰)、'camel_to_snake'(小驼峰转下划线)，默认为'no_case'
        :return: 序列化结果
        """
        if isinstance(result, (MappedBase, dict)):
            return cls.base_to_dict(result, transform_case)
        elif isinstance(result, list):
            return [cls.serialize_result(row, transform_case) for row in result]
        elif isinstance(result, Row):
            if all([isinstance(row, MappedBase) for row in result]):
                return [cls.base_to_dict(row, transform_case) for row in result]
            elif any([isinstance(row, MappedBase) for row in result]):
                return [cls.serialize_result(row, transform_case) for row in result]
            else:
                result_dict = result._asdict()
                if transform_case == 'snake_to_camel':
                    return {CamelCaseUtil.snake_to_camel(k): v for k, v in result_dict.items()}
                elif transform_case == 'camel_to_snake':
                    return {SnakeCaseUtil.camel_to_snake(k): v for k, v in result_dict.items()}
                return result_dict
        return result


class CamelCaseUtil:
    """
    下划线形式(snake_case)转小驼峰形式(camelCase)工具方法
    """

    @classmethod
    def snake_to_camel(cls, snake_str: str) -> str:
        """
        下划线形式字符串(snake_case)转换为小驼峰形式字符串(camelCase)

        :param snake_str: 下划线形式字符串
        :return: 小驼峰形式字符串
        """
        # 分割字符串
        words = snake_str.split('_')
        # 小驼峰命名，第一个词首字母小写，其余词首字母大写
        return words[0] + ''.join(word.capitalize() for word in words[1:])

    @classmethod
    def transform_result(cls, result: Any) -> Any:
        """
        针对不同类型将下划线形式(snake_case)批量转换为小驼峰形式(camelCase)方法

        :param result: 输入数据
        :return: 小驼峰形式结果
        """
        return SqlalchemyUtil.serialize_result(result=result, transform_case='snake_to_camel')


class SnakeCaseUtil:
    """
    小驼峰形式(camelCase)转下划线形式(snake_case)工具方法
    """

    @classmethod
    def camel_to_snake(cls, camel_str: str) -> str:
        """
        小驼峰形式字符串(camelCase)转换为下划线形式字符串(snake_case)

        :param camel_str: 小驼峰形式字符串
        :return: 下划线形式字符串
        """
        # 在大写字母前添加一个下划线，然后将整个字符串转为小写
        words = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', camel_str)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', words).lower()

    @classmethod
    def transform_result(cls, result: Any) -> Any:
        """
        针对不同类型将下划线形式(snake_case)批量转换为小驼峰形式(camelCase)方法

        :param result: 输入数据
        :return: 小驼峰形式结果
        """
        return SqlalchemyUtil.serialize_result(result=result, transform_case='camel_to_snake')