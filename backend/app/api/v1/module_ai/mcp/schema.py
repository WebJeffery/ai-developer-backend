# -*- coding: utf-8 -*-

from pydantic import BaseModel, Field
from typing import Optional


class ChatQuerySchema(BaseModel):
    """聊天查询模型"""
    message: str = Field(..., min_length=1, max_length=4000, description="聊天消息", example="你好，你能帮我什么？")
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "你好，你能帮我什么？"
            }
        }