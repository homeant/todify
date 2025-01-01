import logging

from app.logger import setup_logging

file_path = "./logs/app.log"

setup_logging(file_path)

logging.getLogger(__name__).info("init log success")
