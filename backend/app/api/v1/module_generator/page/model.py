# -*- coding:utf-8 -*-

from sqlalchemy import Boolean, Column, ForeignKey, String, Integer, Text, DateTime

from app.core.base_model import BaseMixin

class PageModel(BaseMixin):
    __tablename__ = "gen_page"
    
    page_name = Column(String(length=255), comment='页面名称')
    
    keywords = Column(String(length=500), comment='页面关键词')
    
    title = Column(String(length=500), comment='页面title标题')
    
