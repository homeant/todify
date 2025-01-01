import logging
from typing import Optional

import aiohttp

from app.config.telegram import settings
from app.core.singleton import Singleton

logger = logging.getLogger(__name__)


class TelegramBot(metaclass=Singleton):
    """Telegram机器人"""

    def __init__(self):
        self.settings = settings
        self.api_url = f"https://api.telegram.org/bot{self.settings.bot_token}"

    async def send_message(self, text: str, parse_mode: Optional[str] = "HTML") -> bool:
        """发送消息"""
        try:
            url = f"{self.api_url}/sendMessage"
            data = {
                "chat_id": self.settings.chat_id,
                "text": text,
                "parse_mode": parse_mode,
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=data) as response:
                    if response.status == 200:
                        return True
                    else:
                        logger.error(f"发送Telegram消息失败: {await response.text()}")
                        return False

        except Exception as e:
            logger.error(f"发送Telegram消息异常: {str(e)}")
            return False
