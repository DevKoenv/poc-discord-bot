import nextcord, requests as req, asyncio, os
from nextcord.ext import commands
from aiohttp import web
from dbot.classes.Api import Api

class Commands(commands.Cog):
    def __init__(self, bot):
        """
        This class is used to update commands for the server.
        """
        self.client = bot
        self.api = os.getenv("api.url")

    @commands.Cog.listener()
    async def on_message(self, message):
        """
        Check if the message is a command for that server with that prefix
        """
        if message.author.bot:
            return
        
        prefix = Api().get_prefix(message)
        if not message.content.startswith(prefix):
            return
        
        command = Api().get_command(message)
        if command:
            await message.channel.send(command["response"])

