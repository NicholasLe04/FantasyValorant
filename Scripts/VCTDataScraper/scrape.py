import os
import requests
from bs4 import BeautifulSoup
import json


class Scraper():
    
    file_dir = os.path.dirname(__file__)
    teamid_file_name = os.path.join(file_dir, 'JsonFiles/teamids.json')
    playerid_file_name = os.path.join(file_dir, 'JsonFiles/playerids.json')
    flags_file_name = os.path.join(file_dir, 'JsonFiles/flags.json')
    teamlogos_file_name = os.path.join(file_dir, 'JsonFiles/teamlogos.json')

    ## Loads team page ID's to access team page urls
    with open(teamid_file_name) as teamids:
        teamIDs = json.load(teamids)

    with open(playerid_file_name) as playerids:
        playerIDs = json.load(playerids)

    with open(flags_file_name) as flags:
        flagEmojis = json.load(flags)

    with open(teamlogos_file_name) as teamlogos:
        teamLogos = json.load(teamlogos)

    ## 'Scrapper' object constructor
    def __init__(self):
        self.headers = {
            "User_Agent": ""
        }

    ## Gets and returns url to the overview page of the most recent match on vlr.gg/matches/results
    def getRecentUrl(self):
        html = requests.get('https://www.vlr.gg/matches/results')
        soup = BeautifulSoup(html.content, 'lxml')

        url = 'https://www.vlr.gg' + soup.find('a', {'class': 'match-item'}).get('href')    # Gets and returns url to the overview page of the most recent match on vlr.gg/matches/results
        return url

    #############################
    #                           #
    #         MATCH DATA        #
    #                           #
    #############################

    ## Gets and returns ARRAY of team names 
    #  example output: ['OpTic Gaming', 'Sentinels']
    #  example usage: 'ScrapperObject'.scrapeMatchTeams(url)[0] = 'OpTic Gaming'
    def scrapeMatchTeams(self, match_id):    
        html = requests.get('https://www.vlr.gg/' + str(match_id))
        soup = BeautifulSoup(html.content, 'lxml')

        # Finds the div's holding team names
        teams = soup.find_all('div', {"class": "wf-title-med"})
        return [teams[0].text.strip(), teams[1].text.strip()]       


    ## Gets and returns ARRAY of score from match 
    #  example output: [2,1]
    #  example usage: ScrapperObject'.scrapeMatchScore(url)[0] = 2
    def scrapeMatchScore(self, match_id):
        html = requests.get('https://www.vlr.gg/' + str(match_id))
        soup = BeautifulSoup(html.content, 'lxml')
        
        return [int(soup.find('span', {'class': 'match-header-vs-score-winner'}).text.strip()), 
                int(soup.find('span', {'class': 'match-header-vs-score-loser'}).text.strip())]  

    ## Gets and returns DICTIONARY filled with ARRAYS of map scores 
    #  example ouput: {'map-1': [15, 13], 'map-2': [6, 13], 'map-3': [16, 14], 'map-4': [13, 5]}
    #  example usage: 'ScrapperObject'.scrapeMapScores(url).get('map-1') = [15, 13]
    def scrapeMapScores(self, match_id: int):
        html = requests.get('https://www.vlr.gg/' + str(match_id))
        soup = BeautifulSoup(html.content, 'lxml')
        map_scores = soup.find_all('div', {'class': 'score'})

        output = {}
        
        for i in range(0, len(map_scores), 2):
            output['map-' + str(int(i/2) + 1)] = [int(map_scores[i].text.strip()), int(map_scores[i+1].text.strip())]
        
        return output

    ## Gets and returns ARRAY filled with DICTIONARIES for each player's info/stats 
    def scrapeMatchPlayerStats(self, match_id: int):
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
    def scrapeMatchInfo(self, match_id):
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


    #############################
    #                           #
    #   INDIVIDUAL TEAM DATA    #
    #                           #
    #############################
    
    ##  Returns an ARRAY filled with DICTIONARIES of all the players IGNs and url's to their images
    #   example output: [{'name 1': 'vanity', 'image 1': 'https://owcdn.net/img/6224a530d0113.png'}, 'name 2': 'curry', 'image 2': 'https:/img/base/ph/sil.png'}, etc.]
    def scrapeTeamPlayers(self, team: str):
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

    ## Returns team name with correct capitalization
    def scrapeTeamName(self, team: str):
        url = 'https://www.vlr.gg/team/' + str(self.teamIDs.get(team.lower()))  # Navigate to the specified team page 
        html = requests.get(url)
        soup = BeautifulSoup(html.content, 'lxml') 
        return soup.find('h1', {'class': 'wf-title'}).text.strip()

    ## Returns the url for the logo of the inputted team
    def scrapeTeamLogo(self, team: str):
        return self.teamLogos.get(team.lower())

    ## Returns team region
    def scrapeTeamRegion(self, team: str):
        url = 'https://www.vlr.gg/team/' + str(self.teamIDs.get(team.lower()))  # Navigate to the specified team page 
        html = requests.get(url)
        soup = BeautifulSoup(html.content, 'lxml') 
        return soup.find('div', {'class': 'team-header-country'}).text.strip()

    ## Returns player_name's country/region flag emoji
    #  Example: scrapper.scrapePlayerRegionFlag('tenz') = ':flag_ca:'
    def scrapeTeamRegionFlag(self, team: str):
        return self.flagEmojis.get(self.scrapeTeamRegion(team).upper())

        output = []

        table = soup.find('tbody')
        for tr in table.find_all('tr', {'class': ''}):

            output.append([tr.find_all('td')[0].text.strip(), tr.find_all('td')[2].text.strip()])

        return output

    ##############################
    #                            #
    #   INDIVIDUAL PLAYER DATA   #
    #                            #
    ##############################

    ## Returns player_name's team
    #  Example: scrapper.scrapePlayerTeam('tenz') = 'Sentinels'
    def scrapePlayerTeam(self, player_name: str):
        url = 'https://www.vlr.gg/player/' + str(self.playerIDs.get(player_name.lower()))  # Navigate to the specified team page 
        html = requests.get(url)
        soup = BeautifulSoup(html.content, 'lxml') 
        try:
            #return soup.find_all('div', {'class': 'wf-card'})[2].find('div', {'style': 'font-weight: 500;'}).text.strip()
            return soup.find('div', {'style': 'font-weight: 500;'}).text.strip()
        except:
            return 'no team' 

    ## Returns 'player_name''s real name 
    #  Example: scrapper.scrapePlayerName('tenz') = 'Tyson Ngo'
    def scrapePlayerName(self, player_name: str):
        url = 'https://www.vlr.gg/player/' + str(self.playerIDs.get(player_name.lower()))  # Navigate to the specified team page 
        html = requests.get(url)
        soup = BeautifulSoup(html.content, 'lxml') 
        return soup.find('h2', {'class': 'player-real-name'}).text.strip()

    ## Returns player_name's username witch correct capitalization
    #  Example: scrapper.scrapePlayerTeam('tenz') = 'TenZ'
    def scrapePlayerUsername(self, player_name: str):
        url = 'https://www.vlr.gg/player/' + str(self.playerIDs.get(player_name.lower()))  # Navigate to the specified team page 
        html = requests.get(url)
        soup = BeautifulSoup(html.content, 'lxml') 
        return soup.find('h1', {'class': 'wf-title'}).text.strip()

    ## Returns player_name's picture or default image url
    #  Example: scrapper.scrapePlayerPicture('tenz') = 'https://www.vlr.gg/img/base/ph/sil.png'
    def scrapePlayerPicture(self, player_name:str):
        url = 'https://www.vlr.gg/player/' + str(self.playerIDs.get(player_name.lower()))  # Navigate to the specified team page 
        html = requests.get(url)
        soup = BeautifulSoup(html.content, 'lxml') 
        image = 'https:' + soup.find('div', {'class': 'wf-avatar'}).find('img').get('src')
        if image == "https:/img/base/ph/sil.png":
            return  "https://www.vlr.gg/img/base/ph/sil.png"
        else:
            return image

    ## Returns player_name's country/region
    #  Example: scrapper.scrapePlayerRegion('tenz') = 'CANADA'
    def scrapePlayerRegion(self, player_name: str):
        url = 'https://www.vlr.gg/player/' + str(self.playerIDs.get(player_name.lower()))  # Navigate to the specified team page 
        html = requests.get(url)
        soup = BeautifulSoup(html.content, 'lxml') 
        return soup.find('div', {'class': 'ge-text-light'}).text.strip()

    ## Returns player_name's country/region flag emoji
    #  Example: scrapper.scrapePlayerRegionFlag('tenz') = ':flag_ca:'
    def scrapePlayerRegionFlag(self, player_name: str):
        url = 'https://www.vlr.gg/player/' + str(self.playerIDs.get(player_name.lower()))  # Navigate to the specified team page 
        html = requests.get(url)
        soup = BeautifulSoup(html.content, 'lxml') 
        region = soup.find('div', {'class': 'ge-text-light'}).text.strip()
        return self.flagEmojis.get(region)
        
    ## Returns player_name's average ACS over the past 90 days
    #  Example: scrapper.scrapePlayerGlobalACS('tenz') = '229.6'
    def scrapePlayerGlobalACS(self, player_name: str):
        url = 'https://www.vlr.gg/player/' + str(self.playerIDs.get(player_name.lower())) + '/?timespan=90d'  # Navigate to the specified team page 
        html = requests.get(url)
        soup = BeautifulSoup(html.content, 'lxml') 
        try:
            return float(soup.find('tbody').find('tr').find_all('td')[4].text.strip())
        except: 
            return 0.0

    ## Returns player_name's average K/D over the past 90 days
    #  Example: scrapper.scrapePlayerGlobalKD('tenz') = '1.2'
    def scrapePlayerGlobalKD(self, player_name: str):
        url = 'https://www.vlr.gg/player/' + str(self.playerIDs.get(player_name.lower())) + '/?timespan=90d'  # Navigate to the specified team page 
        html = requests.get(url)
        soup = BeautifulSoup(html.content, 'lxml') 
        try:
            return float(soup.find('tbody').find('tr').find_all('td')[5].text.strip())
        except:
            return 0.0
    
    ## Returns player_name's average kills per round over the past 90 days
    #  Example: scrapper.scrapePlayerGlobalKPR('tenz') = '0.84'
    def scrapePlayerGlobalKPR(self, player_name: str):
        url = 'https://www.vlr.gg/player/' + str(self.playerIDs.get(player_name.lower())) + '/?timespan=90d'  # Navigate to the specified team page 
        html = requests.get(url)
        soup = BeautifulSoup(html.content, 'lxml') 
        try:
            return float(soup.find('tbody').find('tr').find_all('td')[8].text.strip())
        except:
            return 0.0

    ## Returns player_name's average assists per round over the past 90 days
    #  Example: scrapper.scrapePlayerGlobalAPR('tenz') = '0.11'
    def scrapePlayerGlobalAPR(self, player_name: str):
        url = 'https://www.vlr.gg/player/' + str(self.playerIDs.get(player_name.lower())) + '/?timespan=90d'  # Navigate to the specified team page 
        html = requests.get(url)
        soup = BeautifulSoup(html.content, 'lxml') 
        try:
            return float(soup.find('tbody').find('tr').find_all('td')[9].text.strip())
        except:
            return 0.0

    ## Returns player_name's most played agent over the past 90 days
    #  Example: scrapper.scrapePlayerAgent('tenz') = 'Chamber'
    def scrapePlayerAgent(self, player_name: str):
        url = 'https://www.vlr.gg/player/' + str(self.playerIDs.get(player_name.lower())) + '/?timespan=90d'  # Navigate to the specified team page 
        html = requests.get(url)
        soup = BeautifulSoup(html.content, 'lxml') 
        try:
            agent_url = soup.find('tbody').find('tr').find('td').find('img').get('src')
            return agent_url[21:len(agent_url)-4]
        except:
            return 'no agent'

    
    #############################
    #                           #
    #   INDIVIDUAL COACH DATA   #
    #                           #
    #############################


scraper = Scraper()
print(scraper.scrapeTeamRegion("sentinels"))


## TESTING 


