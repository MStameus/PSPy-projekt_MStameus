import requests
import json
import matplotlib.pyplot as plt
import numpy as np

# klass för spelare som kan initiaras med divierse stats från matchen
class player:
    def __init__(self, slot, gpm, xpm, kills, deaths, assists, networth, name):
        self.slot = slot
        self.gpm = gpm
        self.xpm = xpm
        self.kills = kills
        self.deaths = deaths
        self.assists = assists
        self.networth = networth
        self.name = name
    def __repr__(self):
        return repr(f'Player <slot> {self.slot}, <gpm> {self.gpm}, <xpm> {self.xpm}, <kills> {self.kills}, <deaths> {self.deaths}, <assists>, {self.assists}')
    def setname(self, newname):
        self.name = newname
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
        print(f'Player{index}: {player.name} GPM: {player.gpm}, XPM: {player.xpm}: KDA: {player.kills}/{player.deaths}/{player.assists} ')
        index +=1

# Method for initiating players from the match1.json file
def initplayers():
    with open ('match1.json') as datafh:
         data = json.load(datafh)
    players = data['players']
    for key in players:
        p = player(key['player_slot'], key['gold_per_min'], key['xp_per_min'], key['kills'], key['deaths'], key['assists'], key['net_worth'], key['hero_id']) #initierar 
        playerslist.append(p)

#method using static json file to set hero names for the players
def setheronames():
    with open ('heroes.json') as heroesfh:
        heroes = json.load(heroesfh)
    for player in playerslist:
        hero = heroes[str(player.name)]
        player.setname(hero['localized_name'])
    

def allPlayerGPMScatter(): 
    gpmlist = []
    amountplayers = []
    for i in range(len(playerslist)):
        amountplayers.append(i+1)
    for item in playerslist:
        gpmlist.append(item.gpm)
    x = np.array(amountplayers)
    y = np.array(gpmlist)
    colors = np.array(["red","green","blue","yellow","pink","black","orange","purple","brown","cyan"])            
    plt.scatter(x,y, c=colors)
    for x,y in zip(x,y):
        label = f'Player{format(x)} gpm: {format(y)}'
        plt.annotate(label,(x,y))
    plt.show()

def notAllplayerGPMScatter(list):
    gpmlist = []
    amountplayers = []
    for item in list:
        gpmlist.append(playerslist[int(item)-1].gpm)
        amountplayers.append(int(item))
    x = np.array(amountplayers)
    y = np.array(gpmlist)
    plt.scatter(x,y)
    for x,y in zip(x,y):
        label = f'Player{format(x)} gpm: {format(y)}'
        plt.annotate(label,(x,y))
    plt.show()

#
def allPlayerXPMScatter():  
    xpmlist = []
    amountplayers = []
    for i in range(len(playerslist)):
        amountplayers.append(i+1)
    for item in playerslist:
        xpmlist.append(item.xpm)
    x = np.array(amountplayers)
    y = np.array(xpmlist)
    colors = np.array(["red","green","blue","yellow","pink","black","orange","purple","brown","cyan"])            
    plt.scatter(x,y, c=colors)
    for x,y in zip(x,y):
        label = f'Player{format(x)} xpm: {format(y)}'
        plt.annotate(label,(x,y))
    plt.show()

def notAllplayerXPMScatter(list):
    xpmlist = []
    amountplayers = []
    for item in list:
        xpmlist.append(playerslist[int(item)-1].xpm)
        amountplayers.append(int(item))
    x = np.array(amountplayers)
    y = np.array(xpmlist)
    plt.scatter(x,y)
    for x,y in zip(x,y):
        label = f'Player{format(x)} gpm: {format(y)}'
        plt.annotate(label,(x,y))
    plt.show()


def allPlayerGPMxNET():
    x = np.array ([playerslist[0].networth,playerslist[1].networth,playerslist[2].networth,playerslist[3].networth,playerslist[4].networth,playerslist[5].networth,playerslist[6].networth,playerslist[7].networth,playerslist[8].networth,playerslist[9].networth])
    y = np.array ([playerslist[0].gpm,playerslist[1].gpm,playerslist[2].gpm,playerslist[3].gpm,playerslist[4].gpm,playerslist[5].gpm,playerslist[6].gpm,playerslist[7].gpm,playerslist[8].gpm,playerslist[9].gpm])

    colors = np.array(["red","green","blue","yellow","pink","black","orange","purple","brown","cyan"])            
    plt.scatter(x,y, c=colors)
    plt.title('Gold per minute to net worth table')
    plt.xlabel('Networth')
    plt.ylabel('Gold per minute')
    plt.show()

def notAllplayerGPMxNET(list):
    networthlist = []
    gpmlist = []
    for item in list:
        networthlist.append(playerslist[int(item)-1].networth)
        gpmlist.append(playerslist[int(item)-1].gpm)
    x = np.array(networthlist)
    y = np.array(gpmlist)
    plt.scatter(x,y)
    for x,y in zip(x,y):
        label = f'{format(x)}: {format(y)}'
        plt.annotate(label,(x,y))
    plt.show()
    
def netWorthPieChart():
    networthlist = []
    labellist = []
    explodelist = [0]*10
    i = 0
    y = 0
    netcheck = 0
    #networthsortedlist = sorted(playerslist, key=lambda player: player.networth, reverse =True)
    for item in playerslist:
        networthlist.append(item.networth)
        labellist.append(item.name)
        i+=1
        if item.networth > netcheck: # Finding the highest networth and using the index int i to set that pie slice to explode
            netcheck = item.networth
            y = i
    explodelist[y-1] = 0.2
    y = np.array (networthlist)
    plt.pie(y, labels = labellist, explode = explodelist)
    plt.show()




#Welcome text that will be appended througout the project depending how the functionality is implemented        
def printWelcome():
    welcomestring = 'Välkommen till detta DOTA2 matchanalysverktyg börja med att ange ett matchid för att se statitik för matchen.\n ange sedan vilken statistik du vill se en analys för, skriv hjälp för hjälp'
    print(welcomestring)

printWelcome()
inputMatchID = input('Ange matchid: ')
fetchMatch(inputMatchID)
initplayers()
setheronames()
printScoreboard()
while True:
    commandLine = input('Ange statistik du vill se en tabell för: ').split(' ')
    if len(commandLine) == 1 and commandLine[0] == 'gpm'.lower():
        allPlayerGPMScatter()
    if len(commandLine) > 1 and commandLine[0] == 'gpm'.lower():
        del commandLine[0]
        notAllplayerGPMScatter(commandLine)
    if len(commandLine) == 1 and commandLine[0] == 'xpm'.lower():
        allPlayerXPMScatter()
    if len(commandLine) < 1 and commandLine[0] == 'xpm'.lower():
        del commandLine[0]
        notAllplayerXPMScatter(commandLine)
    if len(commandLine) == 1 and commandLine[0] == 'gold'.lower():
        allPlayerGPMxNET()
    if len(commandLine) == 1 and commandLine[0] == 'gold'.lower():
        del commandLine[0]
        notAllplayerGPMxNET(commandLine)
    if commandLine[0] == 'net'.lower():
        netWorthPieChart()
    








