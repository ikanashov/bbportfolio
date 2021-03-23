from pydantic import BaseSettings

class BBPortfolioSettings(BaseSettings):
    REDIS_HOST: str = 'localhost'
    FLASK_SECRET_KEY: str = ''
    
    class Config:
        env_file = '.env'


config = BBPortfolioSettings()
