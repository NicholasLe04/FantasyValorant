import mysql.connector
from VCTDataScraper.scrape import Scraper
import json
import os
import logging

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

        self.mycursor = self.db.cursor()
        self.logging = logging.basicConfig(filename = 'logging.log', format = '`%(asctime)s %(message)s' , level = logging.INFO)

        file_dir = os.path.dirname(__file__)
        playerlist_dir = os.path.join(file_dir, 'VCTDataScraper/JsonFiles/playerlist.json')
        teamIDs_dir = os.path.join(file_dir, 'VCTDataScraper/JsonFiles/teamids.json')
        with open(playerlist_dir) as playerList:
            players = json.load(playerList)
        with open(teamIDs_dir) as teamIds:
            self.teamIDs = json.load(teamIds) 

        self.playerNames = [] 
        self.coachesNames = []

        for i in players.get('players'):
            self.playerNames.append(i)
        for i in players.get('coaches'):
            self.coachesNames.append(i)
        
        self.scraper = Scraper() #Declaring Scrapper object

    

    def APOCALYPSE(self):
        self.mycursor.execute("DROP TABLE Players")

    ## CREATING A DATA TABLE NAMED PLAYERS
    # Commented out as datatable has already been created locally on Joshua's Laptop
    def createTable(self):
        self.mycursor.execute("""CREATE TABLE IF NOT EXISTS Players (userName VARCHAR(25) DEFAULT 'noname' NOT NULL,
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
        self.mycursor.execute("""CREATE TABLE IF NOT EXISTS Coaches (userName VARCHAR(30) DEFAULT 'noname' NOT NULL,
                        realName VARCHAR(30) DEFAULT 'noname' NOT NULL,
                        team VARCHAR(20) DEFAULT 'noname' NOT NULL,
                        country VARCHAR(25) DEFAULT 'noname' NOT NULL)
                        """)
        self.db.commit()

    def fillNames (self):
        for pName in self.playerNames:
            Q1 = "INSERT INTO Players (userName) VALUES (%s)"
            self.mycursor.execute(Q1, (pName,))
            self.db.commit()

    #db.commit()'''
    #Opening playerlist.json to be accessed

    ##PULLING PLAYER NAMES FROM playerlist.json AND SCRAPPING DATA ACCORDING TO NAME
    ##THEN FILLING THE DATA TABLE WITH THE APPROPIATE VALUES

    def updateTable(self):
        for pName in self.playerNames:

            realname = self.scraper.scrapePlayerName(pName)
            I1 = "UPDATE Players SET realName = %s WHERE userName = %s"
            self.mycursor.execute(I1, (realname, pName,))

            teamName = self.scraper.scrapePlayerTeam(pName)
            I2 = "UPDATE Players SET team = %s WHERE userName = %s"
            self.mycursor.execute(I2, (teamName, pName,))

            country = self.scraper.scrapePlayerRegion(pName)
            I3 = "UPDATE Players SET country = %s WHERE userName = %s"
            self.mycursor.execute(I3, (country, pName,))

            acs = self.scraper.scrapePlayerGlobalACS(pName)
            I4 = "UPDATE Players SET globalACS = %s WHERE userName = %s"
            self.mycursor.execute(I4, (acs, pName,))
            
            kd = self.scraper.scrapePlayerGlobalKD(pName)
            I5 = "UPDATE Players SET globalKD = %s WHERE userName = %s"
            self.mycursor.execute(I5, (kd, pName,))

            kpr = self.scraper.scrapePlayerGlobalKPR(pName)
            I6 = "UPDATE Players SET globalKPR = %s WHERE userName = %s"
            self.mycursor.execute(I6, (kpr, pName,))

            apr = self.scraper.scrapePlayerGlobalAPR(pName)
            I7 = "UPDATE Players SET globalAPR = %s WHERE userName = %s"
            self.mycursor.execute(I7, (apr, pName,))

            agt = self.scraper.scrapePlayerAgent(pName)
            I8 = "UPDATE Players SET agent = %s WHERE userName = %s"
            self.mycursor.execute(I8, (agt, pName,))

            img = self.scraper.scrapePlayerPicture(pName)
            I9 = "UPDATE Players SET playerImg = %s WHERE userName = %s"
            self.mycursor.execute(I9, (img, pName,))

            flg = self.scraper.flagEmojis.get(self.scraper.scrapePlayerRegion(pName).upper())
            I10 = "UPDATE Players SET flag = %s WHERE userName = %s"
            if (flg == None):
                self.mycursor.execute(I10, (":pirate_flag:", pName))
            else:
                self.mycursor.execute(I10, (flg, pName))


            self.db.commit()

    def printTable(self):
        self.mycursor.execute("SELECT * FROM Players")
        for x in self.mycursor:
            print(x)

    def playerGetRealName(self, name: str):
        self.mycursor.execute("SELECT realName FROM Players WHERE userName = %s", (name,))
        for x in self.mycursor:
            return x[0]

    def playerGetUserName(self, name: str):
        self.mycursor.execute("SELECT userName FROM Players WHERE userName = %s", (name,))
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

    def teamGetPlayers(self, team_name: str):
        self.mycursor.execute("SELECT username FROM Players WHERE team = %s", (team_name,))
        team = self.mycursor.fetchall()
        output = []
        for player in team:
            output.append(player[0])
        return output



    #updateTable()
    #closing playerlist.json file
    ## DATABASE COMMIT, DO NOT COMMIT UNLESS YOU KNOW WHAT YOU ARE DOING 
    #mycursor.execute("DROP TABLE users")

#TESTING
datab = Database()
#datab.addNewUser("283407511133093889")
#datab.mycursor.execute("ALTER TABLE Users ADD COLUMN discordID varChar(20)")
#datab.addNewUser(34351351)

### THESE ARE COMMENTED OUT BECAUSE SQL DATABASE ALREADY EXISTS ON AWS SERVERS!!! ONLY USE IF NECESSARY!!!!
# datab.APOCALYPSE()
'''print(datab.getPlayersFromTeam("100 Thieves"))'''






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