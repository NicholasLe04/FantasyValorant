from tabnanny import check
import mysql.connector
import logging
from Scripts.bot import player
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
        self.mycursor.execute("""CREATE TABLE IF NOT EXISTS Users (discordID VARCHAR(20),CONSTRAINT userteam_ibfk_1 PRIMARY KEY(discordID),
                        pTeamName VARCHAR(30) DEFAULT 'no name' NOT NULL,
                        points int DEFAULT 0 NOT NULL,
                        userID int AUTO_INCREMENT UNIQUE KEY) ENGINE = INNODB""")
                        
        self.mycursor.execute("""CREATE TABLE IF NOT EXISTS UserTeam (discordID VARCHAR(20),
                        PRIMARY KEY (discordID),
                        FOREIGN KEY(discordID) REFERENCES Users(discordID) ON UPDATE CASCADE,
                        leagueID VARCHAR(16) DEFAULT '-1' NOT NULL,
                        playerTeam VARCHAR(40) DEFAULT 'userTeam' NOT NULL,
                        coach VARCHAR(25) DEFAULT 'Missing' NOT NULL,
                        playerOne VARCHAR(20) DEFAULT 'Missing' NOT NULL,
                        playerTwo VARCHAR(20) DEFAULT 'Missing' NOT NULL,
                        playerThree VARCHAR(20) DEFAULT 'Missing' NOT NULL,
                        playerFour VARCHAR(20) DEFAULT 'Missing' NOT NULL,
                        playerFive VARCHAR(20) DEFAULT 'Missing' NOT NULL) ENGINE = INNODB
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
            self.mycursor.execute("INSERT into UserTeam (discordID) VALUES (%s)", (discID,))
            self.db.commit()
            self.mycursor.execute("SELECT discordID FROM Users WHERE discordID = %s", (discID,))
            for x in self.mycursor:
                print("Was added to the Users Table " + x[0])
        logging.info("Added a user %s to User Table and created discordID", (discID))

    
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
        self.mycursor.execute("SELECT leagueID FROM UserTeam WHERE discordID = %s", (name,))
        for x in self.mycursor:
            return x[0]

    def uTeamGetCoach(self, name: str):
        self.mycursor.execute("SELECT coach FROM UserTeam WHERE discordID = %s", (name,))
        for x in self.mycursor:
            return x[0]

    # returns an array 
    def uTeamGetPlayers(self, user_id: str) -> list:
        output = []
        output.append(self.uTeamGetPlayerOne(user_id))
        output.append(self.uTeamGetPlayerTwo(user_id))
        output.append(self.uTeamGetPlayerThree(user_id))
        output.append(self.uTeamGetPlayerFour(user_id))
        output.append(self.uTeamGetPlayerFive(user_id))
        return output

    def uTeamGetPlayerOne(self, user_id: str) -> str:
        self.mycursor.execute("SELECT playerOne FROM UserTeam WHERE discordID = %s", (str(user_id),))
        for x in self.mycursor:
            return x[0]

    def uTeamGetPlayerTwo(self, user_id: str) -> str:
        self.mycursor.execute("SELECT playerTwo FROM UserTeam WHERE discordID = %s", (user_id,))
        for x in self.mycursor:
            return x[0]
    
    def uTeamGetPlayerThree(self, user_id: str) -> str:
        self.mycursor.execute("SELECT playerThree FROM UserTeam WHERE discordID = %s", (user_id,))
        for x in self.mycursor:
            return x[0]
    
    def uTeamGetPlayerFour(self, user_id: str) -> str:
        self.mycursor.execute("SELECT playerFour FROM UserTeam WHERE discordID = %s", (user_id,))
        for x in self.mycursor:
            return x[0]
    
    def uTeamGetPlayerFive(self, user_id: str) -> str:
        self.mycursor.execute("SELECT playerFive FROM UserTeam WHERE discordID = %s", (user_id,))
        for x in self.mycursor:
            return x[0]

    def addPlayer(self, player_name: str, discID: str):
        pname = None

        for dName in database.playerNames:
            if (player_name.lower() == dName.lower()):
                pname = dName
                break
        if (pname == None):
            return "No player found"
        if(self.uTeamGetPlayerOne(discID) == "Missing"):
            self.mycursor.execute("UPDATE UserTeam SET playerOne = %s WHERE discordID = %s", (pname, discID,))
            print("Proceeding...")
            self.db.commit()
        elif(self.uTeamGetPlayerTwo(discID) == "Missing"):
            self.mycursor.execute("UPDATE UserTeam SET playerTwo = %s WHERE discordID = %s", (pname, discID,))
            print("Proceeding...")
            self.db.commit()
        elif(self.uTeamGetPlayerThree(discID) == "Missing"):
            self.mycursor.execute("UPDATE UserTeam SET playerThree = %s WHERE discordID = %s", (pname, discID,))
            print("Proceeding...")
            self.db.commit()
        elif(self.uTeamGetPlayerFour(discID) == "Missing"):
            self.mycursor.execute("UPDATE UserTeam SET playerFour = %s WHERE discordID = %s", (pname, discID,))
            print("Proceeding...")
            self.db.commit()
        elif(self.uTeamGetPlayerFive(discID) == "Missing"):
            self.mycursor.execute("UPDATE UserTeam SET playerFive = %s WHERE discordID = %s", (pname, discID,))
            print("Proceeding...")
            self.db.commit()
        else:
            return("Roster full")

    def dropPlayer(self, player_name: str, discID: str):
        if(self.uTeamGetPlayerOne(discID) == player_name):
            self.mycursor.execute("UPDATE UserTeam SET playerOne = %s WHERE discordID = %s", ("Missing", discID,))
            print("Proceeding...")
            self.db.commit()
        elif(self.uTeamGetPlayerTwo(discID) == player_name):
            self.mycursor.execute("UPDATE UserTeam SET playerTwo = %s WHERE discordID = %s", ("Missing", discID,))
            print("Proceeding...")
            self.db.commit()
        elif(self.uTeamGetPlayerThree(discID) == player_name):
            self.mycursor.execute("UPDATE UserTeam SET playerThree = %s WHERE discordID = %s", ("Missing", discID,))
            print("Proceeding...")
            self.db.commit()
        elif(self.uTeamGetPlayerFour(discID) == player_name):
            self.mycursor.execute("UPDATE UserTeam SET playerFour = %s WHERE discordID = %s", ("Missing", discID,))
            print("Proceeding...")
            self.db.commit()
        elif(self.uTeamGetPlayerFive(discID) == player_name):
            self.mycursor.execute("UPDATE UserTeam SET playerFive = %s WHERE discordID = %s", ("Missing", discID,))
            print("Proceeding...")
            self.db.commit()
        else:
            return("No player found")
        

#TESTING

userb = Userbase()
userb.createTable()
'''userb.addNewUser("328309041518608385")
print("P4 " + userb.uTeamGetPlayerOne("328309041518608385"))
userb.addPlayer("yay", "328309041518608385")
userb.addPlayer("yay", "328309041518608385")
userb.addPlayer("yay", "328309041518608385")
userb.addPlayer("yay", "328309041518608385")
userb.addPlayer("yay", "328309041518608385")
print(userb.uTeamGetPlayers("328309041518608385")[0])'''
