import discord
from discord.ext import commands
from discord import app_commands
from discord.utils import get
        
class Website(discord.ui.View):
  def __init__(self):
    super().__init__()
    self.value = None
    self.timeout = None