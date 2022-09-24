class User:

    roster = []

    # user constructor
    def __init__ (self):
        pass

    # adds a player to the user's roster
    def addPlayer (self, playerID):
        if len(self.roster) < 5:
            self.roster.append (playerID)
        else:
            pass # tell the user the command failed

    # gets a playerID from the user's roster
    def getPlayerID (self, index):
        return self.roster[index]
    
    # removes a playerID from the user's roster
    def removePlayer (self, index):
        if index >= 0 and index < len(self.roster):
            self.roster.pop (index)
        else:
            pass # tell the user the command failed

    # returns the roster array
    def returnRoster(self):
        return (self.roster)

    # clears the roster array
    def clearRoster(self):
        self.roster = []
        

# testing
user = User()
user.addPlayer(3232)
user.addPlayer(323)
user.addPlayer(32)
user.addPlayer(32)
user.addPlayer(32)
user.addPlayer(32)
user.addPlayer(32)

print(user.returnRoster())
user.removePlayer(2)
print(user.returnRoster())
user.clearRoster()
print(user.returnRoster())