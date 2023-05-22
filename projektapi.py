import requests
import json
import matplotlib.pyplot as plt
import numpy as np

# klass för spelare som kan initiaras med divierse stats från matchen
class player:
    def __init__(self, slot, gpm, xpm, kills, deaths, assists):
        self.slot = slot
        self.gpm = gpm
        self.xpm = xpm
        self.kills = kills
        self.deaths = deaths
        self.assists = assists
    def __repr__(self):
        return repr(f'Player <slot> {self.slot}, <gpm> {self.gpm}, <xpm> {self.xpm}, <kills> {self.kills}, <deaths> {self.deaths}, <assists>, {self.assists}')
# Method for getting information from match and writing it on JSON file
def fetchMatch(IDstring):
    response = requests.get (f'https://api.opendota.com/api/matches/{IDstring}') 
    mydict = json.loads(response.text)

    with open('match1.json', 'w') as datafh:
        json.dump(mydict, datafh, indent = 4) 

# list wich will contain the players
playerslist = []
#Method for printing a basic scoreboard
def printScoreboard():
    index = 1
    for player in playerslist:
        print(f'Player{index}: GPM: {player.gpm}, XPM: {player.xpm}: KDA: {player.kills}/{player.deaths}/{player.assists} ')
        index +=1
# Method for initiating players from the match.json file
def initplayers():
    with open ('match1.json') as datafh:
         data = json.load(datafh)
    players = data['players']
    for key in players:
        p = player(key['player_slot'], key['gold_per_min'], key['xp_per_min'], key['kills'], key['deaths'], key['assists']) #initierar 
        playerslist.append(p)

def allPlayerGPMScatter():
    # genereellt smålabbande kring matplotlib och hur spelares statistik kan användas för att visas upp i det 
    x = np.array([1,2,3,4,5,6,7,8,9,10])
    y = np.array([playerslist[0].gpm,playerslist[1].gpm,playerslist[2].gpm,playerslist[3].gpm,playerslist[4].gpm,playerslist[5].gpm,playerslist[6].gpm,playerslist[7].gpm,playerslist[8].gpm,playerslist[9].gpm])
    colors = np.array(["red","green","blue","yellow","pink","black","orange","purple","brown","cyan"])            
    plt.scatter(x,y, c=colors)
    plt.show()

#Welcome text that will be appended througout the project depending how the functionality is implemented        
def printWelcome():
    welcomestring = f'Välkommen till detta DOTA2 matchanalysverktyg börja med att ange ett matchid för att se statitik för matchen.\n ange sedan vilken statistik du vill se en analys för, skriv hjälp för hjälp'
    print(welcomestring)

printWelcome
command = input('Ange matchid: ')
fetchMatch(command)
initplayers()
printScoreboard()
command = input('Ange statistik du vill se en scatterplot för: ')
if command == 'gpm':
    allPlayerGPMScatter()








