import requests
from bs4 import BeautifulSoup

class Scrapper():
    
    ## 'Scrapper' object constructor
    def __init__(self):
        self.headers = {
            "User_Agent": ""
        }


    ## Gets and returns ARRAY of team names (ex: ['OpTic Gaming', 'Sentinels'])
    #  'ScrapperObject'.getTeams(url)[0] = 'Optic Gaming'
    def getTeams(self, url):    
        html = requests.get(url)
        soup = BeautifulSoup(html.content, 'lxml')

        teams = soup.find_all('div', {"class": "wf-title-med"})
        return [teams[0].text.strip(), teams[1].text.strip()]       


    ## Gets and returns ARRAY of score from match (ex: [2,1])
    #  'ScrapperObject'.getScore(url)[0] = 2
    def getScore(self, url):
        html = requests.get(url)
        soup = BeautifulSoup(html.content, 'lxml')

        
        return [int(soup.find('span', {'class': 'match-header-vs-score-winner'}).text.strip()), int(soup.find('span', {'class': 'match-header-vs-score-loser'}).text.strip())]


    ## Gets and returns ARRAY of team 1 players (ex: ['yay', 'crashies', 'FNS, 'Victor', 'Marved'])
    #  'ScrapperObject'.getTeam1Players(url)[0] = 'yay'
    def getTeam1Players(self, url):
        html = requests.get(url)
        soup = BeautifulSoup(html.content, 'lxml')
        stat_tables = soup.find('tbody')
        output = []

        containers = stat_tables.find_all('tr')
        for container in containers:
            player = container.find("div", {"class": "text-of"}).text.strip()

            output.append(
                player
            )

        return output


    ## Gets and returns ARRAY of team 1 players (ex: ['Sacy', 'aspas', 'pancada, 'Less', 'saadhak'])
    #  'ScrapperObject'.getTeam2Players(url)[0] = 'Sacy'
    def getTeam2Players(self, url):
        html = requests.get(url)
        soup = BeautifulSoup(html.content, 'lxml')
        stat_tables = soup.find_all('tbody')
        output = []

        containers = stat_tables[1].find_all('tr')
        for container in containers:
            player = container.find("div", {"class": "text-of"}).text.strip()

            output.append(
                player
            )

        return output
        

    ## Gets and returns DICTIONARY filled with ARRAYS of map scores (ex: {'map-1': [15, 13], 'map-2': [6, 13], 'map-3': [16, 14], 'map-4': [13, 5]})
    #  'ScrapperObject'.getMapScores(url).get('map-1') = [15, 13]
    def getMapScores(self, url):
        html = requests.get(url)
        soup = BeautifulSoup(html.content, 'lxml')
        map_scores = soup.find_all('div', {'class': 'score'})

        output = {}
        
        for i in range(0, len(map_scores), 2):
            output['map-' + str(int(i/2) + 1)] = [int(map_scores[i].text.strip()), int(map_scores[i+1].text.strip())]
        
        return output

    def getPlayerStats(self, url):
        html = requests.get(url)
        soup = BeautifulSoup(html.content, 'lxml')
        stat_tables = soup.find_all('tbody')
        player_index = 0

        output = []

        container = soup.find("div", attrs={'class': 'vm-stats-container'})  ## Access stat container
        tables = container.find_all("div", {'class': 'vm-stats-game'})       ## Access all stat tables
        all_map_stat_table = tables[1]                                       ## Access stat table for all maps
        all_map_stats_rows = all_map_stat_table.find_all('tr')               ## Access rows in stat table                 

        for tr in all_map_stats_rows:

            acs_kills_rows = tr.find_all('span', {"class": "side mod-side mod-both"})   ## Finds 'acs' and 'kills' stats 
            deaths_assists_rows = tr.find_all('span', {"class": "side mod-both"})       ## Finds 'deaths' and 'assists' stats
            team_1 = stat_tables[0].find_all('tr')
            team_2 = stat_tables[1].find_all('tr')

            player_stats = {}

            for i in range(0, len(acs_kills_rows), 2):
                if(player_index < 5):
                    player_stats['name'] = team_1[player_index].find("div", {"class": "text-of"}).text.strip()
                else:
                    player_stats['name'] = team_2[player_index - 5].find("div", {"class": "text-of"}).text.strip()

                player_stats['acs'] = int(acs_kills_rows[0].text.strip())
                player_stats['kills'] = int(acs_kills_rows[1].text.strip())
                player_stats['deaths'] = int(deaths_assists_rows[0].text.strip())
                player_stats['assists'] = int(deaths_assists_rows[1].text.strip())
                player_index += 1

                output.append(player_stats)

        return output


    ### Gets all game stats (Teams, score, players, acs, K/D/A)
    def getStats(self, url):
        html = requests.get(url)
        soup = BeautifulSoup(html.content, 'lxml')

        info={}

        ## Get team name
        info['teams'] = self.getTeams(url)

        ## Gets the score
        info['score'] = self.getScore(url)

        ## Gets individual map scores
        info['map-scores'] = self.getMapScores(url)

        ## Get ACS, Kills, Deaths, and Assists for each player from Team 1 
        info['player-stats'] = self.getPlayerStats(url)
                

        return info


    def getRecentUrl(self):
        html = requests.get('https://www.vlr.gg/matches/results')
        soup = BeautifulSoup(html.content, 'lxml')

        url = 'https://www.vlr.gg' + soup.find('a', {'class': 'match-item'}).get('href')    # Gets and returns url to the overview page of the most recent match on vlr.gg/matches/results
        return url


# TESTING 
scrapper = Scrapper()
url = scrapper.getRecentUrl()
print(scrapper.getStats(url))

