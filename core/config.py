from pydantic import BaseSettings 
from typing import Optional
from functools import lru_cache

class Settings(BaseSettings):
    DATABASE_USERNAME: str = 'postgres'
    DATABASE_PASSWORD: str = '123123'
    DATABASE_HOST: str = 'localhost'
    DATABASE_NAME: str = 'mydb'

    DATABASE_URI: str = f"postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:5433/{DATABASE_NAME}"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 5
    JWT_SECRET: str = "z8yEpHYQbZn9n9jHmebc9keZHkZWTU5FNqQy72MJeeLHPtMJb66saK85K4Pt6Z54wsSWF9RUmR"
    #Random Password generated on https://passwordsgenerator.net
    ALGORITHM: str = "HS512"

    class Config:
        case_sensitive: bool = True
    
@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()