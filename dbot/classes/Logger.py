import logging, os
from datetime import datetime

class Logger:
	_instance = None

	def __new__(cls):
		if cls._instance is None:
			cls._instance = super(Logger, cls).__new__(cls)
			cls._instance._initialize()
		return cls._instance

	def _initialize(self):
		self.logger = logging.getLogger("discord_bot")
		if not self.logger.handlers:
			self.logger.setLevel(logging.DEBUG)
			if not os.path.exists("dbot/logs"):
				os.makedirs("dbot/logs")
			handler = logging.FileHandler(filename=f"dbot/logs/{datetime.now().strftime('%d-%m-%Y')}.log", encoding="utf-8", mode="a+")
			handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s: %(message)s', datefmt='%H:%M:%S'))
			self.logger.addHandler(handler)

	def info(self, message):
		self.logger.info(message)

	def error(self, message):
		self.logger.error(message)

	def debug(self, message):
		self.logger.debug(message)

	def warning(self, message):
		self.logger.warning(message)
