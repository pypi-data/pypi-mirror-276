from logging import getLogger, getLevelName, Formatter, StreamHandler


logger = getLogger(__name__)
logger.propagate = False
logger.setLevel(getLevelName('DEBUG'))
log_formatter = \
    Formatter("[%(threadName)s] [%(levelname)s] %(funcName)s: "
              "%(message)s")
console_handler = StreamHandler()
console_handler.setFormatter(log_formatter)
logger.addHandler(console_handler)
