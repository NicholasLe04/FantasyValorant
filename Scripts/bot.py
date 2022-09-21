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


## Access each regions' players and grabs their stats
na_stats = requests.get('https://vlrggapi.vercel.app/stats/na/90')
emea_stats = requests.get("https://vlrggapi.vercel.app/stats/eu/90")
apac_stats = requests.get("https://vlrggapi.vercel.app/stats/ap/90")
sa_stats = requests.get("https://vlrggapi.vercel.app/stats/sa/90")
jpn_stats = requests.get("https://vlrggapi.vercel.app/stats/jp/90")
ocea_stats = requests.get("https://vlrggapi.vercel.app/stats/oce/90")
mena_stats = requests.get("https://vlrggapi.vercel.app/stats/mn/90")

## Creates 'stats' variable to hold stats from all regions
stats = na_stats.json()
stats['data']['segments'] += emea_stats.json()['data']['segments']
stats['data']['segments'] += apac_stats.json()['data']['segments']
stats['data']['segments'] += sa_stats.json()['data']['segments']
stats['data']['segments'] += jpn_stats.json()['data']['segments']
stats['data']['segments'] += ocea_stats.json()['data']['segments']
stats['data']['segments'] += mena_stats.json()['data']['segments']

 
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
    for player in stats['data']['segments']:
        # If player name == user input
        if player['player'].lower() == player_name.lower():
            # Name: {player} | Team: {org} | ACS: {acs}
            return (f"Name: {player['player']}  |  Team: {player['org']}  |  ACS: {player['average_combat_score']}")

## Getter methods
## Method returns player kills over course of match
## Pulled from player
def globalGetPlayerKills(match,player_name):
    None

## Method returns player deaths over course of match
## Pulled from player
def globalGetPlayerDeaths(match,player_name):
    None

## Method returns player assists over course of match
## Pulled from player
def globalGetPlayerAssists(match,player_name):
    None

## Method returns player headshot % overall statistic
## Pulled from player
def globalGetPlayerHeadshot(player_name):
    None

## Method returns player KD % overall statistic
## Pulled from player
def globalGetPlayerKD(player_name):
    None

## Method returns player ACS % overall statistic
## Pulled from player
def globalGetPlayerACS(player_name):
    None

## Method returns player most played agent overall statistic
## Pulled from player
def globalGetPlayerAgent(player_name):
    None

## Method returns player team
## Pulled from team
def getPlayerTeam(player_name):
    None

## Method returns average player ACS over course of match
## Pulled from match
def getPlayerACS(match,player_name):
    None

## Method returns player name
## Pulled from team
def getPlayerName(player_name):
    None

## Method returns player username
## Pulled from team
def getPlayerUsername(player_name):
    None

## Method returns player username (.png link)
## Pulled from team
def getPlayerPicture(player_name):
    None

## Method returns player region
## Pulled from team
def getPlayerRegion(player_name):
    None

## Method returns team logo (.png link)
## Pulled from team
def getTeamLogo(team):
    None

## Method returns team name
## Pulled from team
def getTeamName(team):
    None

## Kills/one taps the bot so we can work on it
### VERY VERY FUCKING IMPORTANT DELETE THIS SHIT BEFORE THIS GOES PUBLIC
@client.command(aliases=['onetap','mavenawpshot'])
@commands.has_permissions(administrator=True) # Online usable by a server admin
async def shutdown(ctx):
    exit() # Ends the program, bot will go offline

# Runs bot
client.run(TOKEN)