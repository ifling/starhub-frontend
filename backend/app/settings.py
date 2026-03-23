from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+psycopg://postgres:postgres@db:5432/starhub"
    cors_allow_origins: str = "*"

    jwt_secret: str = "change-me-in-production-use-long-random-string"
    jwt_algorithm: str = "HS256"
    jwt_expires_minutes: int = 60 * 24 * 7  # 7 days

    wechat_mp_appid: str = ""
    wechat_mp_secret: str = ""

    qq_mp_appid: str = ""
    qq_mp_secret: str = ""


settings = Settings()

