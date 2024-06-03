import nextcord, requests as req, asyncio, os
from nextcord.ext import commands
from aiohttp import web


class Prefix(commands.Cog):
    def __init__(self, bot):
        """
        This class is used to set a custom prefix for the server.
        """
        self.client = bot
        self.api = os.getenv("api.url")

    @nextcord.slash_command(
        name="setprefix",
        description="Set a custom prefix for the server.",
        default_member_permissions=nextcord.Permissions(administrator=True),
    )
    async def setprefix(self, interaction: nextcord.Interaction, prefix: str):
        """
        Set a custom prefix for the server
        """
        guild_id = interaction.guild.id
        headers = {"Authorization": f"Bearer {os.getenv('api.key')}"}
        response = req.put(
            f"{self.api}/guilds/{guild_id}", json={"prefix": prefix}, headers=headers
        )

        if response.status_code == 200:
            await interaction.response.send_message(f"Prefix set to {prefix}")
        else:
            await interaction.response.send_message(
                "An error occurred.", ephemeral=True
            )
            print(f"Error setting prefix for guild {guild_id}: {response.status_code}\n{response.text}")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        """
        Set the default prefix for the server
        """
        r = req.put(f"{self.api}/guilds/{guild.id}", json={"prefix": "!"})
        (
            print(
                f"An error occured while setting the default prefix for guild: {guild.name} - {guild.id}."
            )
            if r.status_code != 200
            else None
        )


def setup(bot):
    bot.add_cog(Prefix(bot))
