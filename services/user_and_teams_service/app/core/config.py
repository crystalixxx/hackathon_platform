from typing import Literal

from dotenv import find_dotenv, load_dotenv
from pydantic import BaseModel, PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv(find_dotenv(".env"))

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
    # = PostgresDsn("postgresql+asyncpg://admin:admin@events_service_postgresql:5432/postgres")
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10


class CachingConfig(BaseModel):
    url: RedisDsn
    # = RedisDsn("redis://admin:admin@user_and_teams_service_redis:6379/0")


class SecurityConfig(BaseModel):
    key: str
    # = "aa4b452e967bbfcd5b06e39742d3c4d53c61c49a0354fb682c12373070dc8eac892f09b17d9a261514ebb6daa6f1a25d1d302cc5909e8a3f23c7a29e02a5ab74"
    algorithm: str
    # = "HS256"
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
