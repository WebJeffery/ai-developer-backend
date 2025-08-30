#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time

from dataclasses import dataclass

from backend.common.exception import errors


@dataclass(frozen=True)
class SnowflakeConfig:
    """雪花算法配置类"""

    # 位分配
    WORKER_ID_BITS: int = 5
    DATACENTER_ID_BITS: int = 5
    SEQUENCE_BITS: int = 12

    # 最大值
    MAX_WORKER_ID: int = (1 << WORKER_ID_BITS) - 1  # 31
    MAX_DATACENTER_ID: int = (1 << DATACENTER_ID_BITS) - 1  # 31
    SEQUENCE_MASK: int = (1 << SEQUENCE_BITS) - 1  # 4095

    # 位移偏移
    WORKER_ID_SHIFT: int = SEQUENCE_BITS
    DATACENTER_ID_SHIFT: int = SEQUENCE_BITS + WORKER_ID_BITS
    TIMESTAMP_LEFT_SHIFT: int = SEQUENCE_BITS + WORKER_ID_BITS + DATACENTER_ID_BITS

    # 元年时间戳
    EPOCH: int = 1262275200000

    # 默认值
    DEFAULT_DATACENTER_ID: int = 1
    DEFAULT_WORKER_ID: int = 0
    DEFAULT_SEQUENCE: int = 0

snowflake = Snowflake()
