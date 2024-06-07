import nextcord, requests as req, asyncio, os, json
from nextcord.ext import commands
from aiohttp import web
from dbot.classes.Api import Api

class ComponentView(nextcord.ui.View):
	def __init__(self, components_data):
		super().__init__()
		for component_group in components_data:
			if not component_group:
				continue

			for component in component_group:
				if component['type'] == 2: # Button
					self.add_item(nextcord.ui.Button(
						style=nextcord.ButtonStyle(component['style']),
						label=component['label'],
						custom_id=component['customId']
					))
				elif component['type'] == 3: # Select Menu
					options = [
						nextcord.SelectOption(
							label=option['label'],
							value=option['value'],
							description=option['description'],
							emoji=option.get('emoji'),
							default=option.get('default', False)
						) for option in component['options']
					]
					self.add_item(nextcord.ui.Select(
						custom_id=component['customId'],
						options=options,
						min_values=component.get('minValues', 1),
						max_values=component.get('maxValues', 1)
					))

class Commands(commands.Cog):
	def __init__(self, bot):
		"""
		This class is used to update commands for the server.
		"""
		self.client = bot
		self.api = os.getenv("api.url")

	@nextcord.slash_command(
		name="newcommand",
		description="Create a new command for the server.",
		default_member_permissions=nextcord.Permissions(administrator=True),
	)
	async def newcommand(self, interaction: nextcord.Interaction, name: str, content: str):
		"""
		Create a new command for the server
		"""
		if not name or not content:
			await interaction.response.send_message("Please provide a name and content for the command.", ephemeral=True)
			return
		
		guild_id = interaction.guild.id
		r = req.get(f"{self.api}/guilds/{guild_id}/commands", headers={"Authorization": f"Bearer {os.getenv('api.key')}"})
		if r.status_code == 200:
			commands = r.json()
			for command in commands:
				if name == command['trigger']:
					await interaction.response.send_message("Command already exists.", ephemeral=True)
					return
				
		headers = {"Authorization": f"Bearer {os.getenv('api.key')}"}
		json = {
			"trigger": name, 
			"response": {
				'content': content, 
				'embeds': [], 
				'components': []
				}
			}
		response = req.post(f"{self.api}/guilds/{guild_id}/commands", json=json, headers=headers)
		if response.status_code == 200:
			returnEmbed = nextcord.Embed(title=f"Command Created", description=f"Want to add more to the command? Go to the [dashboard]({os.getenv('dashboard.url')})!")
			returnEmbed.add_field(name="Name", value=name, inline=False)
			returnEmbed.add_field(name="Content", value=content, inline=False)
			await interaction.response.send_message(embed=returnEmbed)
		else:
			print(response.text)

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

		command = Api().get_command(message, prefix)
		if not command:
			return

		# Extracting parts of the response for readability
		content = command.get('content', None)
		embed_data = command.get('embeds', [])

		# Convert color from hex string to integer
		for embed in embed_data:
			if 'color' in embed:
				embed['color'] = int(embed['color'].lstrip('#'), 16)

		embeds = [nextcord.Embed.from_dict(embed) for embed in embed_data] if embed_data else None

		# Creating a View for components
		view = ComponentView(command.get('components', [])) if command.get('components', []) else None

		# Sending the response
		if content or embeds or view:
			await message.channel.send(
				content=content if content else None,
				embed=embeds[0] if embeds else None,
				view=view if view else None
			)
		else:
			return

	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		"""
		Handle command errors
		"""
		if isinstance(error, commands.errors.CommandNotFound):
			return

		await ctx.send(f"An error occurred: {error}")

def setup(bot):
	bot.add_cog(Commands(bot))
