from typing import Literal

from pydantic import BaseModel, PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

LOG_DEFAULT_FORMAT = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)


class LoggingConfig(BaseModel):
    log_level: Literal[
        "debug",
        "info",
        "warning",
        "error",
        "critical",
    ] = "info"
    log_format: str = LOG_DEFAULT_FORMAT


class APIV0Prefix(BaseModel):
    pass


class APIPrefix(BaseModel):
    prefix: str = "/api"
    v0: APIV0Prefix = APIV0Prefix()


class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10


class CachingConfig(BaseModel):
    url: RedisDsn


class SecurityConfig(BaseModel):
    key: str
    algorithm: str
    access_token_expires_minutes: int = 30


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    api: APIPrefix = APIPrefix()
    logging: LoggingConfig = LoggingConfig()
    db: DatabaseConfig
    caching: CachingConfig
    security: SecurityConfig


settings = Settings()
