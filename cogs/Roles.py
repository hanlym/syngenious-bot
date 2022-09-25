import discord

from discord import app_commands
from discord.ext import commands

from discord.utils import get

server_id = 1003666789995135006


#Role assign buttons
#art
#writing
#programming
#photography

class AssignRole(discord.ui.View):
  def __init__(self):
    super().__init__()
    self.value = None
    self.timeout = None
    
  @discord.ui.button(emoji="🎨", label="Art", style=discord.ButtonStyle.blurple)
  async def art(self, interaction:discord.Interaction, button:discord.ui.Button):
    await interaction.response.defer()
    
    artR = get(interaction.guild.roles, name="art")
    if artR not in interaction.user.roles:
      await interaction.user.add_roles(artR)
  
  @discord.ui.button(emoji="🖊️", label="Writing", style=discord.ButtonStyle.blurple)
  async def writing(self, interaction:discord.Interaction, button:discord.ui.Button):
    await interaction.response.defer()
      
    writR = get(interaction.guild.roles, name="writing")
    if writR not in interaction.user.roles:
      await interaction.user.add_roles(writR)
  
  @discord.ui.button(emoji="💻", label="Programming", style=discord.ButtonStyle.blurple)
  async def programming(self, interaction:discord.Interaction, button:discord.ui.Button):
    await interaction.response.defer()
    
    progR = get(interaction.guild.roles, name="programming")
    if progR not in interaction.user.roles:
      await interaction.user.add_roles(progR)
  
  @discord.ui.button(emoji="📷", label="Photography", style=discord.ButtonStyle.blurple)
  async def photography(self, interaction:discord.Interaction, button:discord.ui.Button):
    await interaction.response.defer()
    
    photR = get(interaction.guild.roles, name="photography")
    if photR not in interaction.user.roles:
      await interaction.user.add_roles(photR)

class RolesCog(commands.Cog):
  def __init__(self, bot: commands.Bot) -> None:
    self.bot = bot
    self.users = self.bot.db["users"]

  @app_commands.command(name="role", description="Display role menu (admins only)")
  async def roles(self, interaction:discord.Interaction):
    adminRole = get(interaction.guild.roles, name="admin")
    if adminRole not in interaction.user.roles:
      await interaction.response.send_message(content="Only admins can use this command", ephemeral=True)
    else:
      view = AssignRole()
      await interaction.response.send_message(content="Get roles here", view=view)
    
async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(RolesCog(bot), guild=discord.Object(id=server_id))
  await bot.tree.sync(guild=discord.Object(id=server_id))
