from pydantic import BaseSettings


class Settings(BaseSettings):
    database_url: str
    dev: bool

    class Config:
        env_prefix = "TURING_MACHINE_"


settings = Settings()
