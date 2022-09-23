import discord
from discord.ext import commands
from discord import app_commands
from discord.utils import get

import pymongo
from pymongo import MongoClient

import butts as b
import utils as u

import os

from keep_alive import keep_alive


extensions = [
  'cogs.DevTools',
  'cogs.Profiles',
  'cogs.Projects',
#   'cogs.Polls'
]

# #connect to db
# cluster = MongoClient(os.getenv("MONGODB_CONNECTION_STRING"))
# db = cluster["alethia"]
# global collection
# collection = db["users"]

class abot(commands.Bot):
  def __init__(self, command_prefix, intents):
    super().__init__(command_prefix=command_prefix, intents=intents)
    self.synced = False
    self.db = MongoClient(os.environ["MONGODB_CONNECTION_STRING"])["alethia"]
    global collection
    collection = self.db["users"]

  async def setup_hook(self):
    for ext in extensions:
      await self.load_extension(ext)

  async def on_ready(self):
    await self.tree.sync(guild=discord.Object(id=server_id))
    self.synced = True
    print("Bot is online")

intents = discord.Intents.default()
intents.members = True

server_id = 1003666789995135006

bot = abot(command_prefix="/", intents=intents)
tree = bot.tree


@tree.command(name="role", description="Display role menu (admins only)", guild=discord.Object(id=server_id))
async def self(interaction:discord.Interaction):
  adminRole = get(interaction.guild.roles, name="admin")
  if adminRole not in interaction.user.roles:
    await interaction.response.send_message(content="Only admins can use this command", ephemeral=True)
  else:
    view = b.AssignRole()
    await interaction.response.send_message(content="Get roles here", view=view)


@tree.command(name="join", description="join", guild=discord.Object(id=server_id))
async def self(interaction:discord.Interaction):
  view = b.Website()
  view.add_item(discord.ui.Button(label="Visit website", style=discord.ButtonStyle.link, url="https://github.com/hanlym/aletheia-bot"))
  await interaction.user.send(content="Visit the website to set up your profile", view=view)

if __name__=='__main__':
  keep_alive()
  bot.run(os.environ["BOT_TOKEN"])
