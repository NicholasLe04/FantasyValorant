import random
import requests
from bs4 import BeautifulSoup
import json


class Scrapper():
    
    ## Loads team page ID's to access team page urls
    with open('Scripts/VCTDataScraper/JsonFiles/teamids.json') as ids:
        teamIDs = json.load(ids)

    with open('Scripts/VCTDataScraper/JsonFiles/playerids.json') as ids:
        playerIDs = json.load(ids)

    ## 'Scrapper' object constructor
    def __init__(self):
        self.headers = {
            "User_Agent": ""
        }

    ### MATCH DATA

    ## Gets and returns ARRAY of team names 
    #  example output: ['OpTic Gaming', 'Sentinels']
    #  example usage: 'ScrapperObject'.getTeams(url)[0] = 'OpTic Gaming'
    def getTeams(self, match_id):    
        html = requests.get('https://www.vlr.gg/' + str(match_id))
        soup = BeautifulSoup(html.content, 'lxml')

        # Finds the div's holding team names
        teams = soup.find_all('div', {"class": "wf-title-med"})
        return [teams[0].text.strip(), teams[1].text.strip()]       


    ## Gets and returns ARRAY of score from match 
    #  example output: [2,1]
    #  example usage: ScrapperObject'.getScore(url)[0] = 2
    def getScore(self, match_id):
        html = requests.get('https://www.vlr.gg/' + str(match_id))
        soup = BeautifulSoup(html.content, 'lxml')
        
        return [int(soup.find('span', {'class': 'match-header-vs-score-winner'}).text.strip()), 
                int(soup.find('span', {'class': 'match-header-vs-score-loser'}).text.strip())]


    ## ~~~~
    ### OBSELETE
    ## ~~~~
    ## Gets and returns ARRAY of team 1 players 
    #  example output: ['yay', 'crashies', 'FNS, 'Victor', 'Marved']
    #  example usage: 'ScrapperObject'.getTeam1Players(url)[0] = 'yay'
    # def getTeam1Players(self, url):
    #     html = requests.get(url)
    #     soup = BeautifulSoup(html.content, 'lxml')
    #     stat_tables = soup.find('tbody')
    #     output = []

    #     containers = stat_tables.find_all('tr')
    #     for container in containers:
    #         player = container.find("div", {"class": "text-of"}).text.strip()

    #         output.append(
    #             player
    #         )

    #     return output

    ## ~~~~
    ### OBSELETE
    ## ~~~~
    ## Gets and returns ARRAY of team 1 players 
    #  example output: ['Sacy', 'aspas', 'pancada, 'Less', 'saadhak']
    #  example usage: 'ScrapperObject'.getTeam2Players(url)[0] = 'Sacy'
    # def getTeam2Players(self, url):
    #     html = requests.get(url)
    #     soup = BeautifulSoup(html.content, 'lxml')
    #     stat_tables = soup.find_all('tbody')
    #     output = []

    #     containers = stat_tables[1].find_all('tr')
    #     for container in containers:
    #         player = container.find("div", {"class": "text-of"}).text.strip()

    #         output.append(
    #             player
    #         )

    #     return output
        

    ## Gets and returns DICTIONARY filled with ARRAYS of map scores 
    #  example ouput: {'map-1': [15, 13], 'map-2': [6, 13], 'map-3': [16, 14], 'map-4': [13, 5]}
    #  example usage: 'ScrapperObject'.getMapScores(url).get('map-1') = [15, 13]
    def getMapScores(self, match_id: int):
        html = requests.get('https://www.vlr.gg/' + str(match_id))
        soup = BeautifulSoup(html.content, 'lxml')
        map_scores = soup.find_all('div', {'class': 'score'})

        output = {}
        
        for i in range(0, len(map_scores), 2):
            output['map-' + str(int(i/2) + 1)] = [int(map_scores[i].text.strip()), int(map_scores[i+1].text.strip())]
        
        return output

    ## Gets and returns ARRAY filled with DICTIONARIES for each player's info/stats 
    def getPlayerStats(self, match_id: int):
        html = requests.get('https://www.vlr.gg/' + str(match_id))
        soup = BeautifulSoup(html.content, 'lxml')
        stat_tables = soup.find_all('tbody')    # Finds all table body elements
        player_index = 0

        output = []

        container = soup.find("div", attrs={'class': 'vm-stats-container'})  # Access stat container
        tables = container.find_all("div", {'class': 'vm-stats-game'})       # Access all stat tables
        all_map_stat_table = tables[1]                                       # Access stat table for all maps
        all_map_stats_rows = all_map_stat_table.find_all('tr')               # Access rows in stat table                 

        for tr in all_map_stats_rows:   # For each row in all map stat rows

            acs_kills_rows = tr.find_all('span', {"class": "side mod-side mod-both"})   # Finds 'acs' and 'kills' stats 
            #deaths_assists_rows = tr.find_all('span', {"class": "side mod-both"})       # Finds 'deaths' and 'assists' stats
            team_1 = stat_tables[2].find_all('tr')  # Finds the team 1 player stat elements
            team_2 = stat_tables[3].find_all('tr')  # Finds the team 2 player stat elements

            for i in range(0, len(acs_kills_rows), 2):  # Iterate through all acs and kill elements
                if (player_index < 5):
                    output.append([team_1[player_index].find("div", {"class": "text-of"}).text.strip(), int(acs_kills_rows[0].text.strip())])
                else:
                    output.append([team_2[player_index-5].find("div", {"class": "text-of"}).text.strip(), int(acs_kills_rows[0].text.strip())])
                player_index += 1

        return output


    ## Gets all game stats (Teams, score, players, acs, K/D/A)
    def getMatchStats(self, match_id):
        info={}

        ## Get team names
        info['teams'] = self.getTeams(match_id)

        ## Gets the final score
        info['score'] = self.getScore(match_id)

        ## Gets individual map scores
        info['map-scores'] = self.getMapScores(match_id)

        ## Get ACS, Kills, Deaths, and Assists for each player
        info['player-stats'] = self.getPlayerStats(match_id)
                

        return info

    ## Gets and returns url to the overview page of the most recent match on vlr.gg/matches/results
    def getRecentUrl(self):
        html = requests.get('https://www.vlr.gg/matches/results')
        soup = BeautifulSoup(html.content, 'lxml')

        url = 'https://www.vlr.gg' + soup.find('a', {'class': 'match-item'}).get('href')    # Gets and returns url to the overview page of the most recent match on vlr.gg/matches/results
        return url


    #############################
    #                           #
    #   INDIVIDUAL TEAM DATA    #
    #                           #
    #############################
    
    ##  Returns an ARRAY filled with DICTIONARIES of all the players IGNs and url's to their images
    #   example output: [{'name 1': 'vanity', 'image 1': 'https://owcdn.net/img/6224a530d0113.png'}, 'name 2': 'curry', 'image 2': 'https:/img/base/ph/sil.png'}, etc.]
    #   example usage: 'ScrapperObject'.getPlayers('cloud9') = [{'name 1': 'vanity', 'image 1': 'https://owcdn.net/img/6224a530d0113.png'}, etc.]
    def teamGetPlayers(self, team: str):
        url = 'https://www.vlr.gg/team/' + str(self.teamIDs.get(team.lower()))  # Navigate to the specified team page 
        html = requests.get(url)
        soup = BeautifulSoup(html.content, 'lxml')
        player_table = soup.find_all('div', {'class': 'wf-card'})
        player_names = player_table[1].find_all('div', {'class': 'team-roster-item-name-alias'})    # Find all in-game names

        output = []
        
        # player_names = player_table.find_all('div', {'class': 'team-roster-item-name-alias'})
        player_image_urls = player_table[1].find_all('img')
        

        for i in range(5):  # player_data['name ' + str(i)] = player_images[i].get('src')
            output.append(
                {'name ' + str(i+1): player_names[i].text.strip(),
                'image ' + str(i+1): 'https:' + player_image_urls[i].get('src')}
            )

        return output

    def teamGetName(self, team: str):
        url = 'https://www.vlr.gg/team/' + str(self.teamIDs.get(team.lower()))  # Navigate to the specified team page 
        html = requests.get(url)
        soup = BeautifulSoup(html.content, 'lxml') 
        return soup.find('h1', {'class': 'wf-title'}).text.strip()

    def teamGetLogo(self, team: str):
        url = 'https://www.vlr.gg/team/' + str(self.teamIDs.get(team.lower()))  # Navigate to the specified team page 
        html = requests.get(url)
        soup = BeautifulSoup(html.content, 'lxml') 
        return 'https:' + soup.find('div', {'class': 'wf-avatar team-header-logo'}).find('img').get('src')



    ##############################
    #                            #
    #   INDIVIDUAL PLAYER DATA   #
    #                            #
    ##############################

    def playerGetTeam(self, player_name: str):
        url = 'https://www.vlr.gg/player/' + str(self.playerIDs.get(player_name.lower()))  # Navigate to the specified team page 
        html = requests.get(url)
        soup = BeautifulSoup(html.content, 'lxml') 
        return soup.find_all('div', {'class': 'wf-card'})[2].find('div', {'style': 'font-weight: 500;'}).text.strip()

    def playerGetName(self, player_name: str):
        url = 'https://www.vlr.gg/player/' + str(self.playerIDs.get(player_name.lower()))  # Navigate to the specified team page 
        html = requests.get(url)
        soup = BeautifulSoup(html.content, 'lxml') 
        return soup.find('h2', {'class': 'player-real-name'}).text.strip()

    def playerGetUsername(self, player_name: str):
        url = 'https://www.vlr.gg/player/' + str(self.playerIDs.get(player_name.lower()))  # Navigate to the specified team page 
        html = requests.get(url)
        soup = BeautifulSoup(html.content, 'lxml') 
        return soup.find('h1', {'class': 'wf-title'}).text.strip()

    def playerGetPicture(self, player_name:str):
        url = 'https://www.vlr.gg/player/' + str(self.playerIDs.get(player_name.lower()))  # Navigate to the specified team page 
        html = requests.get(url)
        soup = BeautifulSoup(html.content, 'lxml') 
        return 'https:' + soup.find('div', {'class': 'wf-avatar'}).find('img').get('src')
    
    def playerGetRegion(self, player_name: str):
        url = 'https://www.vlr.gg/player/' + str(self.playerIDs.get(player_name.lower()))  # Navigate to the specified team page 
        html = requests.get(url)
        soup = BeautifulSoup(html.content, 'lxml') 
        return soup.find('div', {'class': 'ge-text-light'}).text.strip()

    def playerGetGlobalACS(self, player_name: str):
        url = 'https://www.vlr.gg/player/' + str(self.playerIDs.get(player_name.lower())) + '/?timespan=90d'  # Navigate to the specified team page 
        html = requests.get(url)
        soup = BeautifulSoup(html.content, 'lxml') 
        return float(soup.find('tbody').find('tr').find_all('td')[4].text.strip())

    def playerGetGlobalKD(self, player_name: str):
        url = 'https://www.vlr.gg/player/' + str(self.playerIDs.get(player_name.lower())) + '/?timespan=90d'  # Navigate to the specified team page 
        html = requests.get(url)
        soup = BeautifulSoup(html.content, 'lxml') 
        return float(soup.find('tbody').find('tr').find_all('td')[5].text.strip())
    
    def playerGetGlobalKPR(self, player_name: str):
        url = 'https://www.vlr.gg/player/' + str(self.playerIDs.get(player_name.lower())) + '/?timespan=90d'  # Navigate to the specified team page 
        html = requests.get(url)
        soup = BeautifulSoup(html.content, 'lxml') 
        return float(soup.find('tbody').find('tr').find_all('td')[8].text.strip())

    def playerGetGlobalAPR(self, player_name: str):
        url = 'https://www.vlr.gg/player/' + str(self.playerIDs.get(player_name.lower())) + '/?timespan=90d'  # Navigate to the specified team page 
        html = requests.get(url)
        soup = BeautifulSoup(html.content, 'lxml') 
        return float(soup.find('tbody').find('tr').find_all('td')[9].text.strip())

    def playerGetAgent(self, player_name: str):
        url = 'https://www.vlr.gg/player/' + str(self.playerIDs.get(player_name.lower())) + '/?timespan=90d'  # Navigate to the specified team page 
        html = requests.get(url)
        soup = BeautifulSoup(html.content, 'lxml') 
        agent_url = soup.find('tbody').find('tr').find('td').find('img').get('src')
        return agent_url[21:len(agent_url)-4]

    

# # TESTING 
# scrapper = Scrapper()
# url = scrapper.getRecentUrl()

## HOW TO OPEN AN IMAGE FROM URL
# urllib.request.urlretrieve(
#  'https://owcdn.net/img/6207470ac0601.png',
#   "fns.png")
  
# img = Image.open("fns.png") 
# img.show()



