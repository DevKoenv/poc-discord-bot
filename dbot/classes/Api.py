import nextcord
import requests as req
import os


class Api:
    def __init__(self):
        self.api = os.getenv("api.url")
        self.headers = {"Authorization": f"Bearer {os.getenv('api.key')}"}
        self.client = None 

    def get_prefix(self, message=None, *args, **kwargs):
        """
        Get the prefix for the server
        """
        default_prefix = os.getenv("bot.prefix", "!")

        if message and hasattr(message, "channel"):
            if isinstance(message.channel, nextcord.DMChannel):
                return default_prefix
            elif message.guild is not None:
                guild_id = message.guild.id
                r = req.get(f"{self.api}/guilds/{guild_id}", headers=self.headers)
                return r.json()["prefix"] if r.status_code == 200 else default_prefix

        return default_prefix


    def get_command(self, message=None, prefix=None, *args, **kwargs):
        """
        Get the command from the message
        """

        if message and hasattr(message, "channel"):
            if message.guild is not None:
                guild_id = message.guild.id
                r = req.get(f"{self.api}/guilds/{guild_id}/commands", headers=self.headers)
                if r.status_code == 200:
                    commands = r.json()
                    for command in commands:
                        if message.content[len(prefix):] == command["trigger"]:
                            return command['response']
        return None