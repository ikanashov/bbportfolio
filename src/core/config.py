import os

from pydantic import BaseSettings


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class BBPortfolioSettings(BaseSettings):
    REDIS_HOST: str = 'localhost'
    FLASK_SECRET_KEY: str = ''
    BB_DATABASE_DSN: str = 'BBSQLMSSQLServerDatabase'
    BB_DATABASE: str = 'BBLEARN'
    BB_DATABASE_USER: str = 'user'
    BB_DATABASE_PASSWORD: str = ''

    class Config:
        # Файл .env должен находится в корне проекта
        env_file = BASE_DIR + '/../.env'


config = BBPortfolioSettings()
