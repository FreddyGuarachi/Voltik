from pydantic_settings import BaseSettings, SettingsConfigDict


class Setting(BaseSettings):
    DATABASE_URL: str
    DATABASE_URL_SYNC: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    CORS_ORIGINS: list[str] = ["http://127.0.0.1:5500"]

    model_config = SettingsConfigDict(env_file=".env")


setting = Setting()
