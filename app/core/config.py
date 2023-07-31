from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    DEV: bool
    API_V1_PREFIX: str

    class Config:
        env_prefix = "TURING_MACHINE_"


settings = Settings()
