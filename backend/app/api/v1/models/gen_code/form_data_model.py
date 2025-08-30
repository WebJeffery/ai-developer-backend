# -*- coding:utf-8 -*-

from sqlalchemy import Boolean, Column, ForeignKey, String, Integer, Text, DateTime
from sqlalchemy.orm import relationship

from app.core.base_model import BaseMixin


class FormData(BaseMixin):
    __tablename__ = "gen_form_data"

    form_data = Column(Text, nullable=False, comment='表单数据')

    form_id = Column(Integer, ForeignKey(SysForm.id), nullable=False, comment='表单ID')

    form_name = Column(String(255), nullable=False, comment='表单名称')


