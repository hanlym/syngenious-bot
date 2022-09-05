import discord
from discord.ext import commands
from discord import app_commands

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

class abot(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.synced = False

    async def on_ready(self):
        await tree.sync(guild=discord.Object(id=1015009673088335874))
        self.synced = True
        print("Bot is online")

class intButt(discord.ui.View):
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
                
bot = abot()
tree = app_commands.CommandTree(bot)

@tree.command(name="ping", description="Pong!", guild=discord.Object(id=1015009673088335874))
async def self(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!", ephemeral=True)

@tree.command(name="profile", description="Gets the profile of a specified user", guild=discord.Object(id=1015009673088335874))
async def self(interaction:discord.Interaction, user:discord.Member):
    profileEmb = discord.Embed(title=f"Profile of {user.nick if user.nick else user.name}", colour=discord.Colour.dark_grey())
    profileEmb.set_thumbnail(url=user.avatar.url)
    profileEmb.add_field(name="Projects completed", value="7", inline=True)
    profileEmb.add_field(name="Average rating", value="4.2/5", inline=True)
    await interaction.response.send_message(embed=profileEmb, ephemeral=True)

@tree.command(name="post", description="Create a project post", guild=discord.Object(id=1015009673088335874))
async def self(interaction:discord.Interaction, title:str, description:str):
    postEmb = discord.Embed(title=title, colour=discord.Colour.dark_gray())
    postEmb.add_field(name="Description", value=description)
    
    view = intButt(interaction.user, title)
    await interaction.response.send_message(embed=postEmb, view=view)

@tree.command(name="rate", description="Rate a specified user", guild=discord.Object(id=1015009673088335874))
async def self(interaction:discord.Interaction, user:discord.Member, rating:int):
    
    if not 0 <= rating <=5:
        await interaction.response.send_message(content="Rating must be an integer between 0 and 5", ephemeral=True)
    else:
        #register rating in db
        await interaction.response.send_message(content=f"Gave user {user.nick if user.nick else user.name} rating of {rating}/5", ephemeral=True)

bot.run("token")
