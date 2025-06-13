from pydantic_settings import BaseSettings
from typing import Optional 

class Settings(BaseSettings):
    database_url: str = ''
    
    environment: str = 'dev'
    debug: bool = False

    secret_key: str

    class Config: 
        env_file = '.env'

settings = Settings()