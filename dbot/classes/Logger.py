import logging
from datetime import datetime

class Logger:
    def __init__(self):
        self.logger = logging.getLogger("discord_bot")
        self.logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler(filename=f"dbot/logs/{(datetime.now()).strftime("%d-%m-%Y")}.log", encoding="utf-8", mode="w")
        handler.setFormatter(logging.Formatter(f"{datetime.now().strftime("%H:%M:%S")} - %(levelname)s: %(message)s"))
        self.logger.addHandler(handler)

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)

    def debug(self, message):
        self.logger.debug(message)

    def warning(self, message):
        self.logger.warning(message)
