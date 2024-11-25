from pydantic_settings import BaseSettings


class Config(BaseSettings):
    # POSTGRES_USER: str
    # POSTGRES_PASSWORD: str
    # POSTGRES_HOST: str
    # POSTGRES_PORT: int
    # POSTGRES_NAME: str

    @property
    def database_connection_url(self):
        return "postgresql://"
        # return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_NAME}"


config = Config()
