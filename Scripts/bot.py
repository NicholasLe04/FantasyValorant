from ast import ExceptHandler
import requests #pip install requests
import discord #pip install discord.py
from discord.ext import commands
from discord import app_commands
from VCTDataScraper.scrape import Scrapper

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

## Create scrapper object
scrapper = Scrapper()
recentMatchUrl = scrapper.getRecentUrl()

 
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
    # Reply with a private message (command) or public message (using prefix)
    await ctx.defer(ephemeral = True) # Idek what this does but it works lol
    await ctx.reply(printPlayerInfo(player))

## Player info method
def printPlayerInfo(player_name):
    return (f"Username: {getPlayerUsername(player_name)}  |  Name: {getPlayerName(player_name)}  |  Team: {getPlayerTeam(player_name)}  |  ACS: {globalGetPlayerACS(player_name)}")

## Getter methods

## Method returns player team
## Pulled from player
## EX: getPlayerTeam('tenz') = 'Sentinels'
def getPlayerTeam(player_name: str):
    return scrapper.playerGetTeam(player_name)

## Method returns player name
## Pulled from player
## EX: getPlayerName('tenz') = 'Tyson Ngo'
def getPlayerName(player_name: str):
    return scrapper.playerGetName(player_name)

## Method returns player username
## Pulled from player
## EX: getPlayerTeam('tenz') = 'TenZ'
def getPlayerUsername(player_name: str):
    return scrapper.playerGetUsername(player_name)

## Method returns player image (.png link)
## Pulled from player
## EX: getPlayerPicture('tenz') = 'https:/img/base/ph/sil.png'
def getPlayerPicture(player_name: str):
    return scrapper.playerGetPicture(player_name)

## Method returns player region
## Pulled from player 
## EX: getPlayerRegion('tenz') = 'CANADA'
def getPlayerRegion(player_name: str):
    return scrapper.playerGetRegion(player_name)

## Method returns player ACS overall statistic
## Pulled from player
## EX: globalGetPlayerACS('tenz') = 261.3
def globalGetPlayerACS(player_name: str):
    return scrapper.playerGetGlobalACS(player_name)

## Method returns player KD overall statistic
## Pulled from player
## EX: globalGetPlayerKD('tenz') = 1.53
def globalGetPlayerKD(player_name: str):
    return scrapper.playerGetGlobalKD(player_name)

## Method returns player kills per round overall statistic
## Pulled from player
## EX: globalGetPlayerKPR('tenz') = 0.87
def globalGetPlayerKPR(player_name):
    return scrapper.playerGetGlobalKPR(player_name)

## Method returns player assists per round overall statistic
## Pulled from player
## EX: globalGetPlayerKPR('tenz') = 0.63
def globalGetPlayerAPR(player_name):
    return scrapper.playerGetGlobalAPR(player_name)

## Method returns player most played agent overall statistic
## Pulled from player
## EX: globalGetPlayerKPR('tenz') = 'chamber'
def globalGetPlayerAgent(player_name):
    return scrapper.playerGetAgent(player_name)

## Method returns average player ACS over course of match
## Pulled from match
## EX: getPlayerMatchACS()
def getPlayerMatchACS(match ,player_name):
    for player_stats in scrapper.getPlayerStats(match):
        if player_stats[0].lower() == player_name.lower():
            return player_stats[1]

## Method returns team logo (.png link)
## Pulled from team
def getTeamLogo(team: str):
    return scrapper.teamGetLogo(team)

## Method returns team name
## Pulled from team
def getTeamName(team: str):
    return scrapper.teamGetName(team)

## Kills/one taps the bot so we can work on it
### VERY VERY FUCKING IMPORTANT DELETE THIS SHIT BEFORE THIS GOES PUBLIC
@client.command(aliases=['onetap','mavenawpshot'])
@commands.has_permissions(administrator=True) # Online usable by a server admin
async def shutdown(ctx):
    exit() # Ends the program, bot will go offline

# Runs bot
client.run(TOKEN)