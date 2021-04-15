from pydantic import BaseSettings

class BBPortfolioSettings(BaseSettings):
    REDIS_HOST: str = 'localhost'
    FLASK_SECRET_KEY: str = ''
    BB_DATABASE_DSN: str = 'BBSQLMSSQLServerDatabase'
    BB_DATABASE: str = 'BBLEARN'
    BB_DATABASE_USER: str = 'user'
    BB_DATABASE_PASSWORD: str = ''

    class Config:
        env_file = '.env'


config = BBPortfolioSettings()
