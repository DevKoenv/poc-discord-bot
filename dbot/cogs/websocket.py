import os
import socketio
from nextcord.ext import commands
from dbot.classes.Logger import Logger

class Socket(commands.Cog):
	def __init__(self, bot):
		self.client = bot
		self.logger = Logger()
		self.socket_url = os.getenv("websocket.url")
		self.sio = socketio.AsyncClient()
		self.client.loop.create_task(self.connect_socket())

	async def connect_socket(self):
		try:
			await self.sio.connect(self.socket_url)
			print(f"\nConnected to WebSocket server")
			self.logger.info(f"Connected to WebSocket server at {self.socket_url}")
		except Exception as e:
			print(f"\nFailed to connect to WebSocket server")
			self.logger.error(f"Failed to connect to WebSocket server at {self.socket_url}: {e}")

	async def socket_send(self, message):
		if self.sio.connected:
			try:
				await self.sio.emit('message', message)
				self.logger.debug(f"Message sent to WebSocket server: {message}")
			except Exception as e:
				self.logger.error(f"Failed to send message: {e}")
				await self.connect_socket()

	@commands.Cog.listener()
	async def on_guild_join(self, guild):
		"""
		Send a message to the socket server when the bot joins a guild
		"""
		if self.sio.connected:
			await self.socket_send(f"{self.client.user.name} joined {guild.name}")

	@commands.Cog.listener()
	async def on_guild_remove(self, guild):
		"""
		Send a message to the socket server when the bot leaves a guild
		"""
		if self.sio.connected:
			await self.socket_send(f"{self.client.user.name} left {guild.name}")

	@commands.Cog.listener()
	async def on_guild_update(self, before, after):
		"""
		Send a message to the socket server when a guild is updated
		"""
		if self.sio.connected:
			changes = []

			if before.name != after.name:
				changes.append(f"changed name to {after.name}")
			if before.icon != after.icon:
				changes.append("changed icon")
			if before.banner != after.banner:
				changes.append("changed banner")
			if before.owner != after.owner:
				changes.append("changed owner")

			if changes:
				message = f"{before.name} " + ", ".join(changes)
				await self.socket_send(message)


def setup(bot):
	bot.add_cog(Socket(bot))
