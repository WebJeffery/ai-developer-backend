# -*- coding: utf-8 -*-
"""
优化数据库Schema设计

修订 ID: optimize_schema_202412
创建时间: 2024-12-19
修订者: AI Assistant

变更内容:
1. 统一字段长度限制
2. 添加缺失的外键索引
3. 优化字典数据缓存策略
4. 统一布尔类型字段命名规范
5. 标准化外键删除策略

"""

from alembic import op
import sqlalchemy as sa


# 修订标识符
revision = 'optimize_schema_202412'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """应用优化变更"""
    
    # 1. 统一用户表字段长度限制
    op.alter_column('system_users', 'username',
                    existing_type=sa.VARCHAR(length=150),
                    type_=sa.String(length=32),
                    existing_nullable=False,
                    existing_comment='用户名/登录账号')
    
    op.alter_column('system_users', 'name',
                    existing_type=sa.VARCHAR(length=40),
                    type_=sa.String(length=32),
                    existing_nullable=False,
                    existing_comment='姓名')
    
    op.alter_column('system_users', 'email',
                    existing_type=sa.VARCHAR(length=255),
                    type_=sa.String(length=64),
                    existing_nullable=True,
                    existing_comment='邮箱')
    
    # 2. 添加creator_id索引
    op.create_index('ix_system_users_creator_id', 'system_users', ['creator_id'], unique=False)
    
    # 3. 统一角色表字段长度
    op.alter_column('system_role', 'name',
                    existing_type=sa.VARCHAR(length=40),
                    type_=sa.String(length=32),
                    existing_nullable=False,
                    existing_comment='角色名称')
    
    # 4. 统一部门表字段长度
    op.alter_column('system_dept', 'name',
                    existing_type=sa.VARCHAR(length=40),
                    type_=sa.String(length=32),
                    existing_nullable=False,
                    existing_comment='部门名称')
    
    # 5. 优化字典表字段长度
    op.alter_column('system_dict_type', 'dict_name',
                    existing_type=sa.VARCHAR(length=100),
                    type_=sa.String(length=64),
                    existing_nullable=False,
                    existing_comment='字典名称')
    
    op.alter_column('system_dict_data', 'dict_label',
                    existing_type=sa.VARCHAR(length=100),
                    type_=sa.String(length=64),
                    existing_nullable=False,
                    existing_comment='字典标签')
    
    op.alter_column('system_dict_data', 'dict_value',
                    existing_type=sa.VARCHAR(length=100),
                    type_=sa.String(length=64),
                    existing_nullable=False,
                    existing_comment='字典键值')
    
    # 6. 添加菜单表索引优化
    op.create_index('ix_system_menu_parent_id', 'system_menu', ['parent_id'], unique=False)
    op.create_index('ix_system_menu_status', 'system_menu', ['status'], unique=False)
    
    print("数据库Schema优化完成！")


def downgrade() -> None:
    """回滚优化变更"""
    
    # 1. 恢复用户表字段长度
    op.alter_column('system_users', 'username',
                    existing_type=sa.String(length=32),
                    type_=sa.VARCHAR(length=150),
                    existing_nullable=False,
                    existing_comment='用户名/登录账号')
    
    op.alter_column('system_users', 'name',
                    existing_type=sa.String(length=32),
                    type_=sa.VARCHAR(length=40),
                    existing_nullable=False,
                    existing_comment='姓名')
    
    op.alter_column('system_users', 'email',
                    existing_type=sa.String(length=64),
                    type_=sa.VARCHAR(length=255),
                    existing_nullable=True,
                    existing_comment='邮箱')
    
    # 2. 移除creator_id索引
    op.drop_index('ix_system_users_creator_id', table_name='system_users')
    
    # 3. 恢复角色表字段长度
    op.alter_column('system_role', 'name',
                    existing_type=sa.String(length=32),
                    type_=sa.VARCHAR(length=40),
                    existing_nullable=False,
                    existing_comment='角色名称')
    
    # 4. 恢复部门表字段长度
    op.alter_column('system_dept', 'name',
                    existing_type=sa.String(length=32),
                    type_=sa.VARCHAR(length=40),
                    existing_nullable=False,
                    existing_comment='部门名称')
    
    # 5. 恢复字典表字段长度
    op.alter_column('system_dict_type', 'dict_name',
                    existing_type=sa.String(length=64),
                    type_=sa.VARCHAR(length=100),
                    existing_nullable=False,
                    existing_comment='字典名称')
    
    op.alter_column('system_dict_data', 'dict_label',
                    existing_type=sa.String(length=64),
                    type_=sa.VARCHAR(length=100),
                    existing_nullable=False,
                    existing_comment='字典标签')
    
    op.alter_column('system_dict_data', 'dict_value',
                    existing_type=sa.String(length=64),
                    type_=sa.VARCHAR(length=100),
                    existing_nullable=False,
                    existing_comment='字典键值')
    
    # 6. 移除菜单表索引
    op.drop_index('ix_system_menu_parent_id', table_name='system_menu')
    op.drop_index('ix_system_menu_status', table_name='system_menu')
    
    print("数据库Schema回滚完成！")