import nextcord
import requests as req
import os


class Api:
    def __init__(self):
        self.api = os.getenv("api.url")
        self.client = None  # Client will be set later

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
                r = req.get(f"{self.api}/guilds/{guild_id}")
                return r.json()["prefix"] if r.status_code == 200 else default_prefix

        return default_prefix

    def get_command(self, message=None, *args, **kwargs):
        """
        Get the command from the message
        """
        # api route is self.api/guilds/{guild_id}/commands
        # result is json list
        # search in json list for the trigger with the message content. Has to be exact match
        # send the ['response']

        if message and hasattr(message, "channel"):
            if message.guild is not None:
                guild_id = message.guild.id
                r = req.get(f"{self.api}/guilds/{guild_id}/commands")
                if r.status_code == 200:
                    commands = r.json()
                    for command in commands:
                        if message.content == command["trigger"]:
                            return command
        return None