# -*- coding:utf-8 -*-

from sqlalchemy import Boolean, Column, ForeignKey, String, Integer, Text, DateTime

from app.core.base_model import BaseMixin


class FormModel(BaseMixin):
    __tablename__ = "gen_form"

    content = Column(Text, nullable=False, comment='表单代码')

    form_conf = Column(Text, nullable=False, comment='表单配置')

    form_data = Column(Text, nullable=False, comment='表单内容')

    generate_conf = Column(Text, nullable=False, comment='生成配置')

    name = Column(String(255), nullable=False, comment='表单名称')

    drawing_list = Column(Text, nullable=False, comment='字段列表')

