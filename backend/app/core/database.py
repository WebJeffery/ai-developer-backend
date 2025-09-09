# -*- coding: utf-8 -*-

from redis import asyncio as aioredis
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI
from sqlalchemy import create_engine, text, Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
    AsyncEngine
)
from sqlalchemy.exc import (
    OperationalError,
    TimeoutError,
    DisconnectionError,
    InterfaceError,
    ProgrammingError,
    IntegrityError,
    DataError,
    InternalError,
    NotSupportedError,
    InvalidRequestError
)

from app.core.logger import logger
from app.config.setting import settings
from app.core.exceptions import CustomException
from app.core.base_model import MappedBase

# 同步数据库引擎
engine: Engine = create_engine(
    url=settings.DB_URI,
    echo=settings.DATABASE_ECHO,
    pool_pre_ping=settings.POOL_PRE_PING,
    pool_recycle=settings.POOL_RECYCLE,
)
# 同步数据库会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 异步数据库引擎
async_engine: AsyncEngine = create_async_engine(
    url=settings.ASYNC_DB_URI,
    echo=settings.DATABASE_ECHO,
    echo_pool=settings.ECHO_POOL,
    pool_pre_ping=settings.POOL_PRE_PING,
    future=settings.FUTURE,
    pool_recycle=settings.POOL_RECYCLE,
    # pool_size=settings.POOL_SIZE,  # sqlite 不支持
    # max_overflow=settings.MAX_OVERFLOW,  # sqlite 不支持
    # pool_timeout=settings.POOL_TIMEOUT,  # sqlite 不支持
)

# 异步数据库会话工厂
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    autocommit=settings.AUTOCOMMIT,
    autoflush=settings.AUTOFETCH,
    expire_on_commit=settings.EXPIRE_ON_COMMIT,
    class_=AsyncSession
)

def session_connect() -> AsyncSession:
    """获取数据库会话"""
    try:
        if not settings.SQL_DB_ENABLE:
            raise CustomException(msg="请先开启数据库连接", data="请启用 app/config/setting.py: SQL_DB_ENABLE")
        return AsyncSessionLocal()
    except Exception as e:
        raise CustomException(msg=f"数据库连接失败: {e}")

async def init_create_table():
    """
    应用启动时初始化数据库连接

    :return:
    """
    try:
        async with async_engine.begin() as conn:
            await conn.run_sync(MappedBase.metadata.create_all)
        logger.info('数据库连接成功...')
    except Exception as e:
        raise CustomException(msg=f"数据库连接失败: {e}")

async def redis_connect(app: FastAPI, status: bool) -> aioredis.Redis:
    """创建或关闭Redis连接"""
    if not settings.REDIS_ENABLE:
        raise CustomException(msg="请先开启Redis连接", data="请启用 app/core/config.py: REDIS_ENABLE")

    if status:
        try:
            
            rd = await aioredis.from_url(
                url=settings.REDIS_URI,
                encoding='utf-8',
                decode_responses=True,
                health_check_interval=20,
                max_connections=settings.POOL_SIZE,
                socket_timeout=settings.POOL_TIMEOUT
            )
            app.state.redis = rd
            if await rd.ping():
                logger.info("Redis连接成功...")
                return rd
            raise CustomException(msg="Redis连接失败")
        except aioredis.AuthenticationError as e:
            raise aioredis.AuthenticationError(f"Redis认证失败: {e}")
        except aioredis.TimeoutError as e:
            raise aioredis.TimeoutError(f"Redis连接超时: {e}")
        except aioredis.RedisError as e:
            raise aioredis.RedisError(f"Redis连接错误: {e}")
    else:
        await app.state.redis.close()
        logger.info('Redis连接已关闭')

async def mongodb_connect(app: FastAPI, status: bool) -> AsyncIOMotorClient:
    """创建或关闭MongoDB连接"""
    if not settings.MONGO_DB_ENABLE:
        raise CustomException(msg="请先开启MongoDB连接", data="请启用 app/core/config.py: MONGO_DB_ENABLE")

    if status:
        try:
            
            client = AsyncIOMotorClient(
                settings.MONGO_DB_URI,
                maxPoolSize=settings.POOL_SIZE,
                minPoolSize=settings.MAX_OVERFLOW,
                serverSelectionTimeoutMS=settings.POOL_TIMEOUT * 1000
            )
            app.state.mongo_client = client
            app.state.mongo = client[settings.MONGO_DB_NAME]
            data = await client.server_info()
            logger.info("MongoDB连接成功...", data)
            return data
        except Exception as e:
            raise ValueError(f"MongoDB连接失败: {e}")
    else:
        app.state.mongo_client.close()
        logger.info("MongoDB连接已关闭")