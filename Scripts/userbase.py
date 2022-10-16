from itertools import count
import mysql.connector
import logging
from database import Database

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

    ###CREATES TABLE USER & USERTEAM IF THEY DO NOT EXIST
    def createTable(self):
        self.mycursor.execute("DROP TABLE IF EXISTS UserGameData")
        self.mycursor.execute("DROP TABLE IF EXISTS UserInfo")
        self.mycursor.execute("""CREATE TABLE IF NOT EXISTS UserInfo(
                        userID int AUTO_INCREMENT,
                        discID VARCHAR(20) UNIQUE KEY,
                        email VARCHAR(50) UNIQUE KEY,
                        username VARCHAR(30) UNIQUE KEY,
                        PRIMARY KEY(userID)) ENGINE = INNODB
                        """)
        self.mycursor.execute("""CREATE TABLE IF NOT EXISTS UserGameData (
                        userID int,
                        leagueID VARCHAR(30) DEFAULT '-1' NOT NULL,
                        leagueRoster1 VARCHAR(70) DEFAULT 'Missing,Missing,Missing,Missing,Missing' NOT NULL,
                        leagueRoster2 VARCHAR(70) DEFAULT '' NOT NULL,
                        leagueRoster3 VARCHAR(70) DEFAULT '' NOT NULL,
                        leaguePoints1 int DEFAULT 0 NOT NULL,
                        leaguePoints2 int DEFAULT 0 NOT NULL,
                        leaguePoints3 int DEFAULT 0 NOT NULL)
                        ENGINE = INNODB
                        """)
        self.mycursor.execute("ALTER TABLE UserGameData ADD CONSTRAINT FK_UserGameData FOREIGN KEY(userID) REFERENCES UserInfo(userID) ON UPDATE CASCADE ON DELETE CASCADE")
        self.db.commit()

    #CHECKS THE USER TABLE FOR THE DISCORD ID PASSED TO THE FUNCTION
    #IF IT IS FOUND DOES NOTHING AND RETURNS FALSE
    #IF NOT FOUND RETURNS TRUE -- REFERENCE ADD NEW USER

    def checkForUser(self, discID: str):
        self.mycursor.execute("SELECT EXISTS(SELECT discID FROM UserInfo WHERE discID = %s)", (discID,))
        for x in self.mycursor:
            if(x[0] == 1):
                print("User Found")
                return False
            else:
                print("Proceeding...")
                logging.info("User not found creating a table entry...")
                return True

    #IF CHECK FOR USER RETURNS TRUE CREATES AN ENTRY IN BOTH TABLES FOR THEIR DISC ID

    def addNewUser(self, discID: str):
        if(self.checkForUser(discID)):
            self.mycursor.execute("INSERT into UserInfo (discID) VALUES (%s)", (discID,))
            x = self.mycursor.lastrowid
            self.mycursor.execute("INSERT into UserGameData (userID) VALUES (%s)", (x,))
            self.db.commit()
            self.mycursor.execute("SELECT discID FROM UserInfo WHERE discID = %s", (discID,))
            for x in self.mycursor:
                print("Was added to the UserInfo Table " + x[0])
        logging.info("Added a user %s to UserInfo Table and created discordID", (discID))

    
    '''def userGetDiscordID(self, name: str):
        self.mycursor.execute("SELECT discordID FROM Users WHERE userName = %s", (name,))
        for x in self.mycursor:
            return x[0]'''

    ##################################
    # GETTER METHODS FROM THE TABLES #
    ##################################
    def userGetPlayerName(self, name: str):
        self.mycursor.execute("SELECT username FROM Users WHERE discID = %s", (name,))
        for x in self.mycursor:
            return x[0]

    def userGetTeamName(self, name: str):
        self.mycursor.execute("SELECT pTeamName FROM Users WHERE discID = %s", (name,))
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
        self.mycursor.execute("SELECT userID FROM UserInfo WHERE discID = %s", (name,))
        for x in self.mycursor:
            uref = x[0]
        self.mycursor.execute("SELECT leagueID FROM UserGameData WHERE userID = %s", (uref,))
        for x in self.mycursor:
            return x[0]

    def uTeamGetCoach(self, name: str):
        self.mycursor.execute("SELECT coach FROM UserTeam WHERE discordID = %s", (name,))
        for x in self.mycursor:
            return x[0]

    # returns an array 
    def getLgRoster1(self, discordID: str) -> list:
        output = []
        self.mycursor.execute("SELECT userID FROM UserInfo WHERE discID = %s", (discordID,))
        for x in self.mycursor:
            uref = x[0]
        self.mycursor.execute("SELECT leagueRoster1 FROM UserGameData WHERE userID = %s", (uref,))
        for x in self.mycursor:
            output = x[0].split(",")
        return output
    '''output = []
    output.append(self.uTeamGetPlayerOne(user_id))
    output.append(self.uTeamGetPlayerTwo(user_id))
    output.append(self.uTeamGetPlayerThree(user_id))
    output.append(self.uTeamGetPlayerFour(user_id))
    output.append(self.uTeamGetPlayerFive(user_id))
    return output'''

    
    ##################
    # SETTER METHODS #
    ##################

    def addPlayer(self, player_name: str, discID: str):
        pname = None
        for dName in database.playerNames:
            if (player_name.lower() == dName.lower()):
                pname = dName
                break
        if (pname == None):
            return "No player found"
        #THIS IF STATEMENT DOES NOTHING V
        if ("Missing" not in self.getLgRoster1(discID)):
            return "Roster full"

        #for i in range(self.getLgRoster1(discID)):
        count = 0
        temp = self.getLgRoster1(discID)
        emptyIndex = temp.index("Missing")
        temp[emptyIndex] = pname
        s = ""
        for i in temp:
            count += 1
            if(count<5):
                s += i + ","
            else:
                s += i
        print(s)
        self.mycursor.execute("SELECT userID FROM UserInfo WHERE discID = %s", (discID,))
        for x in self.mycursor:
            uref = x[0]
        self.mycursor.execute("UPDATE UserGameData SET leagueRoster1 = %s WHERE userID = %s", (s,uref))


        '''if(self.uTeamGetPlayerOne(discID) == "Missing"):
            self.mycursor.execute("UPDATE UserTeam SET playerOne = %s WHERE discordID = %s", (pname, discID,))

        elif(self.uTeamGetPlayerTwo(discID) == "Missing"):
            self.mycursor.execute("UPDATE UserTeam SET playerTwo = %s WHERE discordID = %s", (pname, discID,))
            
        elif(self.uTeamGetPlayerThree(discID) == "Missing"):
            self.mycursor.execute("UPDATE UserTeam SET playerThree = %s WHERE discordID = %s", (pname, discID,))
            
        elif(self.uTeamGetPlayerFour(discID) == "Missing"):
            self.mycursor.execute("UPDATE UserTeam SET playerFour = %s WHERE discordID = %s", (pname, discID,))
            
        elif(self.uTeamGetPlayerFive(discID) == "Missing"):
            self.mycursor.execute("UPDATE UserTeam SET playerFive = %s WHERE discordID = %s", (pname, discID,))'''
        
        print("Proceeding...")
        self.db.commit()


    def dropPlayer(self, player_name: str, discID: str):

        pname = None
        for dName in database.playerNames:
            if (player_name.lower() == dName.lower()):
                pname = dName
                break
        if (pname == None):
            return "No player found"
        #THIS IF STATEMENT DOES NOTHING V
        if ("Missing" not in self.getLgRoster1(discID)):
            return "Roster full"

        #for i in range(self.getLgRoster1(discID)):
        count = 0
        temp = self.getLgRoster1(discID)
        emptyIndex = temp.index(pname)
        temp[emptyIndex] = "Missing"
        s = ""
        for i in temp:
            count += 1
            if(count<5):
                s += i + ","
            else:
                s += i
        print(s)
        self.mycursor.execute("SELECT userID FROM UserInfo WHERE discID = %s", (discID,))
        for x in self.mycursor:
            uref = x[0]
        self.mycursor.execute("UPDATE UserGameData SET leagueRoster1 = %s WHERE userID = %s", (s,uref))

        print("Proceeding...")
        self.db.commit()


    ##################
    # HELPER METHODS #
    ##################    

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



#TESTING

'''userb = Userbase()
s = ""
a = ""
y = 0
userb.createTable()
userb.addNewUser("328309041518608385")
userb.addNewUser("328309041518608385")
userb.addNewUser("283407511133093889")
print(userb.uTeamGetLeagueID("328309041518608385"))
print(userb.getLgRoster1("328309041518608385"))
print(a.join(userb.getLgRoster1("328309041518608385")))
for i in userb.getLgRoster1("328309041518608385"):
    y += 1
    if(y<5):
        s += i + ","
    else:
        s += i
print(s)
print("__________________")
userb.addPlayer("yay", "328309041518608385")
userb.addPlayer("stellar", "328309041518608385")
userb.addPlayer("yay", "328309041518608385")
userb.addPlayer("stellar", "328309041518608385")
userb.addPlayer("yay", "328309041518608385")
userb.addPlayer("stellar", "328309041518608385")
userb.addPlayer("who", "328309041518608385")'''
    

#userb.mycursor.execute("INSERT into UserInfo (discID) VALUES (%s)", ("328309041518608385",))
'''
x = userb.mycursor.lastrowid
userb.mycursor.execute("INSERT into UserGameData (leagueID) VALUES (%s)", (2,))
userb.mycursor.execute("INSERT into UserGameData (leagueID) VALUES (%s)", (2,))
userb.mycursor.execute("INSERT into UserGameData (leagueID,userID) VALUES (%s,%s)", (1,x))
userb.mycursor.execute("INSERT into UserInfo (discID) VALUES (%s)", ("3r153513312",))
x = userb.mycursor.lastrowid
userb.mycursor.execute("INSERT into UserGameData (leagueID,userID) VALUES (%s,%s)", (1,4))'''

#userb.db.commit()
'''
userb.addNewUser("328309041518608385")
userb.addNewUser("280100023050436609")
userb.addNewUser("735656344966660147")
userb.addNewUser("283407511133093889")
#print("P4 " + userb.uTeamGetPlayerOne("328309041518608385"))
userb.addPlayer("stellar", "328309041518608385")
userb.addPlayer("yay", "280100023050436609")
userb.addPlayer("Tenz", "328309041518608385")
userb.addPlayer("cyrocells", "735656344966660147")
userb.addPlayer("yay", "283407511133093889")
#print(userb.uTeamGetPlayers("328309041518608385")[0])'''
