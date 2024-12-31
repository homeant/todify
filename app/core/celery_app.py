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
        imports={"app.tasks.stock_tasks"},
        worker_cancel_long_running_tasks_on_connection_loss=True,
        worker_redirect_stdouts_level="DEBUG",
        worker_concurrency=4,
        worker_lost_wait=120,
    )

    # 配置定时任务
    celery_app.conf.beat_schedule = {
        "fetch-daily-data": {
            "task": "app.tasks.stock_tasks.fetch_daily_stock_data",
            "schedule": crontab(hour="22", minute="45"),
            # "kwargs": ({"start_date": "20240701", "end_date": "20241229"}),
        },
    }

    # 其他 Celery 配置
    celery_app.conf.update(
        task_serializer="json",
        accept_content=["json"],
        result_serializer="json",
        timezone="Asia/Shanghai",  # 设置时区为上海
        enable_utc=False,
    )
    logger.info(f"{celery_app}")
    return celery_app
