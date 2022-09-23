from fileinput import close
from multiprocessing import connection
import mysql.connector
from mysql.connector import Error
from VCTDataScraper.scrape import Scrapper
import pandas as pd
import json

##CONNECTING TO LOCALLY HOSTED SQL SERVER
##AVOID RUNNING CODE UNTIL SQL SERVER SORTED OUT
db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="SavestaAQT100%",
    database="testdatabase"
)
mycursor = db.cursor()

## CREATING A DATA TABLE NAMED PLAYERS
# Commented out as datatable has already been created locally on Joshua's Laptop
'''mycursor.execute("CREATE TABLE Players (userName VARCHAR(15) DEFAULT 'noname' NOT NULL , realName VARCHAR(30) DEFAULT 'noname' NOT NULL, team VARCHAR(20) DEFAULT 'noname' NOT NULL, country VARCHAR(25) DEFAULT 'noname' NOT NULL, globalACS float DEFAULT 0 NOT NULL, globalKD float DEFAULT 0 NOT NULL, globalKPR float DEFAULT 0 NOT NULL, globalAPR float DEFAULT 0 NOT NULL, agent VARCHAR(20) DEFAULT 'noagent' NOT NULL, playerImg VARCHAR(50) DEFAULT 'https://www.vlr.gg/img/base/ph/sil.png' NOT NULL,   personID int PRIMARY KEY AUTO_INCREMENT)")

mycursor.execute("DESCRIBE PLAYERS")
for x in mycursor:
    print(x)
db.commit()'''

#Junk Example Code
'''#mycursor.execute("DESCRIBE Players")

#mycursor.execute("SELECT userName, realName FROM Players WHERE userName = 'Magni'")

#mycursor.execute("ALTER TABLE Players ADD COLUMN globalKDR smallint NOT NULL")

#mycursor.execute("DESCRIBE Players")

#mycursor.execute("ALTER TABLE Players RENAME TO Players")
#mycursor.execute("ALTER TABLE Players ADD COLUMN Agent VARCHAR(20) NOT NULL")'''

#Opening playerlist.json to be accessed
playeridJson = open('Scripts/VCTDataScraper/JsonFiles/playerlist.json')
data = json.load(playeridJson)
scrape = Scrapper() #Declaring Scrapper object

#A List being filled with the names found in playerlist.json
stuff = []
for i in data.get('players'):
    stuff.append(i)

##PULLING PLAYER NAMES FROM playerlist.json AND SCRAPPING DATA ACCORDING TO NAME
##THEN FILLING THE DATA TABLE WITH THE APPROPIATE VALUES
for y, pName in enumerate(stuff):
    agt = scrape.playerGetAgent(pName)
    I1 = "UPDATE Players SET agent = %s WHERE userName = %s"
    mycursor.execute(I1, (agt, pName,))

    img = scrape.playerGetPicture(pName)
    I2 = "UPDATE Players SET playerImg = %s WHERE userName = %s"
    mycursor.execute(I2, (img, pName,))

    

    #PRINTING TEST
    mycursor.execute("SELECT * FROM Players WHERE userName = %s", (pName,))
    for x in mycursor:
        print(x)


close() #closing playerlist.json file

## DATABASE COMMIT, DO NOT COMMIT UNLESS YOU KNOW WHAT YOU ARE DOING 
#db.commit()