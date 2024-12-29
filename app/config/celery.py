from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # ... 其他配置 ...

    # Celery配置
    broker_url: str
    backend_url: str

    model_config = SettingsConfigDict(env_prefix="celery_")


settings = Settings()
