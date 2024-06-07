import nextcord, os, requests as req
from nextcord.ext import commands
from dbot.classes.Logger import Logger


class Guilds(commands.Cog):
	def __init__(self, bot):
		self.client = bot
		self.api = os.getenv("api.url")
		self.headers = {"Authorization": f"Bearer {os.getenv('api.key')}"}
		self.logger = Logger()

	@commands.Cog.listener()
	async def on_guild_join(self, guild):
		"""
		This event is triggered when the bot joins a guild.
		The bot sends a welcome message to the owner of the guild or the bot inviter.
		"""
		welcomeEmbed = nextcord.Embed(
			title=f" Thanks for using {self.client.user.name}!",
			description=f"In order to manage your server on the web dashboard, follow [this link]({os.getenv('dashboard.url')}).",
			color=nextcord.Color.green(),
		)

		owner = guild.owner
		await owner.send(embed=welcomeEmbed)

	@commands.Cog.listener()
	async def on_guild_remove(self, guild):
		"""
		This event is triggered when the bot leaves a guild.
		Removes the guild from the database.
		"""
		pass #TODO: Remove the guild from the database when Koen made the API route

	@commands.Cog.listener()
	async def on_guild_update(self, before, after):
		"""
		This event is triggered when a guild is updated.
		"""
		r = req.put(f"{self.api}/guilds/{after.id}", headers=self.headers)
		if r.status_code != 200:
			self.logger.error(f"An error occured while updating the guild: {after.id} - {after.name}.\n{r.text}")





def setup(bot):
	bot.add_cog(Guilds(bot))
