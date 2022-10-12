from tabnanny import check
import mysql.connector
import logging
from db import Database

database = Database()

class Userbase():

    ##CONNECTING TO LOCALLY HOSTED SQL SERVER
    ##AVOID RUNNING CODE UNTIL SQL SERVER SORTED OUT

    def __init__(self) -> None:
        
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="SavestaAQT100%",
            database="FantasyUsers"
        )
        self.logging = logging.basicConfig(filename = 'logging.log', format = '`%(asctime)s %(message)s' , level = logging.INFO)
        self.mycursor = self.db.cursor()

    def createTable(self):
        self.mycursor.execute("""CREATE TABLE IF NOT EXISTS Users (discordID VARCHAR(20) PRIMARY KEY,
                        pTeamName VARCHAR(30) DEFAULT 'no name' NOT NULL,
                        points int DEFAULT 0 NOT NULL,
                        userID int AUTO_INCREMENT UNIQUE KEY)""")
                        
        self.mycursor.execute("""CREATE TABLE IF NOT EXISTS UserTeam (teamID VARCHAR(20) PRIMARY KEY,
                        leagueID VARCHAR(16) DEFAULT '-1' NOT NULL,
                        playerTeam VARCHAR(40) DEFAULT 'userTeam' NOT NULL,
                        coach VARCHAR(25) DEFAULT 'Missing' NOT NULL,
                        playerOne VARCHAR(20) DEFAULT 'Missing' NOT NULL,
                        playerTwo VARCHAR(20) DEFAULT 'Missing' NOT NULL,
                        playerThree VARCHAR(20) DEFAULT 'Missing' NOT NULL,
                        playerFour VARCHAR(20) DEFAULT 'Missing' NOT NULL,
                        playerFive VARCHAR(20) DEFAULT 'Missing' NOT NULL,
                        FOREIGN KEY(teamID) REFERENCES Users(discordID))
                        """)
        self.db.commit()
    
    def checkForUser(self, discID: str):
        self.mycursor.execute("SELECT EXISTS(SELECT discordID FROM Users WHERE discordID = %s)", (discID,))
        for x in self.mycursor:
            if(x[0] == 1):
                print("User Found")
                return False
            else:
                print("Proceeding...")
                logging.info("User not found creating a table entry...")
                return True

    def addNewUser(self, discID: str):
        if(self.checkForUser(discID)):
            self.mycursor.execute("INSERT into Users (discordID) VALUES (%s)", (discID,))
            self.mycursor.execute("INSERT into UserTeam (teamID) VALUES (%s)", (discID,))
            self.mycursor.execute("SELECT discordID FROM Users WHERE discordID = %s", (discID,))
            for x in self.mycursor:
                print("Was added to the Users Table " + x[0])
            self.db.commit()
        logging.info("Added a user %s to User Table and created TeamID", (discID))

    
    '''def userGetDiscordID(self, name: str):
        self.mycursor.execute("SELECT discordID FROM Users WHERE userName = %s", (name,))
        for x in self.mycursor:
            return x[0]'''

    def userGetPlayerName(self, name: str):
        self.mycursor.execute("SELECT playerName FROM Users WHERE discordID = %s", (name,))
        for x in self.mycursor:
            return x[0]

    def userGetTeamName(self, name: str):
        self.mycursor.execute("SELECT pTeamName FROM Users WHERE discordID = %s", (name,))
        for x in self.mycursor:
            return x[0]

    def userGetPoints(self, name: str):
        self.mycursor.execute("SELECT points FROM Users WHERE discordID =%s", (name,))
        for x in self.mycursor:
            return x[0]

    def userGetUserID(self, name: str):
        self.mycursor.execute("SELECT userID FROM Users WHERE discordID = %s", (name,))
        for x in self.mycursor:
            return x[0]
    '''
    def uTeamGetTeamID(self, name: str):
        self.mycursor.execute("SELECT teamID FROM UserTeam WHERE discordID = %s", (name,))
        for x in self.mycursor:
            return x[0]'''

    def uTeamGetLeagueID(self, name: str):
        self.mycursor.execute("SELECT leagueID FROM UserTeam WHERE teamID = %s", (name,))
        for x in self.mycursor:
            return x[0]

    def uTeamGetCoach(self, name: str):
        self.mycursor.execute("SELECT coach FROM UserTeam WHERE teamID = %s", (name,))
        for x in self.mycursor:
            return x[0]

    def uTeamGetPlayers(self, name: str):
        self.mycursor.execute("SELECT playerOne, playerTwo, playerThree, playerFour, playerFive FROM UserTeam WHERE teamID = %s", (name,))
        for x in self.mycursor:
            print(x)
            return x

    '''def uTeamGetPlayerTwo(self, name: str):
        self.mycursor.execute("SELECT playerTwo FROM UserTeam WHERE teamID = %s", (name,))
        for x in self.mycursor:
            return x[0]
    
    def uTeamGetPlayerThree(self, name: str):
        self.mycursor.execute("SELECT playerThree FROM UserTeam WHERE teamID = %s", (name,))
        for x in self.mycursor:
            return x[0]
    
    def uTeamGetPlayerFour(self, name: str):
        self.mycursor.execute("SELECT playerFour FROM UserTeam WHERE teamID = %s", (name,))
        for x in self.mycursor:
            return x[0]
    
    def uTeamGetPlayerFive(self, name: str):
        self.mycursor.execute("SELECT playerFive FROM UserTeam WHERE teamID = %s", (name,))
        for x in self.mycursor:
            return x[0]'''

    def addPlayer(self, name: str, discID: str, pos: int):
        pname = None

        for dName in database.playerNames:
            if (name.lower() == dName.lower()):
                pname = dName
                break

        if (pname == None):
            return "No player found"

        if(pos == 1):
            self.mycursor.execute("UPDATE UserTeam SET playerOne = %s WHERE teamID = %s", (pname, discID,))
            print("Proceeding...")
            self.db.commit()
        elif(pos == 2):
            self.mycursor.execute("UPDATE UserTeam SET playerTwo = %s WHERE teamID = %s", (pname, discID,))
            print("Proceeding...")
            self.db.commit()
        elif(pos == 3):
            self.mycursor.execute("UPDATE UserTeam SET playerThree = %s WHERE teamID = %s", (pname, discID,))
            print("Proceeding...")
            self.db.commit()
        elif(pos == 4):
            self.mycursor.execute("UPDATE UserTeam SET playerFour = %s WHERE teamID = %s", (pname, discID,))
            print("Proceeding...")
            self.db.commit()
        elif(pos == 5):
            self.mycursor.execute("UPDATE UserTeam SET playerFive = %s WHERE teamID = %s", (pname, discID,))
            print("Proceeding...")
            self.db.commit()
        else:
            return "Invalid position"
            
        

#TESTING

userb = Userbase()