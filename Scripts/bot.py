from ast import ExceptHandler
import requests
import discord
from discord.ext import commands
from discord import app_commands

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
        await self.tree.sync(guild = discord.Object(id=1020055030247727155))
        print("Synced tree")

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
 
## Prints message in console if bot launches successfullylemme switch smt rq

@client.event
async def on_ready():
    print("I got cash. Anyone need something?")

# Sends player info to channel
@client.hybrid_command(name = "player", with_app_command = True, description = "Obtain player statistics",aliases = ['p'])
@app_commands.guilds(discord.Object(id=1020055030247727155))
async def player(ctx: commands.Context, player = ""):
    await ctx.defer(ephemeral = True)
    await ctx.reply(printPlayerInfo(player))

## Player info method
def printPlayerInfo(player_name):
    for player in stats['data']['segments']:
        # If player name == user input
        if player['player'].lower() == player_name.lower():
            # Name: {player} | Team: {org} | ACS: {acs}
            return (f"Name: {player['player']}  |  Team: {player['org']}  |  ACS: {player['average_combat_score']}")


## Kills/one taps the bot so we can work on it
### VERY VERY FUCKING IMPORTANT DELETE THIS SHIT BEFORE THIS GOES PUBLIC
@client.command(aliases=['onetap','mavenawpshot'])
@commands.has_permissions(administrator=True)
async def shutdown(ctx):
    exit()

# Runs bot
client.run(TOKEN)