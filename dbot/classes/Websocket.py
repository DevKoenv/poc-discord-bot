import os
import json
import aiohttp
import asyncio
import socketio
from dbot.classes.Logger import Logger
import nextcord

class Websocket:
    def __init__(self, bot):
        self.client = bot
        self.api = os.getenv("api.url")
        self.websocket_url = os.getenv("websocket.url")
        self.api_key = os.getenv("api.key")
        self.sio = socketio.AsyncClient()
        self.logger = Logger()

    async def start(self):
        """
        Start the WebSocket listener
        """
        self.sio.on('update_command', self.handle_update_command)
        self.sio.on('update_prefix', self.handle_update_prefix)
        try:
            await self.sio.connect(self.websocket_url)
        except:
            self.logger.error("Failed to connect to the WebSocket server")
            activity = nextcord.Activity(type=nextcord.ActivityType.watching, name="Dashboard offline")
            await self.client.change_presence(activity=activity, status=nextcord.Status.dnd)
            await asyncio.sleep(20)
            await self.start()
            return
        self.logger.info("Connected to WebSocket server")

    async def handle_update_command(self, data):
        """
        Handle update command event
        """
        print("update command")
        guild_id = data.get("guild_id")
        if guild_id:
            await self.update_commands_for_guild(guild_id)

    async def handle_update_prefix(self, data):
        """
        Handle update prefix event
        """
        print("update prefix")
        guild_id = data.get("guild_id")
        if guild_id:
            await self.update_prefix_for_guild(guild_id)

    async def update_commands_for_guild(self, guild_id):
        """
        Update commands for a specific guild
        """
        url = f"{self.api}/guilds/{guild_id}/commands"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    commands = await response.json()
                else:
                    self.logger.error(
                        f"Failed to fetch commands for guild {guild_id}: {response.status}"
                    )
                    return

        # Remove all existing commands for the guild
        guild = self.client.get_guild(guild_id)
        if guild:
            for command in list(self.client.commands):
                self.client.remove_command(command.name)

            # Add new commands
            for command_data in commands:

                async def new_command(ctx, *args, command_data=command_data):
                    await ctx.send(command_data["response"])

                new_command.__name__ = command_data["trigger"]
                self.client.command(name=command_data["trigger"])(new_command)

    async def update_prefix_for_guild(self, guild_id):
        """
        Update prefix for a specific guild
        """
        url = f"{self.api}/guilds/{guild_id}"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    guild_data = await response.json()
                    prefix = guild_data["prefix"]
                    self.client.command_prefix = prefix
                    guild = self.client.get_guild(guild_id)
                    if guild:
                        await guild.me.edit(nick=f"{self.client.user.name} | {prefix}")
                else:
                    self.logger.error(
                        f"Failed to fetch guild data for guild {guild_id}: {response.status}"
                    )
