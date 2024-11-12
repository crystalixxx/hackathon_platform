from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    settings_config = SettingsConfigDict(env_prefix="backend_")

    database_connection_url: str = ""


config = Config()
