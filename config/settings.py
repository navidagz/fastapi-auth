from pydantic import BaseSettings


class Settings(BaseSettings):
    mongo_url: str
    secret: str

    class Config:
        env_file = ".env"


settings = Settings()
