import discord
from discord.ext import commands
from discord import app_commands
from discord.utils import get

import pymongo
from pymongo import MongoClient

import butts as b
import utils as u

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

id = 69420

class abot(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.synced = False

    async def on_ready(self):
        await tree.sync(guild=discord.Object(id=id))
        self.synced = True
        print("Bot is online")

        #connect to db
        cluster = MongoClient("server")
        db = cluster["alethia"]
        global collection
        collection = db["users"]
                
bot = abot()
tree = app_commands.CommandTree(bot)

@tree.command(name="ping", description="Pong!", guild=discord.Object(id=id))
async def self(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!", ephemeral=True)

@tree.command(name="profile", description="Gets the profile of a specified user", guild=discord.Object(id=id))
async def self(interaction:discord.Interaction, user:discord.Member):
    profile = collection.find_one({"_id":user.name})
    if not profile:
        await interaction.response.send_message(content="Profile does not exist.", ephemeral=True)
    else:
        profileEmb = discord.Embed(title=f"Profile of {user.nick if user.nick else user.name}", colour=discord.Colour.dark_grey())
        profileEmb.set_thumbnail(url=user.avatar.url)
        profileEmb.add_field(name="Bio", value=profile["bio"], inline=False)
        profileEmb.add_field(name="Skills and interests", value=profile["skills"], inline=False)
        profileEmb.add_field(name="Projects completed", value=profile["projects"], inline=False)
        profileEmb.add_field(name="Average rating", value=profile["rating"], inline=False)

        await interaction.response.send_message(embed=profileEmb, ephemeral=True)

@tree.command(name="post", description="Create a project post", guild=discord.Object(id=id))
async def self(interaction:discord.Interaction, title:str, description:str):
    postEmb = discord.Embed(title=title, colour=discord.Colour.dark_gray())
    postEmb.add_field(name="Description", value=description)
    
    view = b.IntButt(interaction.user, title)
    await interaction.response.send_message(embed=postEmb, view=view)

@tree.command(name="rate", description="Rate a specified user", guild=discord.Object(id=id))
async def self(interaction:discord.Interaction, user:discord.Member, rating:int):
    
    if not 0 <= rating <= 5:
        await interaction.response.send_message(content="Rating must be an integer between 0 and 5", ephemeral=True)
    else:
        if not collection.find_one({"_id":interaction.user.name}):
            currRating = collection.find_one({"_id":user.name})["rating"]
            ratings = collection.find_one({"_id":user.name})["ratings"]
            totRating = round(currRating * ratings) + rating
            newRating = round(totRating/(ratings+1), 1)

            collection.update_one({"_id":user.name}, {"$set":{"rating":newRating}})
            collection.update_one({"_id":user.name}, {"$inc":{"ratings":1}})
            await interaction.response.send_message(content=f"Gave user {user.nick if user.nick else user.name} rating of {rating}/5", ephemeral=True)
        else:
            await interaction.response.send_message(content="User profile does not exist.", ephemeral=True)

@tree.command(name="role", description="display role menu", guild=discord.Object(id=id))
async def self(interaction:discord.Interaction):
    adminRole = get(interaction.guild.roles, name="admin")
    if adminRole not in interaction.user.roles:
        await interaction.response.send_message(content="Only admins can use this command", ephemeral=True)
    else:
        view = b.AssignRole()
        await interaction.response.send_message(content="Get roles here", view=view)

@tree.command(name="profileconfig", description="create or update your profile", guild=discord.Object(id=id))
async def self(interaction:discord.Interaction, bio:str, skills_and_interests:str):
    if collection.find({"_id":interaction.user.name}):
        #update profile
        collection.update_one({"_id":interaction.user.name}, {"$set":{
            "bio":bio,
            "skills":skills_and_interests
        }})
        
        await interaction.response.send_message(content="Updated profile.", ephemeral=True)
    else:
        #create new profile
        collection.insert_one({
            "_id":interaction.user.name,
            "bio":bio,
            "skills":skills_and_interests,
            "projects":0,
            "rating":0,
            "ratings":0
        })
        await interaction.response.send_message(content="Created profile", ephemeral=True)

@tree.command(name="join", description="join", guild=discord.Object(id=id))
async def self(interaction:discord.Interaction):
    view = b.Website()
    view.add_item(discord.ui.Button(label="Visit website", style=discord.ButtonStyle.link, url="https://github.com/hanlym/aletheia-bot"))
    await interaction.user.send(content="Visit the website to set up your profile", view=view)

bot.run("token")
