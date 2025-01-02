import logging

from celery import Celery
from celery.schedules import crontab

from app.config.celery import settings

logger = logging.getLogger(__name__)


def init_celery_app() -> Celery:
    celery_app = Celery(
        "stock_app",
        broker=settings.broker_url,
        backend=settings.backend_url,
        broker_connection_retry_on_startup=True,
        imports={
            "app.tasks.stock_tasks",
            "app.tasks.stock_indicator_task",
            "app.tasks.stock_signal_task",
        },
        worker_cancel_long_running_tasks_on_connection_loss=True,
        worker_redirect_stdouts_level="DEBUG",
        worker_concurrency=4,
        worker_lost_wait=120,
    )

    # 配置定时任务
    celery_app.conf.beat_schedule = {
        "fetch_daily_stock_data": {
            "task": "app.tasks.stock_tasks.fetch_daily_stock_data",
            "schedule": crontab(hour="23", minute="43"),
            # "kwargs": ({"start_date": "20240701", "end_date": "20241229"}),
        },
        # "calculate_indicators_task": {
        #     "task": "app.tasks.stock_indicator_task.calculate_indicators_task",
        #     "schedule": crontab(hour="10", minute="46"),
        #     # "kwargs": ({"start_date": "20240901"}),
        # },
        # "calculate_signals_task": {
        #     "task": "app.tasks.stock_signal_task.calculate_signals_task",
        #     "schedule": crontab(hour="15", minute="01"),
        #     "kwargs": ({"start_date": "20240901"}),
        # },
    }

    # 其他 Celery 配置
    celery_app.conf.update(
        task_serializer="json",
        accept_content=["json"],
        result_serializer="json",
        timezone="Asia/Shanghai",  # 设置时区为上海
        enable_utc=False,
    )
    logger.info(f"{celery_app.conf}")
    return celery_app
