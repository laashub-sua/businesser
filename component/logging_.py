import logging
import os
from logging.handlers import TimedRotatingFileHandler

logging.basicConfig(
    level=logging.INFO
)


def do_init():
    from __init__ import app

    if not os.path.exists("logs"):
        os.mkdir("logs")
    formatter = logging.Formatter(
        "[%(asctime)s][%(filename)s:%(lineno)d][%(levelname)s][%(thread)d] - %(message)s")
    handler = TimedRotatingFileHandler(
        "logs/flask.log", when="D", interval=1, backupCount=15,
        encoding="UTF-8", delay=False, utc=True)
    app.logger.addHandler(handler)
    handler.setFormatter(formatter)


def info(msg):
    logging.info(msg)
