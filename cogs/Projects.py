import discord

from discord import app_commands
from discord.ext import commands

import butts as b

server_id = 1003666789995135006

class IntButt(discord.ui.View):
  def __init__(self, author, title):
    super().__init__()
    self.value = None
    self.timeout = None
    self.author = author
    self.title = title

  @discord.ui.button(label="Register interest", style=discord.ButtonStyle.blurple)
  async def interest(self, interaction:discord.Interaction, button:discord.ui.Button):
    await interaction.response.send_message(content="Registered interest", ephemeral=True)

    #get user profile from db
    profileEmb = discord.Embed(title=f"Profile of {interaction.user.nick if interaction.user.nick else interaction.user.name}", colour=discord.Colour.dark_grey())
    profileEmb.set_thumbnail(url=interaction.user.avatar.url)
    profileEmb.add_field(name="Projects completed", value="7", inline=True)
    profileEmb.add_field(name="Average rating", value="4.2/5", inline=True)

    await self.author.send(content=f"{interaction.user} has registered interest in project \"{self.title}\"", embed=profileEmb)


class ProjectsCog(commands.Cog):
  def __init__(self, bot: commands.Bot) -> None:
    self.bot = bot
    self.users = self.bot.db["users"]

  @app_commands.command(name="post", description="Create a project post")
  async def post(self, interaction:discord.Interaction, title:str, description:str):
    postEmb = discord.Embed(title=title, colour=discord.Colour.dark_gray())
    postEmb.add_field(name="Description", value=description)
    
    view = b.IntButt(interaction.user, title)
    await interaction.response.send_message(embed=postEmb, view=view)

  @app_commands.command(name="rate", description="Rate a specified user")
  async def rate(self, interaction:discord.Interaction, user:discord.Member, rating:int):
    if not 1 <= rating <= 5:
      await interaction.response.send_message(content="Rating must be an integer between 1 and 5", ephemeral=True)
    else:
      if self.users.count_documents(self.users.find({"_id":interaction.user.name})) != 0:
        currRating = self.users.find_one({"_id":user.name})["rating"]
        ratings = self.users.find_one({"_id":user.name})["ratings"]
        totRating = round(currRating * ratings) + rating
        newRating = round(totRating/(ratings+1), 1)

        self.users.update_one({"_id":user.name}, {"$set":{"rating":newRating}})
        self.users.update_one({"_id":user.name}, {"$inc":{"ratings":1}})
        await interaction.response.send_message(content=f"Gave user {user.nick if user.nick else user.name} rating of {rating}/5", ephemeral=True)
      else:
        await interaction.response.send_message(content="User profile does not exist.", ephemeral=True)

async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(ProjectsCog(bot), guild=discord.Object(id=server_id))
  await bot.tree.sync(guild=discord.Object(id=server_id))