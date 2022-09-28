from ast import ExceptHandler
import discord #pip install discord.py
from discord.ext import commands
from discord import app_commands
'''from VCTDataScraper.scrape import Scraper '''#                                            ***TO BE ADDED TO DB.PY***
from VCTDataScraper.db import Database

# NOTES ABOUT PROGRAM:
# TAKES ~ 30s TO LAUNCH, GIVE IT TIME
# ONCE DONE, STOP YOUR PROGRAM
# NEVER LEAK TOKEN, THIS ALLOWS CODE TO BE RUN ON THE BOT
# IF TOKEN LEAKED, GENERATE NEW ONE

## Initialize client
class Client(commands.Bot):
    def __init__(self):
        # Intents
        intents = discord.Intents.default()
        intents.message_content = True
        # intents.members = True
        # intents.presences = True
        # intents.reactions = True
        super().__init__(command_prefix = "$",intents = intents)

    async def setup_hook(self):
        await self.tree.sync(guild = discord.Object(id=1020055030247727155)) # Only will work on this server (guild)
        print("Synced tree") # If you don't see this, it didn't work

    async def on_command_error(self,ctx,error):
        await ctx.reply(error,ephemeral = True)

client = Client()

# client = commands.Bot(command_prefix='$', intents=discord.Intents.all())
## TOKEN DO NOT LEAK
TOKEN = 'MTAyMDAwOTM5MzM5MzI0NjI0Mg.Gt_Unu.jm624p_Ogoz3tyXfS6vXHv776SHpcR4pYDTaXU'

## Create scraper object                                                                                                          ***TO BE ADDED TO DB.PY***
''' scraper = Scraper()'''
database = Database()
'''recentMatchUrl = scraper.getRecentUrl()'''                                                                                 ##  ***TO BE ADDED TO DB.PY***

 
## Prints message in console if bot launches successfully
@client.event
async def on_ready():
    print("I got cash. Anyone need something?") # If you don't see this, the bot ain't online

# Sends player info to channel 
@client.hybrid_command(name = "player", with_app_command = True, description = "Obtain player statistics",aliases = ['p'])
# Works only on selected server (guild)
@app_commands.guilds(discord.Object(id=1020055030247727155))
# Defining player command
# Params: ctx is defined as the command's context, player is set to empty string by default
async def player(ctx: commands.Context, player = ""):
    # Reply with a private message (command) or public message (using prefix)                   implement database
    await ctx.defer(ephemeral = True) # Idek what this does but it works lol
    if embedPlayerInfo(player) == "No player found":
        await ctx.reply("No player has been found under that name. Are you sure you typed it correctly?")
        return None
    await ctx.reply(embed=embedPlayerInfo(player))

# Methods that interface with discord.py

## Team info method
## Returns an embed with respective team information
## Usage: await ctx.reply(embed = embedTeamInfo(team_name))
## embedTeamInfo(team_name) will return embed
# def embedTeamInfo(team_name):
#     embed=discord.Embed(title=f"{getTeamName(team_name)}",description=f"**{getTeamAbbreviation(team_name)}**\n{getTeamRegionFlag(team_name)} {getTeamRegion(team_name).lower().title()}") # This cannot be implemented until these methods are added
#     embed.set_thumbnail(url=getTeamLogo(team_name))
#     # For loop here for each player to be listed, inline 2 wide
#     return (embed)

## Player info method                                                                                                          ***TO BE ADDED TO DB.PY***
## Returns an embed with respective player information
## Usage: await ctx.reply(embed = embedPlayerInfo(player_name))
## embedPlayerInfo(player_name) will return embed 
def embedPlayerInfo(player_name):
    try:
        database.playerGetUsername()
    except AttributeError:
        return "No player found"
    embed=discord.Embed(title=f"{database.playerGetUsername(player_name)}",description=f"**{database.playerGetName(player_name)}**\n{database.playerGetRegionFlag(player_name)} {database.playerGetRegion(player_name).lower().title()}")
    embed.set_author(name=database.playerGetTeam(player_name), icon_url=database.teamGetLogo(database.playerGetTeam(player_name)))
    embed.set_thumbnail(url=database.playerGetPicture(player_name))
    embed.add_field(name="ACS", value=database.playerGetGlobalACS(player_name), inline=True)
    embed.add_field(name="K/D", value=database.playerGetGlobalKD(player_name), inline=True)
    embed.add_field(name="KPR", value=database.playerGetGlobalKPR(player_name))
    embed.add_field(name="APR", value=database.playerGetGlobalAPR(player_name), inline=True)
    embed.add_field(name="AGENT", value=database.playerGetAgent(player_name).capitalize())
    return (embed)


### Getter Methods                                                                                                          ***TO BE ADDED TO DB.PY***

## Method returns average player ACS over course of match
## Pulled from match
## EX: getPlayerMatchACS()
def getPlayerMatchACS(match ,player_name):
    for player_stats in database.getPlayerStats(match):
        if player_stats[0].lower() == player_name.lower():
            return player_stats[1]


## Kills/one taps the bot so we can work on it
### VERY VERY IMPORTANT DELETE THIS BEFORE THIS GOES PUBLIC
@client.command(aliases=['onetap','mavenawpshot', 'stirfriedsatchelpeak'])
@commands.has_permissions(administrator=True) # Online usable by a server admin
async def shutdown(ctx):
    exit() # Ends the program, bot will go offline

# Runs bot
client.run(TOKEN)