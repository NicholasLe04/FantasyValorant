import discord #pip install discord.py
from discord.ext import commands, tasks
from discord import app_commands
from discord import Member
from db import Database
from VCTDataScraper.scrape import Scraper
from threading import Thread
from user import Userbase
from time import time

# NOTES ABOUT PROGRAM:
# NEVER LEAK TOKEN, THIS ALLOWS CODE TO BE RUN ON THE BOT
# IF TOKEN LEAKED, GENERATE NEW ONE


## TOKEN DO NOT LEAK
TOKEN = 'MTAyMDAwOTM5MzM5MzI0NjI0Mg.Gt_Unu.jm624p_Ogoz3tyXfS6vXHv776SHpcR4pYDTaXU'

## Creates necessary objects
database = Database()
scraper = Scraper()
userbase = Userbase()
userbase.createTable()

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


## Updates player table every 30 minutes
@tasks.loop(minutes=30)
async def db_update_loop():
    channel = client.get_channel(1020057539292962856)   # Prints message in 'bot-commands' channel to confirm loop
    await channel.send('Updating SQL Table',delete_after=120)
    dbUpdate = Thread(target = database.updateTable, args=())   # Runs database update on 2nd thread to run bot processes and database processes simultaneously
    dbUpdate.start()


# client = commands.Bot(command_prefix='$', intents=discord.Intents.all())

 
## Prints message in console if bot launches successfully
@client.event
async def on_ready():
    db_update_loop.start()
    print("I got cash. Anyone need something?") # If you don't see this, the bot ain't online


### USER COMMANDS
# /player
# /roster

# Sends player info to channel 
@client.hybrid_command(name = "player", with_app_command = True, description = "Obtains player statistics",aliases = ['p'])
# Works only on selected server (guild)
@app_commands.guilds(discord.Object(id=1020055030247727155))
# Defining player command
# Params: ctx is defined as the command's context, player is set to empty string by default
async def player(ctx: commands.Context, player = ""):
    user_id = str(ctx.author.id) # This obtains the user's id who sent the command
    userbase.addNewUser(user_id)
    # Reply with a private message (command) or public message (using prefix)                   implement database
    await ctx.defer(ephemeral = True) # Idek what this does but it works lol
    if embedPlayerInfo(player) == "No player found":
        await ctx.reply("No player has been found under that name. Are you sure you typed it correctly?")
        return None
    await ctx.reply(embed=embedPlayerInfo(player))

# Returns a user's roster
@client.hybrid_command(name = "roster", with_app_command = True, description = "Gets your fantasy roster",aliases = ['r'])
# Works only on selected server (guild)
@app_commands.guilds(discord.Object(id=1020055030247727155))
# Defining roster command
# Params: ctx is defined as the command's context, user is optional field
async def roster(ctx: commands.Context, member: Member = None):
    # Reply with a private message (command) or public message (using prefix)                   implement database
    user_id = str(ctx.author.id) # This obtains the user's id who sent the command
    userbase.addNewUser(user_id)
    await ctx.defer(ephemeral = True) # Idek what this does but it works lol
    if (member == None):
        await ctx.reply(embed = embedRosterInfo(ctx.author, user_id))
    else:
        #await ctx.reply(embed = embedRosterInfo(member))
        await ctx.reply(embed = embedRosterInfo(member, user_id))

# Adds a player to user's roster
@client.hybrid_command(name = "draft", with_app_command = True, description = "Adds the selected player to your roster",aliases = ['d'])
# Works only on selected server (guild)
@app_commands.guilds(discord.Object(id=1020055030247727155))
# Defining add command
# Params: ctx is defined as the command's context, user is optional field
async def draft(ctx: commands.Context, player_name : str):
    user_id = str(ctx.author.id) # This obtains the user's id who sent the command
    userbase.addNewUser(user_id)
    # Reply with a private message (command) or public message (using prefix)                   implement database
    await ctx.defer(ephemeral=True)
    if userbase.addPlayer(player_name, user_id) == "No player found":
        await ctx.reply("No player has been found under that name. Are you sure you typed it correctly?")
        return None
    await ctx.reply("Player added")

''' #### to be implemented, add an index query too
    if (member == None):
        await ctx.reply(embed = embedRosterInfo(ctx.author))
    else:
        await ctx.reply(embed = embedRosterInfo(member))'''
        
## EMBED FUNCTIONS

def embedPlayerInfo(player_name : str):
    pname = None

    for name in database.playerNames:
        if (player_name.lower() == name.lower()):
            pname = name
            break
    
    if (pname == None):
        return "No player found"
        

    embed=discord.Embed(title=f"{database.playerGetUserName(pname)}",description=f"**{database.playerGetRealName(pname)}**\n{scraper.flagEmojis.get(database.playerGetRegion(pname))} {database.playerGetRegion(pname).lower().title()}")
    embed.set_author(name=database.playerGetTeam(pname), icon_url=scraper.scrapeTeamLogo(database.playerGetTeam(pname)))
    embed.set_thumbnail(url=database.playerGetPicture(pname))
    embed.add_field(name="ACS", value=database.playerGetGlobalACS(pname), inline=True)
    embed.add_field(name="K/D", value=database.playerGetGlobalKD(pname), inline=True)
    embed.add_field(name="KPR", value=database.playerGetGlobalKPR(pname))
    embed.add_field(name="APR", value=database.playerGetGlobalAPR(pname), inline=True)
    embed.add_field(name="AGENT", value=database.playerGetAgent(pname).capitalize())
    return (embed)


def embedRosterInfo(member : Member, id: str):
    testi = str(id)
    embed = discord.Embed(title=f"{member.name}'s Roster")
    #embed.add_field(name="Player 1", value=userbase.uTeamGetPlayers(str(member.id))[0], inline=False)
    embed.add_field(name="Player 1", value=userbase.uTeamGetPlayers("328309041518608385")[0], inline=False)
    print(id)
    print(userbase.uTeamGetPlayers(id)[0])
    print(userbase.uTeamGetPlayers)
    embed.add_field(name="Player 2", value=userbase.uTeamGetPlayers(id)[1], inline=False)
    embed.add_field(name="Player 3", value=userbase.uTeamGetPlayers(testi)[2], inline=False)
    embed.add_field(name="Player 4", value=userbase.uTeamGetPlayers(str(member.id))[3], inline=False)
    embed.add_field(name="Player 5", value=userbase.uTeamGetPlayers(str(member.id))[4], inline=False)
    print(userbase.uTeamGetPlayers(str(member.id))[4])
    print(str(member.id))
    return (embed)

### Getter Methods                                                                                                          ***TO BE ADDED TO DB.PY***

## Method returns average player ACS over course of match
## Pulled from match
## EX: getPlayerMatchACS()
def getPlayerMatchACS(match, player_name):
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