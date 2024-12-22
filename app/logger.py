import logging
import os
from logging.handlers import TimedRotatingFileHandler

LOG_FORMATTER = "%(asctime)s|%(levelname)s|%(processName)s|%(threadName)s|%(thread)d|%(name)s|%(funcName)s:%(lineno)d|%(message)s"


def setup_logging(
    log_file: str, level: int = logging.INFO, logging_format: str = LOG_FORMATTER
):
    log_dir = os.path.dirname(log_file)
    if os.path.exists(log_dir) is False:
        os.makedirs(log_dir)

    formatter = logging.Formatter(logging_format)

    handler = TimedRotatingFileHandler(
        log_file,
        when="midnight",
        interval=1,
        backupCount=5,
    )

    handler.setFormatter(formatter)
    handler.setLevel(level)

    handlers = [handler]

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(level)
    handlers.append(console_handler)

    # 配置根日志记录器
    logging.basicConfig(level=level, handlers=handlers)
    # 捕获 Uvicorn 日志
    logger = logging.getLogger("app")
    return logger
