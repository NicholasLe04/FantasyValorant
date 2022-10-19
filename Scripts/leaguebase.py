from discord import User
import mysql.connector
import logging
from database import Database
from userbase import Userbase

database = Database()
userbase = Userbase()

class LeagueBase():

    ##CONNECTING TO LOCALLY HOSTED SQL SERVER
    ##AVOID RUNNING CODE UNTIL SQL SERVER SORTED OUT

    def __init__(self) -> None:
        
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="SavestaAQT100%",
            database="FantasyLeague"
        )
        self.logging = logging.basicConfig(filename = 'logging.log', format = '`%(asctime)s %(message)s' , level = logging.INFO)
        self.mycursor = self.db.cursor(buffered=True)

    ###CREATES TABLE USER & USERTEAM IF THEY DO NOT EXIST
    def createTable(self):
        self.mycursor.execute("DROP TABLE IF EXISTS LeagueInfo")
        self.mycursor.execute("""CREATE TABLE IF NOT EXISTS LeagueInfo(
                        leagueID int AUTO_INCREMENT,
                        ownerID int UNIQUE KEY,
                        ownerdisc_id VARCHAR(20) UNIQUE KEY,
                        draftDate Date,
                        users VARCHAR(255) DEFAULT 'Missing,Missing,Missing,Missing,Missing,Missing,Missing,Missing,Missing,Missing',
                        draftTurn VARCHAR(20) DEFAULT 'none',
                        leagueName VARCHAR(20) DEFAULT 'noname' UNIQUE KEY,
                        PRIMARY KEY(leagueID)) ENGINE = INNODB
                        """)
        self.mycursor.execute("ALTER TABLE LeagueInfo AUTO_INCREMENT=100")
        self.db.commit()
    
    def createLeague(self, name : str, discord_id : str):
        userbase.addNewUser(discord_id)
        user_id = 0
        output = []

        userbase.mycursor.execute("SELECT userID FROM UserInfo WHERE discID = %s", (discord_id,))
        for x in userbase.mycursor:
            user_id = x[0]

        self.mycursor.execute("INSERT into LeagueInfo (ownerID, ownerdisc_id, leagueName) VALUES(%s,%s,%s)", (user_id,discord_id,name))
        self.mycursor.execute("SELECT users FROM LeagueInfo WHERE ownerID = %s", (user_id,))
        for x in self.mycursor:
            output = x[0].split(",")
        emptyIndex = output.index("Missing")
        output[emptyIndex] = str(user_id)
        output = ",".join(output)

        self.mycursor.execute("UPDATE LeagueInfo SET users = %s WHERE leagueName = %s", (output,name))
        self.db.commit()
        # return("League Created; Owner: " + str(user_id) + ", " + discord_id + " league name: " + name)

    def checkOwnership (self, disc_id : str):
        self.mycursor.execute ("SELECT EXISTS (SELECT ownerID From LeagueInfo WHERE ownerdisc_id = %s)", (disc_id,))
        isOwner = 0
        for x in self.mycursor:
            isOwner = x[0]
        if (isOwner == 1):
            return True
        else:
            return False
    
    def getOwnedLeague (self, disc_id : str):
        if (self.checkOwnership(disc_id)):
            self.mycursor.execute("SELECT leagueID FROM LeagueInfo WHERE ownerdisc_id = %s", (disc_id,))
            for x in self.mycursor:
                return x[0]
        else:
            return None

    def getPlayers(self, disc_id):
        players = []
        user_id = 0
        userbase.mycursor.execute("SELECT userID FROM UserInfo WHERE discID = %s", (disc_id,))
        for x in userbase.mycursor:
            user_id = x[0]
        self.mycursor.execute("SELECT users FROM LeagueInfo WHERE ownerID = %s", (user_id,))
        for x in self.mycursor:
            players = x[0].split(",")
        print("These players belong to league owned by: " + str(user_id) + " | " + str(players))
        return(players)

    
    def initDraft(self, disc_id):
        print("a")
    
    def inviteLeague(self, disc_id : str, odisc_id : str):
        if (self.checkOwnership(disc_id)):
            userbase.addNewUser(disc_id)
            userbase.addNewUser(odisc_id)
            self.mycursor.execute("SELECT ownerID From LeagueInfo WHERE ownerdisc_id = %s", (disc_id,))
            user_id = 0
            ouser_id = 0
            output = []
            for x in self.mycursor:
                user_id = x[0]
            userbase.mycursor.execute("SELECT userID FROM UserInfo WHERE discID = %s", (odisc_id,))
            for x in userbase.mycursor:
                ouser_id = x[0]
            self.mycursor.execute("SELECT users FROM LeagueInfo WHERE ownerID = %s", (user_id,))
            for x in self.mycursor:
                output = x[0].split(",")
            emptyIndex = output.index("Missing")
            print(emptyIndex)
            print(ouser_id)
            print(user_id)
            output[emptyIndex] = str(ouser_id)
            output = ",".join(output)
            self.mycursor.execute("UPDATE LeagueInfo SET users = %s WHERE ownerID = %s", (output,user_id))
            self.db.commit()
            self.mycursor.execute("SELECT leagueName FROM LeagueInfo WHERE ownerID = %s", (user_id,))
        
    def leagueGetName (self, league_id):
        self.mycursor.execute("SELECT leagueName FROM LeagueInfo WHERE leagueID = %s", (league_id,))
        for x in self.mycursor:
            return x[0]

    def leagueGetOwnerID (self, league_id):
        self.mycursor.execute("SELECT ownerID FROM LeagueInfo WHERE leagueID = %s", (league_id,))
        for x in self.mycursor:
            return x[0]

    def leagueExist(self, league_id):
        self.mycursor.execute("SELECT EXISTS(SELECT * from LeagueInfo WHERE leagueID = %s)", (league_id,))
        for x in self.mycursor:
            if (x[0] == 0):
                return False
            else:
                return True

leg = LeagueBase()
leg.createTable()