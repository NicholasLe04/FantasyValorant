import discord #pip install discord.py
from discord.ext import commands, tasks
from discord import app_commands
from discord import Member
from database import Database
from VCTDataScraper.scrape import Scraper
from threading import Thread
from userbase import Userbase
from discord.ui import Button, View
from leaguebase import LeagueBase

# NOTES ABOUT PROGRAM:
# NEVER LEAK TOKEN, THIS ALLOWS CODE TO BE RUN ON THE BOT
# IF TOKEN LEAKED, GENERATE NEW ONE


## TOKEN DO NOT LEAK
TOKEN = 'MTAyMDAwOTM5MzM5MzI0NjI0Mg.Gt_Unu.jm624p_Ogoz3tyXfS6vXHv776SHpcR4pYDTaXU'

## Creates necessary objects
database = Database()
scraper = Scraper()
userbase = Userbase()
leaguebase = LeagueBase()
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

### Buttons subclass
class Buttons(discord.ui.View):
    def __init__(self, member: Member, timeout=60):
        super().__init__(timeout=timeout)
        self.member = member
    @discord.ui.button(label="1", style=discord.ButtonStyle.blurple)
    async def roster1(self, button:discord.ui.Button, interaction:discord.Interaction):
        await interaction.response.edit_message(embed=embedRosterInfo(self.member, 1))
    @discord.ui.button(label="2", style=discord.ButtonStyle.blurple)
    async def roster2(self, button:discord.ui.Button, interaction:discord.Interaction):
        await interaction.response.edit_message(embed=embedRosterInfo(self.member, 2))
    @discord.ui.button(label="3", style=discord.ButtonStyle.blurple)
    async def roster3(self, button:discord.ui.Button, interaction:discord.Interaction):
        await interaction.response.edit_message(embed=embedRosterInfo(self.member, 3))
    

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
# '/player'
# '/roster'
# '/draft'
# '/drop'
# '/drop-all'

# Sends player info to channel 
@client.hybrid_command(name = "player", with_app_command = True, description = "Obtains player statistics",aliases = ['p'])
# Works only on selected server (guild)
@app_commands.guilds(discord.Object(id=1020055030247727155))
# Defining player command
# Params: ctx is defined as the command's context, player is set to empty string by default
async def player(ctx: commands.Context, player = ""):
    disc_id = str(ctx.author.id) # This obtains the user's id who sent the command
    userbase.addNewUser(disc_id)
    # Reply with a private message (command) or public message (using prefix)                   implement database
    await ctx.defer(ephemeral = True) # Idek what this does but it works lol
    
    if embedPlayerInfo(player) == "No player found":
        await ctx.reply("No player has been found under that name. Are you sure you typed it correctly?")
        return None
    await ctx.reply(embed=embedPlayerInfo(player))


@client.hybrid_command(name = "team", with_app_command= True, description = "Returns team stats",aliases = ['t'])
@app_commands.guilds(discord.Object(id=1020055030247727155))
async def team(ctx: commands.Context, *, team_name):
    disc_id = str(ctx.author.id)
    userbase.addNewUser(disc_id)
    await ctx.defer(ephemeral=True)
    
    if embedTeamInfo(team_name) == "No team found":
        await ctx.reply("No team has been found under that name. Are you sure you typed it correctly?")
        return None
    await ctx.reply(embed=embedTeamInfo(team_name))


# Returns a user's roster
@client.hybrid_command(name = "roster", with_app_command = True, description = "Gets your fantasy roster",aliases = ['r'])
# Works only on selected server (guild)
@app_commands.guilds(discord.Object(id=1020055030247727155))
# Defining roster command
# Params: ctx is defined as the command's context, user is optional field
async def roster(ctx: commands.Context, member: Member = None):
    # Reply with a private message (command) or public message (using prefix)                   implement database
    disc_id = str(ctx.author.id) # This obtains the user's id who sent the command
    userbase.addNewUser(disc_id)
    await ctx.defer(ephemeral = True) # Idek what this does but it works lol
    if (member == None):
        member_ref = ctx.author
    else:
        member_ref = member
    view = Buttons(member_ref)
    await ctx.send(embed=embedRosterInfo(member_ref, 1), view=view)

    # while True:
    #     try:
    #         reaction = await client.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in buttons, timeout=60.0)
    #     except asyncio.TimeoutError:
    #         embed = embedRosterInfo(member_ref, current_page)
    #         embed.set_footer(text="Timed Out.")
    #         await msg.clear_reactions()

    #     else:
    #         previous_page = current_page

    #         if current_page != previous_page:
    #             await msg.edit(embed=embedRosterInfo(member_ref, current_page))

# Adds a player to user's roster
@client.hybrid_command(name = "draft", with_app_command = True, description = "Adds the selected player to your roster",aliases = ['d'])
# Works only on selected server (guild)
@app_commands.guilds(discord.Object(id=1020055030247727155))
# Defining add command
# Params: ctx is defined as the command's context, player_name is the selected player
async def draft(ctx: commands.Context, player_name : str):
    disc_id = str(ctx.author.id) # This obtains the user's id who sent the command
    userbase.addNewUser(disc_id)
    # Reply with a private message (command) or public message (using prefix)                   implement database
    await ctx.defer(ephemeral=True)
    x = userbase.addPlayer(player_name, disc_id)
    if x == "No player found":
        await ctx.reply("No player has been found under that name. Are you sure you typed it correctly?")
        return None
    elif x == "Roster full":
        await  ctx.reply("Roster filled!")
        return None
    await ctx.reply("Player added")

# Creates a league
@client.hybrid_command(name = "create", with_app_command = True, description = "Creates a league")
# Works only on selected server (guild)
@app_commands.guilds(discord.Object(id=1020055030247727155))
# Defining add command
# Params: ctx is defined as the command's context, player_name is the selected player
async def create(ctx: commands.Context, name : str):
    disc_id = str(ctx.author.id)
    # Reply with a private message (command) or public message (using prefix)                   implement database
    await ctx.defer(ephemeral=True)
    await ctx.reply(leaguebase.createLeague(name, disc_id))
    
# Removes player from user's roster
@client.hybrid_command(name = "drop", with_app_command = True, description = "Removes the selected player from your roster",aliases = ['dr'])
# Works only on selected server (guild)
@app_commands.guilds(discord.Object(id=1020055030247727155))
# Defining add command
# Params: ctx is defined as the command's context, player_name is the selected player
async def drop(ctx: commands.Context, player_name : str):
    disc_id = str(ctx.author.id) # This obtains the user's id who sent the command
    userbase.addNewUser(disc_id)
    # Reply with a private message (command) or public message (using prefix)                   implement database
    await ctx.defer(ephemeral=True)
    if userbase.dropPlayer(player_name, disc_id) == "No player found":
        await ctx.reply("No player has been found under that name in your roster. Are you sure you typed it correctly?")
        return None
    await ctx.reply("Player dropped")

# Removes player from user's roster
@client.hybrid_command(name = "drop-all", with_app_command = True, description = "Removes all players from your roster",aliases = ['da'])
# Works only on selected server (guild)
@app_commands.guilds(discord.Object(id=1020055030247727155))
# Defining add command
# Params: ctx is defined as the command's context, player_name is the selected player
async def drop_all(ctx: commands.Context):
    disc_id = str(ctx.author.id) # This obtains the user's id who sent the command
    userbase.addNewUser(disc_id)
    # Reply with a private message (command) or public message (using prefix)                   implement database
    await ctx.defer(ephemeral=True)
    for player in userbase.uTeamGetLeagueRoster1(disc_id):
        userbase.dropPlayer(player, disc_id)

    await ctx.reply("Roster has been dropped")




''' #### to be implemented, add an index query too
    if (member == None):
        await ctx.reply(embed = embedRosterInfo(ctx.author))
    else:
        await ctx.reply(embed = embedRosterInfo(member))'''
        
#######################
#   EMBED FUNCTIONS   #
#######################

def embedPlayerInfo(player_name: str):
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

def embedTeamInfo (team_name: str):
    try:
        team_name = team_name.lower()
        embed = discord.Embed(title=f"{scraper.scrapeTeamRegionFlag(team_name)} {scraper.scrapeTeamRegion(team_name)}")
        embed.set_author(name=f"{scraper.scrapeTeamName(team_name)}")
        embed.set_thumbnail(url=scraper.scrapeTeamLogo(team_name.lower()))
        
        for player in database.teamGetPlayers(team_name): ## Make a string of players seperated by ,
            pname = player.lower()
            embed.add_field(name=f"{player}", value=f"**ACS** {database.playerGetGlobalACS(pname)} | **K/D** {database.playerGetGlobalKD(pname)}\n{scraper.flagEmojis.get(database.playerGetRegion(pname))} {database.playerGetRegion(pname).lower().title()}", inline=False) ## Make an element for each player & display team
        
        return (embed)
    except:
        return ("Team not found")


def embedRosterInfo(member: Member, league: int):
    embed = discord.Embed(title=f"{member.name}'s Roster")
    embed.set_thumbnail(url = member.avatar.url)
    if (league == 1):
        roster = userbase.uTeamGetLeagueRoster1(member.id)
    elif (league == 2):
        roster = userbase.uTeamGetLeagueRoster2(member.id)
    elif (league == 3):
        roster = userbase.uTeamGetLeagueRoster3(member.id)
    else:
        return ("Invalid league")

    embed.add_field(name="Players", value=f"• {roster[0]}\n• {roster[1]}\n• {roster[2]}\n• {roster[3]}\n• {roster[4]}\n", inline=False)
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