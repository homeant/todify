import logging
from typing import Optional

import aiohttp

from app.config.telegram import settings

logger = logging.getLogger(__name__)


class TelegramBot:
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

    async def send_signals(self, signals: list, date: str) -> bool:
        """发送交易信号"""
        try:
            # 按策略分组
            strategy_signals = {}
            for signal in signals:
                if signal.strategy not in strategy_signals:
                    strategy_signals[signal.strategy] = {"buy": [], "sell": []}
                strategy_signals[signal.strategy][signal.signal_type].append(signal)

            # 构建消息
            message = f"📊 {date} 交易信号\n\n"

            for strategy, data in strategy_signals.items():
                message += f"🔸 {strategy}\n"

                # 买入信号
                if data["buy"]:
                    message += "买入:\n"
                    for signal in data["buy"]:
                        message += f"- {signal.code} {signal.name}\n"

                # 卖出信号
                if data["sell"]:
                    message += "卖出:\n"
                    for signal in data["sell"]:
                        message += f"- {signal.code} {signal.name}\n"

                message += "\n"

            # 发送消息
            return await self.send_message(message)

        except Exception as e:
            logger.error(f"发送交易信号异常: {str(e)}")
            return False
