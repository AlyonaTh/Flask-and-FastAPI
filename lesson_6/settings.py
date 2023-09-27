from pydantic import BaseSettings


class Setting(BaseSettings):
    DATABASE_URL: str

    class Config:
        env_file = '.env'


settings = Setting()