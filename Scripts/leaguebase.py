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
        self.mycursor = self.db.cursor()

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
        user_id = 0
        output = []
        print("Command initiated by: " + discord_id)
        userbase.mycursor.execute("SELECT userID FROM UserInfo WHERE discID = %s", (discord_id,))
        for x in userbase.mycursor:
            user_id = x[0]
            print("This is at L46: " + str(user_id))
        self.mycursor.execute("INSERT into LeagueInfo (ownerID, ownerdisc_id, leagueName) VALUES(%s,%s,%s)", (user_id,discord_id,name))
        self.mycursor.execute("SELECT users FROM LeagueInfo WHERE ownerID = %s", (user_id,))
        for x in self.mycursor:
            output = x[0].split(",")
        emptyIndex = output.index("Missing")
        output[emptyIndex] = str(user_id)
        output = ",".join(output)
        self.mycursor.execute("UPDATE LeagueInfo SET users = %s WHERE leagueName = %s", (output,name))
        print("Owner: " + str(user_id) + " | " + discord_id + " named league " + name)
        self.db.commit()
        print("This is at L59: "+ str(user_id))
        return("League Created; Owner: " + str(user_id) + ", " + discord_id + " league name: " + name)
    
    def inviteLeague(self, disc_id : str, odisc_id : str):
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
        
        
        


leg = LeagueBase()
leg.createTable()
userbase.createTable()
userbase.addNewUser("343")
userbase.addNewUser("353")
leg.createLeague("somenuts", "343")
leg.createLeague("phatnuts", "353")