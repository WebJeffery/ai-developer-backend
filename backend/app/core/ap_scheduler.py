# -*- coding: utf-8 -*-

import json
import importlib
from datetime import datetime
from typing import Union, List, Any, Optional
from asyncio import iscoroutinefunction
from apscheduler.job import Job
from apscheduler.events import JobExecutionEvent, EVENT_ALL, JobEvent
from apscheduler.executors.asyncio import AsyncIOExecutor
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.executors.pool import ProcessPoolExecutor
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.interval import IntervalTrigger
# from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
# from apscheduler.jobstores.mongodb import MongoDBJobStore
# from apscheduler.jobstores.base import JobLookupError, ConflictingIdError
# from apscheduler.schedulers.background import BackgroundScheduler
# from apscheduler.triggers.combining import OrTrigger
# from pymongo import MongoClient

from app.config.setting import settings
from app.core.database import SessionLocal, AsyncSessionLocal
from app.core.exceptions import CustomException
from app.core.logger import logger


job_stores = {
    'default': MemoryJobStore(),
    # 'sqlalchemy': SQLAlchemyJobStore(url=settings.DB_URI, engine=engine), 如果用同一个数据库会有lock冲突
    'redis': RedisJobStore(**dict(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        username=settings.REDIS_USER,
        password=settings.REDIS_PASSWORD,
        db=settings.REDIS_DB_NAME,
    )),
}
# 配置执行器
executors = {
    'default': AsyncIOExecutor(), 
    'processpool': ProcessPoolExecutor(max_workers=1)  # 减少进程数量以减少资源消耗
}
# 配置默认参数
job_defaults = {
    'coalesce': False,  # 是否合并执行
    'max_instances': 1,  # 最大实例数
}
# 配置调度器
scheduler = AsyncIOScheduler()
scheduler.configure(
    jobstores=job_stores, 
    executors=executors, 
    job_defaults=job_defaults,
    timezone='Asia/Shanghai'
)

class SchedulerUtil:
    """
    定时任务相关方法
    """

    @classmethod
    def scheduler_event_listener(cls, event: JobEvent | JobExecutionEvent):
        # 延迟导入避免循环导入
        from app.api.v1.module_application.job.schema import JobLogCreateSchema
        
        # 获取事件类型和任务ID
        event_type = event.__class__.__name__
        # 初始化任务状态
        status = True
        exception_info = ''
        if isinstance(event, JobExecutionEvent) and event.exception:
            exception_info = str(event.exception)
            status = False
        if hasattr(event, 'job_id'):
            job_id = event.job_id
            query_job = cls.get_job(job_id=job_id)
            if query_job:
                query_job_info = query_job.__getstate__()
                # 获取任务名称
                job_name = query_job_info.get('name')
                # 获取任务组名
                job_group = query_job._jobstore_alias
                # # 获取任务执行器
                job_executor = query_job_info.get('executor')
                # 获取调用目标字符串
                invoke_target = query_job_info.get('func')
                # 获取调用函数位置参数
                job_args = ','.join(map(str, query_job_info.get('args', [])))
                # 获取调用函数关键字参数
                job_kwargs = json.dumps(query_job_info.get('kwargs'))
                # 获取任务触发器
                job_trigger = str(query_job_info.get('trigger'))
                # 构造日志消息
                job_message = f"事件类型: {event_type}, 任务ID: {job_id}, 任务名称: {job_name}, 状态: {status}, 任务组: {job_group}, 错误详情: {exception_info}, 执行于{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                job_log = JobLogCreateSchema(
                    job_name=job_name,
                    job_group=job_group,
                    job_executor=job_executor,
                    invoke_target=invoke_target,
                    job_args=job_args,
                    job_kwargs=job_kwargs,
                    job_trigger=job_trigger,
                    job_message=job_message,
                    status=status,
                    exception_info=exception_info,
                    create_time=datetime.now(),
                )
                session = SessionLocal()
                session.add(**job_log.model_dump())
                session.commit()
                session.close()

    @classmethod
    async def init_system_scheduler(cls):
        """
        应用启动时初始化定时任务

        :return:
        """
        # 延迟导入避免循环导入
        from app.api.v1.module_application.job.crud import JobCRUD
        from app.api.v1.module_system.auth.schema import AuthSchema
        
        scheduler.start()
        async with AsyncSessionLocal() as session:
            async with session.begin():
                auth = AuthSchema(db=session)
                job_list = await JobCRUD(auth).get_obj_list_crud()
                for item in job_list:
                    cls.remove_job(job_id=item.id)  # 删除旧任务
                    cls.add_job(item)
        scheduler.add_listener(cls.scheduler_event_listener, EVENT_ALL)

    @classmethod
    async def close_system_scheduler(cls):
        """
        关闭

        :return:
        """
        scheduler.shutdown(wait=False)
        logger.info('关闭定时任务成功')

    @classmethod
    def get_job(cls, job_id: Union[str, int]) -> Optional[Job]:
        """
        获取

        :param job_id: 任务id
        :return: 任务对象
        """
        return scheduler.get_job(job_id=str(job_id))

    @classmethod
    def get_all_jobs(cls) -> List[Job]:
        """
        获取任务列表
        :return: 任务列表
        """
        return scheduler.get_jobs()

    @classmethod
    def add_job(cls, job_info):
        """
        创建
        :param job_info: 任务对象信息
        :return:
        """
        # 动态导入模块
        # 1. 解析调用目标
        # app.module_task.scheduler_test.job
        module_path, func_name = str(job_info.func).rsplit('.', 1)
        module_path = "app.module_task." + module_path
        try:
            module = importlib.import_module(module_path)
            job_func = getattr(module, func_name)
            
            # 2. 确定执行器
            job_executor = job_info.executor
            if iscoroutinefunction(job_func):
                job_executor = 'default'
            if job_info.trigger == 'date':
                trigger = DateTrigger(run_date=job_info.trigger_args)
            elif job_info.trigger == 'interval':
                # 将传入的 interval 表达式拆分为不同的字段
                fields = job_info.trigger_args.strip().split()
                if len(fields) != 5:
                    raise ValueError("无效的 interval 表达式")
                second, minute, hour, day, week = tuple([int(field) if field != '*' else 0 for field in fields])
                # 秒、分、时、天、周（* * * * 1）
                trigger = IntervalTrigger(
                    weeks=week,
                    days=day,
                    hours=hour,
                    minutes=minute,
                    seconds=second,
                    start_date=job_info.start_date,
                    end_date=job_info.end_date,
                    timezone='Asia/Shanghai',
                    jitter=None
                )
            elif job_info.trigger == 'cron':
                # 秒、分、时、天、月、星期几、年 ()
                fields = job_info.trigger_args.strip().split()
                if len(fields) not in (6, 7):
                    raise ValueError("无效的 Cron 表达式")

                parsed_fields = [None if field in ('*', '?') else field for field in fields]
                if len(fields) == 6:
                    parsed_fields.append(None)

                second, minute, hour, day, month, day_of_week, year = tuple(parsed_fields)
                trigger = CronTrigger(
                    second=second,
                    minute=minute,
                    hour=hour,
                    day=day,
                    month=month,
                    day_of_week=day_of_week,
                    year=year,
                    start_date=job_info.start_date,
                    end_date=job_info.end_date,
                    timezone='Asia/Shanghai'
                )
            else:
                raise ValueError("无效的 trigger 触发器")

            # 3. 添加任务
            job = scheduler.add_job(
                func=job_func,  # 直接使用函数对象
                trigger=trigger,
                args=str(job_info.args).split(',') if job_info.args else None,
                kwargs=json.loads(job_info.kwargs) if job_info.kwargs else None,
                id=str(job_info.id),
                name=job_info.name,
                coalesce=job_info.coalesce,
                max_instances=job_info.max_instances,
                jobstore=job_info.jobstore,
                executor=job_executor,
            )
            return job
        except ModuleNotFoundError:
            raise ValueError(f"未找到该模块：{module_path}")
        except AttributeError:
            raise ValueError(f"未找到该模块下的方法：{func_name}")
        except Exception as e:
            raise CustomException(msg=f"添加任务失败: {str(e)}")

    @classmethod
    def remove_job(cls, job_id: Union[str, int]) -> None:
        """
        删除

        :param job_id: 任务id
        :return: None
        """
        query_job = cls.get_job(job_id=str(job_id))
        if query_job:
            scheduler.remove_job(job_id=str(job_id))

    @classmethod
    def clear_jobs(cls):
        """
        删除
        :param job_group: 任务组名
        :return:
        """
        scheduler.remove_all_jobs()

    @classmethod
    def modify_job(cls, job_id: Union[str, int]) -> Job:
        """
        更新（如果是运行中，则是下次次执行生效）
        :param job_id: 任务id
        :return: 更新后的任务对象
        """
        query_job = cls.get_job(job_id=str(job_id)) 
        if not query_job:
            raise CustomException(msg=f"未找到该任务：{job_id}")
        return scheduler.modify_job(job_id=str(job_id))

    @classmethod
    def pause_job(cls, job_id: Union[str, int]):
        """
        暂停（只有状态是运行中时才可以暂停， 已终止不可以）
        :param job_id: 任务id
        :return:
        """
        logger.info(f"开始获取全部任务：{cls.get_all_jobs()}， 状态： {cls.get_job_status()}")
        query_job = cls.get_job(job_id=str(job_id))
        if not query_job:
            raise ValueError(f"未找到该任务：{job_id}")
        scheduler.pause_job(job_id=str(job_id))
        logger.info(f"查看获取全部任务：{cls.get_all_jobs()}， 状态： {cls.get_job_status()}")

    @classmethod
    def resume_job(cls, job_id: Union[str, int]):
        """
        恢复（只有状态是暂停中时才可以恢复， 已终止不可以）
        :param job_id: 任务id
        :return:
        """
        
        logger.info(f"开始获取全部任务：{cls.get_all_jobs()}， 状态： {cls.get_job_status()}")
        query_job = cls.get_job(job_id=str(job_id))
        if not query_job:
            raise ValueError(f"未找到该任务：{job_id}")
        scheduler.resume_job(job_id=str(job_id))
        logger.info(f"查看获取全部任务：{cls.get_all_jobs()}， 状态： {cls.get_job_status()}")

    @classmethod
    def reschedule_job(cls, job_id: Union[str, int]) -> Optional[Job]:
        """
        重启
        :param job_id: 任务id
        :return: 重启后的任务对象
        """
        logger.info(f"开始获取全部任务：{cls.get_all_jobs()}， 状态： {cls.get_job_status()}")
        query_job = cls.get_job(job_id=str(job_id))
        if not query_job:
            raise CustomException(msg=f"未找到该任务：{job_id}")
        scheduler.reschedule_job(job_id=str(job_id))
        logger.info(f"查看获取全部任务：{cls.get_all_jobs()}， 状态： {cls.get_job_status()}")

    @classmethod
    def export_jobs(cls):
        scheduler.export_jobs("/tmp/jobs.json")

    @classmethod
    def import_jobs(cls):
        scheduler.import_jobs("/tmp/jobs.json")

    @classmethod
    def print_jobs(cls,jobstore: Any | None = None, out: Any | None = None):
        """
        打印
        :return:
        """
        scheduler.print_jobs(jobstore=jobstore, out=out)

    @classmethod
    def get_job_status(cls) -> str:
        """
        获取调度器的当前状态
        
        :return: 状态字符串 ('stopped', 'running', 'paused')
        """
        #: constant indicating a scheduler's stopped state
        STATE_STOPPED = 0
        #: constant indicating a scheduler's running state (started and processing jobs)
        STATE_RUNNING = 1
        #: constant indicating a scheduler's paused state (started but not processing jobs)
        STATE_PAUSED = 2
        if scheduler.state == STATE_STOPPED:
            return 'stopped'
        elif scheduler.state == STATE_RUNNING:
            return 'running'
        elif scheduler.state == STATE_PAUSED:
            return 'paused'
        else:
            return 'unknown'