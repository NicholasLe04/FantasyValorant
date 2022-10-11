import mysql.connector
import logging

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
        self.mycursor.execute("""CREATE TABLE Users (discordID VARCHAR(20) PRIMARY KEY,
                        pTeamName VARCHAR(30) DEFAULT 'no name' NOT NULL,
                        points int DEFAULT 0 NOT NULL,
                        userID int PRIMARY KEY AUTO_INCREMENT)""")
                        
        self.mycursor.execute("""CREATE TABLE UserTeam (teamID int PRIMARY KEY, FOREIGN KEY(teamID) REFERENCES Users(discordID),
                        leagueID VARCHAR(16) DEFAULT '-1' NOT NULL,
                        playerTeam VARCHAR(40) DEFAULT 'userTeam' NOT NULL,
                        coach VARCHAR(25) DEFAULT 'Missing' NOT NULL,
                        playerOne VARCHAR(20) DEFAULT 'Missing' NOT NULL,
                        playerTwo VARCHAR(20) DEFAULT 'Missing' NOT NULL,
                        playerThree VARCHAR(20) DEFAULT 'Missing' NOT NULL,
                        playerFour VARCHAR(20) DEFAULT 'Missing' NOT NULL,
                        playerFive VARCHAR(20) DEFAULT 'Missing' NOT NULL)
                        """)
        self.db.commit()

    def addNewUser(self, discID: str):
        self.mycursor.execute("INSERT into Users (discordID) VALUES (%s)", (discID,))
        self.mycursor.execute("SELECT discordID FROM Users WHERE discordID = %s", (discID,))
        for x in self.mycursor:
            print("Was added to the Users Table " + x[0])
        self.db.commit()
        logging.info("Added a user %s to User Table", (discID))
    
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
        self.mycursor.execute("SELECT teamID FROM userTeams WHERE discordID = %s", (name,))
        for x in self.mycursor:
            return x[0]'''

    def uTeamGetLeagueID(self, name: str):
        self.mycursor.execute("SELECT leagueID FROM userTeams WHERE teamID = %s", (name,))
        for x in self.mycursor:
            return x[0]

    def uTeamGetCoach(self, name: str):
        self.mycursor.execute("SELECT coach FROM userTeams WHERE teamID = %s", (name,))
        for x in self.mycursor:
            return x[0]

    def uTeamGetPlayerOne(self, name: str):
        self.mycursor.execute("SELECT playerOne FROM userTeams WHERE teamID = %s", (name,))
        for x in self.mycursor:
            return x[0]

    def uTeamGetPlayerTwo(self, name: str):
        self.mycursor.execute("SELECT playerTwo FROM userTeams WHERE teamID = %s", (name,))
        for x in self.mycursor:
            return x[0]
    
    def uTeamGetPlayerThree(self, name: str):
        self.mycursor.execute("SELECT playerThree FROM userTeams WHERE teamID = %s", (name,))
        for x in self.mycursor:
            return x[0]
    
    def uTeamGetPlayerFour(self, name: str):
        self.mycursor.execute("SELECT playerFour FROM userTeams WHERE teamID = %s", (name,))
        for x in self.mycursor:
            return x[0]
    
    def uTeamGetPlayerFive(self, name: str):
        self.mycursor.execute("SELECT playerFive FROM userTeams WHERE teamID = %s", (name,))
        for x in self.mycursor:
            return x[0]

#TESTING

userb = Userbase()
userb.createTable()
userb.addNewUser("328309041518608385")