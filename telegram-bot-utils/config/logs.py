import datetime
from sys import stderr

from loguru import logger

date_string = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
file_log = 'resources/logs/log_' + date_string


def load_logger(send_to_bot, telegram_enabled, telegram_log_level):
    # LOGGING SETTING
    logger.remove()
    logger.add(stderr, format="<white>{time:HH:mm:ss}</white> | <level>{level: <8}</level> | <cyan>{line}</cyan> - "
                              "<white>{message}</white>")
    logger.add(file_log + f"{datetime.datetime.now().strftime('%Y%m%d')}.log",
               format="<white>{time:HH:mm:ss}</white> | "
                      "<level>{level: <8}</level> | "
                      "<cyan>{line}</cyan> - <white>{"
                      "message}</white>")
    if telegram_enabled:
        logger.add(send_to_bot, level=telegram_log_level)
