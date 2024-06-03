import nextcord
import requests as req
import os


class Prefix:
    def __init__(self):
        self.api = os.getenv("api.url")
        self.client = None  # Client will be set later

    def get_prefix(self, message):
        """
        Get the prefix for the server
        """
        default_prefix = os.getenv("bot.prefix")
        if isinstance(message.channel, nextcord.DMChannel):
            return default_prefix
        elif message.guild is not None:
            guild_id = message.guild.id
            r = req.get(f"{self.api}/guilds/{guild_id}")
            return r.json()["prefix"] if r.status_code == 200 else default_prefix
        return default_prefix