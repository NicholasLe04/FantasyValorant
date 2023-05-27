from dis import disco
from token import TOKEN
import discord  # pip install discord.py
from discord.ext import commands, tasks
from discord import ButtonStyle, app_commands
from discord import Member
from database import Database
from VCTDataScraper.scrape import Scraper
from threading import Thread
from userbase import Userbase
from discord.ui import Button, View
from leaguebase import LeagueBase

# Creates necessary objects
database = Database()
scraper = Scraper()
userbase = Userbase()
leaguebase = LeagueBase()
userbase.createTable()

# Initialize client


class Client(commands.Bot):
    def __init__(self):
        # Intents
        intents = discord.Intents.default()
        intents.message_content = True
        # intents.members = True
        # intents.presences = True
        # intents.reactions = True
        super().__init__(command_prefix="$", intents=intents)

    async def setup_hook(self):
        # Only will work on this server (guild)
        await self.tree.sync(guild=discord.Object(id=1020055030247727155))
        print("Synced tree")  # If you don't see this, it didn't work

    async def on_command_error(self, ctx, error):
        await ctx.reply(error, ephemeral=True)


# Generate Client object
client = Client()

# ### Buttons subclass
# class Buttons(discord.ui.View):
#     def __init__(self, member: Member, timeout=60):
#         super().__init__(timeout=timeout)
#         self.member = member
#     @discord.ui.button(label="1", style=discord.ButtonStyle.blurple)
#     async def roster1(self, button:discord.ui.Button, interaction:discord.Interaction):
#         await interaction.response.edit_message(embed=embedRosterInfo(self.member, 1))
#     @discord.ui.button(label="2", style=discord.ButtonStyle.blurple)
#     async def roster2(self, button:discord.ui.Button, interaction:discord.Interaction):
#         await interaction.response.edit_message(embed=embedRosterInfo(self.member, 2))
#     @discord.ui.button(label="3", style=discord.ButtonStyle.blurple)
#     async def roster3(self, button:discord.ui.Button, interaction:discord.Interaction):
#         await interaction.response.edit_message(embed=embedRosterInfo(self.member, 3))


# Updates player table every 30 minutes
@tasks.loop(minutes=30)
async def db_update_loop():
    # Prints message in 'bot-commands' channel to confirm loop
    channel = client.get_channel(1020057539292962856)
    await channel.send('Updating SQL Table', delete_after=120)
    # Runs database update on 2nd thread to run bot processes and database processes simultaneously
    dbUpdate = Thread(target=database.updateTable, args=())
    dbUpdate.start()


# client = commands.Bot(command_prefix='$', intents=discord.Intents.all())


# Prints message in console if bot launches successfully
@client.event
async def on_ready():
    db_update_loop.start()
    # If you don't see this, the bot ain't online
    print("I got cash. Anyone need something?")


# USER COMMANDS
# '/player'
# '/roster'
# '/draft'
# '/drop'
# '/drop-all'

# Sends player info to channel
@client.hybrid_command(name="player", with_app_command=True, description="Obtains player statistics", aliases=['p'])
# Works only on selected server (guild)
@app_commands.guilds(discord.Object(id=1020055030247727155))
# Defining player command
# Params: ctx is defined as the command's context, player is set to empty string by default
async def player(ctx: commands.Context, player=""):
    # This obtains the user's id who sent the command
    disc_id = str(ctx.author.id)
    userbase.addNewUser(disc_id)
    # Reply with a private message (command) or public message (using prefix)                   implement database
    await ctx.defer(ephemeral=True)  # Idek what this does but it works lol

    if embedPlayerInfo(player) == "No player found":
        await ctx.reply("No player has been found under that name. Are you sure you typed it correctly?")
        return None
    await ctx.reply(embed=embedPlayerInfo(player))


@client.hybrid_command(name="team", with_app_command=True, description="Returns team stats", aliases=['t'])
@app_commands.guilds(discord.Object(id=1020055030247727155))
async def team(ctx: commands.Context, *, team_name):
    disc_id = str(ctx.author.id)
    userbase.addNewUser(disc_id)
    await ctx.defer(ephemeral=True)

    if embedTeamInfo(team_name) == "No team found":
        await ctx.reply("No team has been found under that name. Are you sure you typed it correctly?")
        return None
    await ctx.reply(embed=embedTeamInfo(team_name))


@client.hybrid_command(name="league", with_app_command=True, description="Returns league info", aliases=['l'])
@app_commands.guilds(discord.Object(id=1020055030247727155))
async def league(ctx: commands.Context, league_id):
    disc_id = str(ctx.author.id)
    userbase.addNewUser(disc_id)
    await ctx.defer(ephemeral=True)

    if leaguebase.leagueExist(league_id) or embedLeagueInfo(league_id) == "No league found":
        await ctx.reply("No league has been found under that ID. Are you sure you typed it correctly?")
        return None
    await ctx.reply(embed=embedLeagueInfo(league_id))


# Returns a user's roster
@client.hybrid_command(name="roster", with_app_command=True, description="Gets your fantasy roster", aliases=['r'])
# Works only on selected server (guild)
@app_commands.guilds(discord.Object(id=1020055030247727155))
# Defining roster command
# Params: ctx is defined as the command's context, user is optional field
async def roster(ctx: commands.Context, member: Member = None):
    # Reply with a private message (command) or public message (using prefix)                   implement database
    # This obtains the user's id who sent the command
    disc_id = str(ctx.author.id)
    userbase.addNewUser(disc_id)
    await ctx.defer(ephemeral=True)  # Idek what this does but it works lol
    if (member == None):
        member_ref = ctx.author
    else:
        member_ref = member

    current_page = 1

    async def page_1_callback(interaction):
        nonlocal current_page
        current_page = 1
        await interaction.response.edit_message(embed=embedRosterInfo(member_ref, current_page))

    async def page_2_callback(interaction):
        nonlocal current_page
        current_page = 2
        await interaction.response.edit_message(embed=embedRosterInfo(member_ref, current_page))

    async def page_3_callback(interaction):
        nonlocal current_page
        current_page = 3
        await interaction.response.edit_message(embed=embedRosterInfo(member_ref, current_page))

    page_1_button = Button(label="1", style=ButtonStyle.blurple)
    page_1_button.callback = page_1_callback
    page_2_button = Button(label="2", style=ButtonStyle.blurple)
    page_2_button.callback = page_2_callback
    page_3_button = Button(label="3", style=ButtonStyle.blurple)
    page_3_button.callback = page_3_callback

    view = View(timeout=180)
    view.add_item(page_1_button)
    view.add_item(page_2_button)
    view.add_item(page_3_button)
    await ctx.send(embed=embedRosterInfo(member_ref, 1), view=view, delete_after=90.0)


# Adds a player to user's roster
@client.hybrid_command(name="draft", with_app_command=True, description="Adds the selected player to your roster", aliases=['d'])
# Works only on selected server (guild)
@app_commands.guilds(discord.Object(id=1020055030247727155))
# Defining add command
# Params: ctx is defined as the command's context, player_name is the selected player
async def draft(ctx: commands.Context, player_name: str, league_number: int):
    # This obtains the user's id who sent the command
    disc_id = str(ctx.author.id)
    userbase.addNewUser(disc_id)
    # Reply with a private message (command) or public message (using prefix)                   implement database
    await ctx.defer(ephemeral=True)
    x = userbase.addPlayer(player_name, disc_id, league_number)
    if x == "No player found":
        await ctx.reply("No player has been found under that name. Are you sure you typed it correctly?")
        return None
    elif x == "Roster full":
        await ctx.reply("Roster filled!")
        return None
    await ctx.reply("Player added")


# Removes player from user's roster
@client.hybrid_command(name="drop", with_app_command=True, description="Removes the selected player from your roster", aliases=['dr'])
# Works only on selected server (guild)
@app_commands.guilds(discord.Object(id=1020055030247727155))
# Defining add command
# Params: ctx is defined as the command's context, player_name is the selected player
async def drop(ctx: commands.Context, player_name: str):
    # This obtains the user's id who sent the command
    disc_id = str(ctx.author.id)
    userbase.addNewUser(disc_id)
    # Reply with a private message (command) or public message (using prefix)                   implement database
    await ctx.defer(ephemeral=True)
    if userbase.dropPlayer(player_name, disc_id) == "No player found":
        await ctx.reply("No player has been found under that name in your roster. Are you sure you typed it correctly?")
        return None
    await ctx.reply("Player dropped")


# Removes all players from user's roster
@client.hybrid_command(name="drop-all", with_app_command=True, description="Removes all players from your roster", aliases=['da'])
# Works only on selected server (guild)
@app_commands.guilds(discord.Object(id=1020055030247727155))
# Defining add command
# Params: ctx is defined as the command's context, player_name is the selected player
async def drop_all(ctx: commands.Context):
    # This obtains the user's id who sent the command
    disc_id = str(ctx.author.id)
    userbase.addNewUser(disc_id)
    # Reply with a private message (command) or public message (using prefix)                   implement database
    await ctx.defer(ephemeral=True)
    for player in userbase.uTeamGetLeagueRoster1(disc_id):
        userbase.dropPlayer(player, disc_id)

    await ctx.reply("Roster has been dropped")


# Creates a league
@client.hybrid_command(name="create", with_app_command=True, description="Creates a league")
# Works only on selected server (guild)
@app_commands.guilds(discord.Object(id=1020055030247727155))
# Defining add command
# Params: ctx is defined as the command's context, player_name is the selected player
async def create(ctx: commands.Context, name: str):
    disc_id = str(ctx.author.id)
    # Reply with a private message (command) or publåic message (using prefix)                   implement database
    # await ctx.defer(ephemeral=True)
    try:
        leaguebase.createLeague(name, disc_id)
        await ctx.send(embed=embedLeagueInfo(leaguebase.getOwnedLeague(disc_id)), delete_after=90.0)
    except:
        await ctx.reply("Unable to create league. Perhaps the name is too long.")


# Invites a player to the league the user owns
@client.hybrid_command(name="invite", with_app_command=True, description="Invites a player to a league")
# Works only on selected server (guild)
@app_commands.guilds(discord.Object(id=1020055030247727155))
# Defining invite command
# Params: ctx is defined as the command's context, player_name is the selected player
async def invite(ctx: commands.Context, member: Member):
    try:
        if ():
            raise Exception("User already in league!")
        disc_id = str(ctx.author.id)
        # Reply with a private message (command) or public message (using prefix)                   implement database
        await ctx.defer(ephemeral=False)
        yesButton = Button(label="Accept", style=discord.ButtonStyle.green)
        noButton = Button(label="Decline", style=discord.ButtonStyle.red)
        view = View()
        view.add_item(yesButton)
        view.add_item(noButton)

        async def yesButton_callback(interaction):
            if interaction.user == member:
                nonlocal sent_msg
                leaguebase.inviteLeague(disc_id, member.id)
                view.remove_item(yesButton)
                view.remove_item(noButton)
                await sent_msg.edit(content=member.mention + " Invite Accepted!", view=view)

        async def noButton_callback(interaction):
            if interaction.user == member:
                nonlocal sent_msg
                view.remove_item(yesButton)
                view.remove_item(noButton)
                await sent_msg.edit(content=member.mention + " Invite Declined!", view=view)
        yesButton.callback = yesButton_callback
        noButton.callback = noButton_callback

        if (leaguebase.checkOwnership(disc_id)):
            sent_msg = await ctx.send(f"{member.mention} Do you want to accept the invite from league \"{leaguebase.leagueGetName(leaguebase.getOwnedLeague(disc_id))}\"?", view=view)
        else:
            raise Exception("You are not the owner of a league!")

    except Exception as e:
        await ctx.reply(e)


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

    embed = discord.Embed(title=f"{database.playerGetUserName(pname)}",
                          description=f"**{database.playerGetRealName(pname)}**\n{scraper.flagEmojis.get(database.playerGetRegion(pname))} {database.playerGetRegion(pname).lower().title()}")
    embed.set_author(name=database.playerGetTeam(
        pname), icon_url=scraper.scrapeTeamLogo(database.playerGetTeam(pname)))
    embed.set_thumbnail(url=database.playerGetPicture(pname))
    embed.add_field(
        name="ACS", value=database.playerGetGlobalACS(pname), inline=True)
    embed.add_field(
        name="K/D", value=database.playerGetGlobalKD(pname), inline=True)
    embed.add_field(name="KPR", value=database.playerGetGlobalKPR(pname))
    embed.add_field(
        name="APR", value=database.playerGetGlobalAPR(pname), inline=True)
    embed.add_field(
        name="AGENT", value=database.playerGetAgent(pname).capitalize())
    return (embed)


def embedTeamInfo(team_name: str):
    try:
        team_name = team_name.lower()
        embed = discord.Embed(
            title=f"{scraper.scrapeTeamRegionFlag(team_name)} {scraper.scrapeTeamRegion(team_name)}")
        embed.set_author(name=f"{scraper.scrapeTeamName(team_name)}")
        embed.set_thumbnail(url=scraper.scrapeTeamLogo(team_name.lower()))
        team_roster = database.teamGetPlayers(team_name).copy()

        for player in team_roster:
            pname = player.lower()
            embed.add_field(name=f"{player}", value=f"{scraper.flagEmojis.get(database.playerGetRegion(pname))} {database.playerGetRealName(pname)}\n**ACS** {database.playerGetGlobalACS(pname)} |\
                 **K/D** {database.playerGetGlobalKD(pname)}",
                            inline=False)  # Make an element for each player & display team

        return (embed)
    except:
        return ("Team not found")


def embedRosterInfo(member: Member, league: int):
    embed = discord.Embed(title=f"{member.name}'s Roster")
    embed.set_thumbnail(url=member.avatar.url)

    if (league == 1):
        roster = userbase.uTeamGetLeagueRoster1(member.id)
    elif (league == 2):
        roster = userbase.uTeamGetLeagueRoster2(member.id)
    elif (league == 3):
        roster = userbase.uTeamGetLeagueRoster3(member.id)
    else:
        return ("Invalid league")

    embed.add_field(name="STARTERS", value=f"**C**\t{roster[0]}\n**P**\t{roster[1]}\n**P**\t{roster[2]}\n**P**\t\
        {roster[3]}\n**P**\t{roster[4]}\n**P**\t{roster[5]}\n", inline=False)
    embed.add_field(
        name="BENCH", value=f"\n**BE**\t{roster[6]}\n**BE**\t{roster[7]}\n**BE**\t{roster[8]}\n", inline=False)
    return (embed)


def embedLeagueInfo(league_id):
    try:
        league_name = leaguebase.leagueGetName(league_id)
        league_owner_id = leaguebase.leagueGetOwnerID(league_id)
        embed = discord.Embed(
            title=f"\"{league_name}\"", description=f"**Owner ID:** {league_owner_id}")
        embed.add_field(name="Leauge ID:", value=f"{league_id}", inline=False)
        return (embed)
    except:
        return "No league found with that ID. Are you sure you typed it correctly?"

# Getter Methods                                                                                                          ***TO BE ADDED TO DB.PY***

# Method returns average player ACS over course of match
# Pulled from match
# EX: getPlayerMatchACS()


def getPlayerMatchACS(match, player_name):
    for player_stats in database.getPlayerStats(match):
        if player_stats[0].lower() == player_name.lower():
            return player_stats[1]


# Kills/one taps the bot so we can work on it
# VERY VERY IMPORTANT DELETE THIS BEFORE THIS GOES PUBLIC
@client.command(aliases=['onetap', 'mavenawpshot', 'stirfriedsatchelpeak'])
# Online usable by a server admin
@commands.has_permissions(administrator=True)
async def shutdown(ctx):
    exit()  # Ends the program, bot will go offline

# Runs bot
client.run(TOKEN)


# Methods that interface with discord.py

# Team info method
# Returns an embed with respective team information
# Usage: await ctx.reply(embed = embedTeamInfo(team_name))
# embedTeamInfo(team_name) will return embed
# def embedTeamInfo(team_name):
#     embed=discord.Embed(title=f"{getTeamName(team_name)}",description=f"**{getTeamAbbreviation(team_name)}**\n{getTeamRegionFlag(team_name)} {getTeamRegion(team_name).lower().title()}") # This cannot be implemented until these methods are added
#     embed.set_thumbnail(url=getTeamLogo(team_name))
#     # For loop here for each player to be listed, inline 2 wide
#     return (embed)

# Player info method                                                                                                          ***TO BE ADDED TO DB.PY***
# Returns an embed with respective player information
# Usage: await ctx.reply(embed = embedPlayerInfo(player_name))
# embedPlayerInfo(player_name) will return embed
