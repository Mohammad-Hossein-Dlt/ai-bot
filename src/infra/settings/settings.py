from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    
    DOMAIN_URL: str
    
    RUN_PLATFORM: str
    BOT_PLATFORM: str
    
    BOT_TOKEN: str
    
    GPT_TOKEN: str
    GPT_BASE_URL: str
    
    ZARINPAL_MERCHANT_ID: str
    
    DB_STACK: str
    
    MONGO_HOST: str
    MONGO_PORT: int
    MONGO_INITDB_ROOT_USERNAME: str
    MONGO_INITDB_ROOT_PASSWORD: str
    MONGO_INITDB_DATABASE: str
    
    REDIS_HOST: str
    REDIS_PORT: str
    REDIS_PASSWORD: str
    
    JWT: dict

    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file=[
            ".env",
            "../.env",
        ],
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings: Settings = Settings()
