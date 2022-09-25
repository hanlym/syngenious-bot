import discord

from discord import app_commands
from discord.ext import commands
from discord.utils import get


server_id = 1003666789995135006

class DevToolsCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.users = self.bot.db["users"]
    
    async def cog_check(self, ctx):
        '''
        The default check for this cog whenever a command is used. Returns True if the command is allowed.
        '''
        programmer_role = get(ctx.interaction.guild.roles, id=1014849397995089981)
        return programmer_role in ctx.interaction.user.roles

    @app_commands.command(name="ping", description="Pong!")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message("Pong!", ephemeral=True)

    @app_commands.command(name="reload", description="Reloads a cog.")
    async def reload(self, interaction:discord.Interaction, cog:str):
        extensions = self.bot.extensions  # A list of the bot's cogs/extensions.
        if cog == 'all':  # Lets you reload all cogs at once
            for extension in extensions:
                self.bot.unload_extension(cog)
                self.bot.load_extension(cog)
            await interaction.response.send_message(content="Done", ephemeral=True)
        if cog in extensions:
            await self.bot.unload_extension(cog)  # Unloads the cog
            await self.bot.load_extension(cog)  # Loads the cog
            await interaction.response.send_message(content="Done", ephemeral=True)
        else:
            await interaction.response.send_message(content="Unknown Cog", ephemeral=True)
        
    @app_commands.command(name="unload", description="Unloads a cog.")
    async def unload(self, interaction:discord.Interaction, cog:str):
        extensions = self.bot.extensions
        if cog not in extensions:
            await interaction.response.send_message(content="Cog is not loaded!", ephemeral=True)
            return
        self.bot.unload_extension(cog)
        await interaction.response.send_message(content=f"`{cog}` has successfully been unloaded.", ephemeral=True)

    @app_commands.command(name="listcogs", description="Returns a list of all cogs")
    async def listcogs(self, interaction:discord.Interaction):
        base_string = "```css\n" 
        base_string += "\n".join([str(cog) for cog in self.bot.extensions])
        base_string += "\n```"
        await interaction.response.send_message(content=base_string, ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(DevToolsCog(bot), guild=discord.Object(id=server_id))
    await bot.tree.sync(guild=discord.Object(id=server_id))