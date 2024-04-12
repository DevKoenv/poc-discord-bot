import os, nextcord
from nextcord.ext import commands

class Url(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @nextcord.slash_command()
    async def invite(self, interaction: nextcord.Interaction):
        """
        Link to the bot's invite
        """
        await interaction.response.send_message(f"https://discord.com/api/oauth2/authorize?client_id={self.client.user.id}&permissions=8&scope=bot", ephemeral=True)
        

    @nextcord.slash_command()
    async def dashboard(self, interaction: nextcord.Interaction):
        """
        Link to the bot's dashboard
        """
        await interaction.response.send_message(os.getenv('dashboard.url'), ephemeral=True)


def setup(bot):
    bot.add_cog(Url(bot))