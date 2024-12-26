from pydantic_settings import BaseSettings, SettingsConfigDict



class TelegramSettings(BaseSettings):
    """Telegram配置"""

    bot_token: str = ""  # Bot Token
    chat_id: str = ""  # 群组ID

    model_config = SettingsConfigDict(
        env_prefix="telegram_"
    )

settings = TelegramSettings()