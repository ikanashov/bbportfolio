from core.config import config as conf
# gunicorn not allowed config https://github.com/benoitc/gunicorn/issues/156


bind = conf.GUNICORN_HOST+':'+str(conf.GUNICORN_PORT)
workers = conf.GUNICORN_WORKERS
loglevel = conf.GUNICORN_LOGLEVEL
accesslog = conf.GUNICORN_ACCESSLOG
access_log_format = conf.GUNICORN_LOGFORMAT
