from pydantic_settings import BaseSettings


class Config(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_NAME: str
    SECURITY_KEY: str = "709cb22f047a59f492c4d6407e627240e2272bda11ab791c16fb4f4661f7285a95ba6efbc1bbf762cddcc3710a1487f4a3242f21b2d9cd751b3154a452c5a286"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    @property
    def database_connection_url(self):
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_NAME}"


config = Config()
