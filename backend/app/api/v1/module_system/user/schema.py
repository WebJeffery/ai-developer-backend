# -*- coding: utf-8 -*-

from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field, EmailStr, field_validator

from app.core.validator import DateTimeStr, mobile_validator
from app.core.base_schema import BaseSchema, CommonSchema


class CurrentUserUpdateSchema(BaseModel):
    """基础用户信息"""
    name: str = Field(..., max_length=32, description="名称")
    mobile: Optional[str] = Field(default=None, description="手机号")
    email: Optional[EmailStr] = Field(default=None, description="邮箱")
    gender: Optional[str] = Field(default=None, description="性别")
    avatar: Optional[str] = Field(default=None, description="头像")

    @field_validator("mobile")
    @classmethod
    def validate_mobile(cls, value: Optional[str]):
        return mobile_validator(value)


class UserRegisterSchema(BaseModel):
    """注册"""
    name: Optional[str] = Field(default=None, max_length=32, description="名称")
    mobile: Optional[str] = Field(default=None, description="手机号")
    username: str = Field(..., max_length=32, description="账号")
    password: str = Field(..., max_length=128, description="密码哈希值")
    role_ids: Optional[List[int]] = Field(default=[2], description='角色ID')
    creator_id: Optional[int] = Field(default=1, description='创建人ID')
    description: Optional[str] = Field(default=f'注册用户{username}', max_length=255, description="备注")

    @field_validator("mobile")
    @classmethod
    def validate_mobile(cls, value: Optional[str]):
        return mobile_validator(value)


class UserForgetPasswordSchema(BaseModel):
    """忘记密码"""
    username: str = Field(..., max_length=32, description="用户名")
    new_password: str = Field(..., max_length=128, description="新密码")
    mobile: Optional[str] = Field(default=None, description="手机号")
    
    @field_validator("mobile")
    @classmethod
    def validate_mobile(cls, value: Optional[str]):
        return mobile_validator(value)


class UserChangePasswordSchema(BaseModel):
    """修改密码"""
    old_password: str = Field(..., max_length=128, description="旧密码")
    new_password: str = Field(..., max_length=128, description="新密码")


class ResetPasswordSchema(BaseModel):
    """重置密码"""
    id: int = Field(..., description="主键ID")
    password: str = Field(..., min_length=6, max_length=128, description="新密码")


class UserCreateSchema(CurrentUserUpdateSchema):
    """新增"""
    model_config = ConfigDict(from_attributes=True)
    
    username: str = Field(..., max_length=32, description="用户名")
    password: str = Field(..., max_length=128, description="密码哈希值")
    status: bool = Field(default=True, description="是否可用")
    is_superuser: bool = Field(default=False, description="是否超管")
    description: Optional[str] = Field(None, max_length=255, description="备注")
    
    dept_id: Optional[int] = Field(default=None, description='部门ID')
    role_ids: Optional[List[int]] = Field(default=[], description='角色ID')
    position_ids: Optional[List[int]] = Field(default=[], description='岗位ID')


class UserUpdateSchema(UserCreateSchema):
    """更新"""
    model_config = ConfigDict(from_attributes=True, exclude={"password"})

    id: int = Field(..., description="主键ID")


class UserOutSchema(UserCreateSchema, BaseSchema):
    """响应"""
    model_config = ConfigDict(arbitrary_types_allowed=True, from_attributes=True)
    
    password: str = Field(exclude=True)  # password 不返回
    last_login: Optional[DateTimeStr] = Field(default=None, description="最后登录时间")
    dept_name: Optional[str] = Field(default=None, description='部门名称')
    dept: Optional[CommonSchema] = Field(default=None, description='部门')
    roles: Optional[List[CommonSchema]] = Field(default=[], description='角色')
    positions: Optional[List[CommonSchema]] = Field(default=[], description='岗位')
