import nextcord
from nextcord.ext import commands
from dbot.classes.Api import Api

class Prefix(commands.Cog):
    def __init__(self, bot):
        self.client = bot
        self.api = Api.getUrl()

    def get_prefix(self, message):
        """
        Get the prefix for the server
        """
        default_prefix = "!"
        if isinstance(message.channel, nextcord.DMChannel):
            return default_prefix
        else:
            guild_id = message.guild.id
            return self.api.getPrefix(guild_id)
        

    @nextcord.ui.slash_command(
        name="setprefix", description="Set a custom prefix for the server."
    )
    @commands.has_permissions(administrator=True)
    async def setprefix(self, ctx: nextcord.ui.Context, prefix: str):
        """
        Set a custom prefix for the server
        """
        guild_id = ctx.guild.id
        self.api.setPrefix(guild_id, prefix)
        await ctx.send(f"Prefix set to {prefix}")

    async def on_guild_join(self, guild):
        """
        Set the default prefix for the server
        """
        self.api.setPrefix(guild.id, "!")
