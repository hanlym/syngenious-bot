import discord
from discord.ext import commands
from discord import app_commands
from discord.utils import get

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
        
class Website(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None
        self.timeout = None