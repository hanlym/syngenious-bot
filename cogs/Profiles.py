import discord

from discord import app_commands
from discord.ext import commands

server_id = 1003666789995135006

class ProfileCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.users = self.bot.db["users"]
        
    @app_commands.command(name="profile", description="Gets the profile of a specified user")
    async def profile(self, interaction:discord.Interaction, user:discord.Member):
        profile = self.users.find_one({"_id":user.name})
        if not profile:
            await interaction.response.send_message(content="Profile does not exist.", ephemeral=True)
        else:
            profileEmb = discord.Embed(title=f"Profile of {user.nick if user.nick else user.name}", colour=discord.Colour.dark_grey())
            profileEmb.set_thumbnail(url=user.avatar.url)

            if profile["bio"]: profileEmb.add_field(name="Bio", value=profile["bio"], inline=False)
            if profile["skills"]: profileEmb.add_field(name="Skills and interests", value=profile["skills"], inline=False)
            profileEmb.add_field(name="Projects completed", value=profile["projects"], inline=False)
            profileEmb.add_field(name="Average rating", value=profile["rating"], inline=False)

            await interaction.response.send_message(embed=profileEmb, ephemeral=True)

    @app_commands.command(name="profileconfig", description="create or update your profile")
    async def profileconfig(self, interaction:discord.Interaction, bio:str, skills_and_interests:str):
        if self.users.count_documents({"_id":interaction.user.name}) == 0:
            #update profile
            self.users.update_one({"_id":interaction.user.name}, {"$set":{
                "bio":bio,
                "skills":skills_and_interests
            }})
            
            await interaction.response.send_message(content="Updated profile.", ephemeral=True)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ProfileCog(bot), guild=discord.Object(id=server_id))
    await bot.tree.sync(guild=discord.Object(id=server_id))
