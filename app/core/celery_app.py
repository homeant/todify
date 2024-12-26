from celery import Celery
from celery.schedules import crontab
from app.config.celery import settings


def init_celery_app() -> Celery:
    celery_app = Celery(
        "stock_app",
        broker=settings.broker_url,
        backend=settings.backend_url,
        broker_connection_retry_on_startup=True,
        imports={
            "app.tasks.stock_tasks"
        }
    )

    # 配置定时任务
    celery_app.conf.beat_schedule = {
        'fetch-daily-data': {
            'task': 'app.tasks.stock_tasks.fetch_daily_data_task',
            'schedule': crontab(hour="23", minute="39"),
            "args": (),
        },
        'fetch-lhb-data': {
            'task': 'app.tasks.stock_tasks.fetch_lhb_data_task',
            'schedule': crontab(hour="23", minute="40"),
            "args": (),
        },
        'fetch-block-trade-data': {
            'task': 'app.tasks.stock_tasks.fetch_block_trade_data_task',
            'schedule': crontab(hour="23", minute="41"),
            "args": (),
        },
    }

    # 其他 Celery 配置
    celery_app.conf.update(
        task_serializer='json',
        accept_content=['json'],
        result_serializer='json',
        timezone='Asia/Shanghai',  # 设置时区为上海
        enable_utc=False,
    )
    return celery_app