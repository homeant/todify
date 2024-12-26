from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    database_url: str = "mysql+mysqldb://codly_test:123456@192.168.2.10/codly_test_db"
    jwt_secret: str
    jwt_algorithm: str
    jwt_expire_seconds: int

    dash_scope_api_key: str
    qwen_default_model: str = "qwen2.5-72b-instruct"

    silicon_flow_api_key: str
    silicon_flow_model: str = "deepseek-ai/DeepSeek-V2.5"

    embeddings_model_name: str = "text-embedding-v3"

    qdrant_url: str
    qdrant_api_key: str

    model_config = SettingsConfigDict(
    )


settings = Settings()
