import discord
from discord.ext import commands
from discord import app_commands

#MTAxNTAwOTE0NTQ4MjY0OTc2MA.Gcwcds.JzND2NfHkdGlOT_mJhaV2PBmajZgMnWKRD8j_Y

bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())

class abot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
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
        print(interaction.user)
        print(self.author)

        #get user profile
        profileEmb = discord.Embed(title="Profile of merk#5844", colour=discord.Colour.dark_grey())
        profileEmb.add_field(name="Projects completed", value="7", inline=True)
        profileEmb.add_field(name="Average rating", value="4.2/5", inline=True)

        await self.author.send(content=f"{interaction.user} has registered interest in project \"{self.title}\"", embed=profileEmb)
                
bot = abot()
tree = app_commands.CommandTree(bot)

@tree.command(name="ping", description="Pong!", guild=discord.Object(id=1015009673088335874))
async def self(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!", ephemeral=True)

#TODO
#Profile: show rating, projects competed etc
#Post project: send dm with suitable people, use button to request people
#Connect with requested people who accept
#Leave rating at end of project
#Database

@tree.command(name="profile", description="Gets the profile of a specified user", guild=discord.Object(id=1015009673088335874))
async def self(interaction: discord.Interaction, user:str):
    profileEmb = discord.Embed(title="Profile of merk#5844", colour=discord.Colour.dark_grey())
    profileEmb.add_field(name="Projects completed", value="7", inline=True)
    profileEmb.add_field(name="Average rating", value="4.2/5", inline=True)
    await interaction.response.send_message(embed=profileEmb, ephemeral=True)

@tree.command(name="post", description="Create a project post", guild=discord.Object(id=1015009673088335874))
async def self(interaction: discord.Interaction, title:str, description:str):
    postEmb = discord.Embed(title=title, colour=discord.Colour.dark_gray())
    postEmb.add_field(name="Description", value=description)
    
    view = intButt(interaction.user, title)
    await interaction.response.send_message(embed=postEmb, view=view)

bot.run("")
