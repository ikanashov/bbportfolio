import multiprocessing
import os

from pydantic import BaseSettings


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class BBPortfolioSettings(BaseSettings):
    FLASK_SECRET_KEY: str = ''
    BB_DATABASE_HOST: str = '127.0.0.1'
    BB_DATABASE_DRIVER: str = '{ODBC Driver 17 for SQL Server}'
    BB_DATABASE: str = 'BBLEARN'
    BB_DATABASE_USER: str = 'user'
    BB_DATABASE_PASSWORD: str = ''
    GUNICORN_HOST: str = '127.0.0.1'
    GUNICORN_PORT: int = 8000
    GUNICORN_WORKERS: int = multiprocessing.cpu_count() * 2 + 1
    GUNICORN_LOGLEVEL: str = 'INFO'
    GUNICORN_ACCESSLOG: str = '/logs/portfolio.log'
    GUNICORN_LOGFORMAT: str = '%(h)s %({x-forwarded-for}i)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

    class Config:
        # Файл .env должен находится в корне проекта
        env_file = BASE_DIR + '/../.env'


config = BBPortfolioSettings()
