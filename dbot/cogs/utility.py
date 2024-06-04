import os, nextcord
from nextcord.ext import commands
from datetime import datetime


class Utility(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @nextcord.slash_command(name="invite", description="Generates an bot invite")
    async def invite(self, interaction: nextcord.Interaction):
        """
        Link to the bot's invite
        """
        await interaction.response.send_message(
            f"https://discord.com/api/oauth2/authorize?client_id={self.client.user.id}&permissions=8&scope=bot",
            ephemeral=True,
        )

    @nextcord.slash_command(name="dashboard", description="Link to the bot's dashboard")
    async def dashboard(self, interaction: nextcord.Interaction):
        """
        Link to the bot's dashboard
        """
        await interaction.response.send_message(
            os.getenv("dashboard.url"), ephemeral=True
        )

    @nextcord.slash_command(name="help", description="Display's the bot help message")
    async def help(self, interaction: nextcord.Interaction):
        """
        Display's the bot help message
        """
        embed = nextcord.Embed(
            title=self.client.user.display_name,
            url=os.getenv("dashboard.url"),
            timestamp=datetime.now(),
        )

        embed.add_field(name="/help", value="Displays this menu.", inline=False)
        embed.add_field(
            name="/dashboard", value="Display's the URL to the dashboard", inline=False
        )
        embed.add_field(name="/invite", value="Generates an bot invite", inline=False)

        avatar = self.client.user.avatar
        if avatar is None:
            avatar = os.getenv('bot.avatar')
        else:
            avatar = self.client.user.avatar.url

        embed.set_footer(
            text="Want to personalize my features? Head to my online dashboard!",
            icon_url=avatar,
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)

def setup(bot):
    bot.add_cog(Utility(bot))
