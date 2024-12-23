from pydantic import BaseSettings

class TelegramSettings(BaseSettings):
    """Telegram配置"""
    bot_token: str = ""  # Bot Token
    chat_id: str = ""    # 群组ID
    
    class Config:
        env_prefix = "TELEGRAM_"  # 环境变量前缀 TELEGRAM_BOT_TOKEN 