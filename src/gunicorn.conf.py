from core.config import config as conf
# gunicorn not allowed config https://github.com/benoitc/gunicorn/issues/156


bind = conf.GUNICORN_HOST+':'+str(conf.GUNICORN_PORT)
workers = conf.GUNICORN_WORKERS
loglevel = conf.GUNICORN_LOGLEVEL
