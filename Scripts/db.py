import mysql.connector
from VCTDataScraper.scrape import Scraper
import json
import os

class Database():

    ##CONNECTING TO LOCALLY HOSTED SQL SERVER
    ##AVOID RUNNING CODE UNTIL SQL SERVER SORTED OUT

    def __init__(self) -> None:
        
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="SavestaAQT100%",
            database="FantasyValorant"
        )
        
        file_dir = os.path.dirname(__file__)
        playerlist_dir = os.path.join(file_dir, 'VCTDataScraper/JsonFiles/playerlist.json')
        self.mycursor = self.db.cursor()
        self.playeridJson = open(playerlist_dir)
        self.data = json.load(self.playeridJson)
        self.scrape = Scraper() #Declaring Scrapper object
        self.playerNames = []
        for i in self.data.get('players'):
            self.playerNames.append(i)

        

    def APOCALYPSE(self):
        self.mycursor.execute("DROP TABLE Players")
        self.mycursor.execute("DROP TABLE UserTeam")
        self.mycursor.execute("DROP TABLE Users")

    ## CREATING A DATA TABLE NAMED PLAYERS
    # Commented out as datatable has already been created locally on Joshua's Laptop
    def createTable(self):
        self.mycursor.execute("""CREATE TABLE Players (userName VARCHAR(25) DEFAULT 'noname' NOT NULL,
                        realName VARCHAR(30) DEFAULT 'noname' NOT NULL,
                        team VARCHAR(20) DEFAULT 'noname' NOT NULL,
                        country VARCHAR(25) DEFAULT 'noname' NOT NULL,
                        globalACS float DEFAULT 0 NOT NULL,
                        globalKD float DEFAULT 0 NOT NULL,
                        globalKPR float DEFAULT 0 NOT NULL,
                        globalAPR float DEFAULT 0 NOT NULL,
                        agent VARCHAR(20) DEFAULT 'noagent' NOT NULL,
                        playerImg VARCHAR(50) DEFAULT 'https://www.vlr.gg/img/base/ph/sil.png' NOT NULL,
                        flag VARCHAR(15) DEFAULT ':pirate_flag:' NOT NULL,
                        personID int PRIMARY KEY AUTO_INCREMENT)""")

        self.mycursor.execute("""CREATE TABLE Users (userID int PRIMARY KEY AUTO_INCREMENT,
                        playerName VARCHAR(40) DEFAULT 'user' NOT NULL,
                        pTeamName VARCHAR(30) DEFAULT 'no name' NOT NULL,
                        points int DEFAULT 0 NOT NULL)""")
                        
        self.mycursor.execute("""CREATE TABLE UserTeam (teamID int PRIMARY KEY, FOREIGN KEY(teamID) REFERENCES Users(userID),
                        playerTeam VARCHAR(40) DEFAULT 'userTeam' NOT NULL,
                        coach VARCHAR(25) DEFAULT 'Missing' NOT NULL,
                        playerOne VARCHAR(20) DEFAULT 'Missing' NOT NULL,
                        playerTwo VARCHAR(20) DEFAULT 'Missing' NOT NULL,
                        playerThree VARCHAR(20) DEFAULT 'Missing' NOT NULL,
                        playerFour VARCHAR(20) DEFAULT 'Missing' NOT NULL,
                        playerFive VARCHAR(20) DEFAULT 'Missing' NOT NULL)
                        """)
        for y, pName in enumerate(self.playerNames):
            Q1 = "INSERT INTO Players (userName) VALUES (%s)"
            self.mycursor.execute(Q1, (pName,))

        self.mycursor.execute("DESCRIBE UserTeam")
        for x in self.mycursor:
            print(x)
        print("\n\n")
    #db.commit()'''
    #Opening playerlist.json to be accessed

    ##PULLING PLAYER NAMES FROM playerlist.json AND SCRAPPING DATA ACCORDING TO NAME
    ##THEN FILLING THE DATA TABLE WITH THE APPROPIATE VALUES

    def updateTable(self):
        for y, pName in enumerate(self.playerNames):

            realname = self.scrape.playerGetName(pName)
            I1 = "UPDATE Players SET realName = %s WHERE userName = %s"
            self.mycursor.execute(I1, (realname, pName,))

            teamName = self.scrape.playerGetTeam(pName)
            I2 = "UPDATE Players SET team = %s WHERE userName = %s"
            self.mycursor.execute(I2, (teamName, pName,))

            country = self.scrape.playerGetRegion(pName)
            I3 = "UPDATE Players SET country = %s WHERE userName = %s"
            self.mycursor.execute(I3, (country, pName,))

            acs = self.scrape.playerGetGlobalACS(pName)
            I4 = "UPDATE Players SET globalACS = %s WHERE userName = %s"
            self.mycursor.execute(I4, (acs, pName,))
            
            kd = self.scrape.playerGetGlobalKD(pName)
            I5 = "UPDATE Players SET globalKD = %s WHERE userName = %s"
            self.mycursor.execute(I5, (kd, pName,))

            kpr = self.scrape.playerGetGlobalKPR(pName)
            I6 = "UPDATE Players SET globalKPR = %s WHERE userName = %s"
            self.mycursor.execute(I6, (kpr, pName,))

            apr = self.scrape.playerGetGlobalAPR(pName)
            I7 = "UPDATE Players SET globalAPR = %s WHERE userName = %s"
            self.mycursor.execute(I7, (apr, pName,))

            agt = self.scrape.playerGetAgent(pName)
            I8 = "UPDATE Players SET agent = %s WHERE userName = %s"
            self.mycursor.execute(I8, (agt, pName,))

            img = self.scrape.playerGetPicture(pName)
            I9 = "UPDATE Players SET playerImg = %s WHERE userName = %s"
            self.mycursor.execute(I9, (img, pName,))

            self.mycursor.execute("SELECT * FROM Players WHERE userName = %s", (pName,))
            for x in self.mycursor:
                print(x)
            self.db.commit()

    def printTable(self):
        self.mycursor.execute("SELECT * FROM Players")
        for x in self.mycursor:
            print(x)

    def playerGetRealName(self, name: str):
        self.mycursor.execute("SELECT realName FROM Players WHERE userName = %s", (name,))
        for x in self.mycursor:
            return x[0]

    def playerGetTeam(self, name: str):
        self.mycursor.execute("SELECT team FROM Players WHERE userName = %s", (name,))
        for x in self.mycursor:
            return x[0]

    def playerGetRegion(self, name: str):
        self.mycursor.execute("SELECT country FROM Players WHERE userName = %s", (name,))
        for x in self.mycursor:
            return x[0]

    def playerGetGlobalACS(self, name: str):
        self.mycursor.execute("SELECT globalACS FROM Players WHERE userName = %s", (name,))
        for x in self.mycursor:
            return x[0]

    def playerGetGlobalKD(self, name: str):
        self.mycursor.execute("SELECT globalKD FROM Players WHERE userName = %s", (name,))
        for x in self.mycursor:
            return x[0]

    def playerGetGlobalKPR(self, name: str):
        self.mycursor.execute("SELECT globalKPR FROM Players WHERE userName = %s", (name,))
        for x in self.mycursor:
            return x[0]

    def playerGetGlobalAPR(self, name: str):
        self.mycursor.execute("SELECT globalAPR FROM Players WHERE userName = %s", (name,))
        for x in self.mycursor:
            return x[0]

    def playerGetAgent(self, name: str):
        self.mycursor.execute("SELECT agent FROM Players WHERE userName = %s", (name,))
        for x in self.mycursor:
            return x[0]

    def playerGetPicture(self, name: str):
        self.mycursor.execute("SELECT playerImg FROM Players WHERE userName = %s", (name,))
        for x in self.mycursor:
            return x[0]

    #updateTable()
    #closing playerlist.json file
    ## DATABASE COMMIT, DO NOT COMMIT UNLESS YOU KNOW WHAT YOU ARE DOING 
    #mycursor.execute("DROP TABLE users")

#TESTING
datab = Database()
datab.createTable()
datab.updateTable()






    #Junk Example Code
'''#mycursor.execute("DESCRIBE Players")
    #mycursor.execute("SELECT userName, realName FROM Players WHERE userName = 'Magni'")
    #mycursor.execute("ALTER TABLE Players ADD COLUMN globalKDR smallint NOT NULL")
    #mycursor.execute("DESCRIBE Players")
    #mycursor.execute("ALTER TABLE Players RENAME TO Players")
    #mycursor.execute("ALTER TABLE Players ADD COLUMN Agent VARCHAR(20) NOT NULL")'''
'''
    playeridJson = open('Scripts/VCTDataScraper/JsonFiles/playerlist.json')
    data = json.load(playeridJson)
    scrape = Scrapper() #Declaring Scrapper object
   #A List being filled with the names found in playerlist.json
    stuff = []
    for i in data.get('players'):
        stuff.append(i)'''