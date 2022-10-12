import discord #pip install discord.py
from discord.ext import commands, tasks
from discord import app_commands
from db import Database
from VCTDataScraper.scrape import Scraper
from threading import Thread

# NOTES ABOUT PROGRAM:
# NEVER LEAK TOKEN, THIS ALLOWS CODE TO BE RUN ON THE BOT
# IF TOKEN LEAKED, GENERATE NEW ONE


## TOKEN DO NOT LEAK
TOKEN = 'MTAyMDAwOTM5MzM5MzI0NjI0Mg.Gt_Unu.jm624p_Ogoz3tyXfS6vXHv776SHpcR4pYDTaXU'

## Creates necessary objects
database = Database()
scraper = Scraper()

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

## Generate Client object
client = Client()


### TESTING ZONE NO CAP AREA 51 TYPE BEAT FR


@tasks.loop(minutes=30) # Every 30 min, update player table
async def db_update_loop():
    channel = client.get_channel(1020057539292962856)   # Prints message in 'bot-commands' channel to confirm loop
    await channel.send('Updating SQL Table')
    dbUpdate = Thread(target = database.updateTable, args=())   # Runs database update on 2nd thread to run bot processes and database processes simultaneously
    dbUpdate.start()

#####


# client = commands.Bot(command_prefix='$', intents=discord.Intents.all())

 
## Prints message in console if bot launches successfully
@client.event
async def on_ready():
    db_update_loop.start()
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
    for name in database.playerNames:
        if (player_name == name.lower()):
            pname = name
            break
        return "No player found"
        

    embed=discord.Embed(title=f"{database.playerGetUserName(pname)}",description=f"**{database.playerGetRealName(pname)}**\n{scraper.flagEmojis.get(database.playerGetRegion(pname))} {database.playerGetRegion(pname).lower().title()}")
    embed.set_author(name=database.playerGetTeam(pname), icon_url=scraper.teamGetLogo(database.playerGetTeam(pname)))
    embed.set_thumbnail(url=database.playerGetPicture(pname))
    embed.add_field(name="ACS", value=database.playerGetGlobalACS(pname), inline=True)
    embed.add_field(name="K/D", value=database.playerGetGlobalKD(pname), inline=True)
    embed.add_field(name="KPR", value=database.playerGetGlobalKPR(pname))
    embed.add_field(name="APR", value=database.playerGetGlobalAPR(pname), inline=True)
    embed.add_field(name="AGENT", value=database.playerGetAgent(pname).capitalize())
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
