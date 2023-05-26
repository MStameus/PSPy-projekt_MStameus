import requests
import json
import matplotlib.pyplot as plt
import numpy as np

# klass för spelare som kan initiaras med divierse stats från matchen
class player:
    def __init__(self, slot, gpm, xpm, kills, deaths, assists, networth, name, accountid):
        self.slot = slot
        self.gpm = gpm
        self.xpm = xpm
        self.kills = kills
        self.deaths = deaths
        self.assists = assists
        self.networth = networth
        self.name = name
        self.accountid = accountid
    def __repr__(self):
        return repr(f'Player <slot> {self.slot}, <gpm> {self.gpm}, <xpm> {self.xpm}, <kills> {self.kills}, <deaths> {self.deaths}, <assists>, {self.assists}')
    def setname(self, newname):
        self.name = newname

# list wich will contain the players and accessed in methods to easily access relevant stats
playerslist = []

# Method for getting information from match and writing it on JSON file
def fetchMatch(IDstring):
    response = requests.get (f'https://api.opendota.com/api/matches/{IDstring}') 
    mydict = json.loads(response.text)

    with open('match1.json', 'w') as datafh:
        json.dump(mydict, datafh, indent = 4)

def saveMatchData(): #uses the data in the file that fetchMatch initially writes on to save to user named file
    outfilename = input('Namnge matchen för att spara den: ')
    with open  ('match1.json') as datafh:
        data = json.load(datafh) 
    with open(f'{outfilename}.json', 'w') as output:
        json.dump(data, output, indent=4)
    print(f'Matchen har sparats lokalt som {outfilename}.json !')

#Method for printing a basic scoreboard
def printScoreboard():
    print('Matchlängd: %.2f '% matchtime + 'minuter')
    index = 1 #used for indexing each player for the user 
    for player in playerslist:
        print(f'Player{index}: {player.name} GPM: {player.gpm}, XPM: {player.xpm}: KDA: {player.kills}/{player.deaths}/{player.assists} ')
        index +=1

# Method for initiating players from the match1.json file and appending the playerslist
def initplayers():
    with open ('match1.json') as datafh:
        data = json.load(datafh) 
    players = data['players']    
    for key in players:
        p = player(key['player_slot'], key['gold_per_min'], key['xp_per_min'], key['kills'], key['deaths'], key['assists'], key['net_worth'], key['hero_id'],key['account_id']) #initierar 
        playerslist.append(p)

def settime():
    with open ('match1.json') as datafh:
         data = json.load(datafh)     
    return data['duration']/60

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
    labellist = []
    for i in range(len(playerslist)):
        amountplayers.append(i+1)
    for item in playerslist:
        gpmlist.append(item.gpm)
        labellist.append(item.name)
    x = np.array(amountplayers)
    y = np.array(gpmlist)            
    plt.scatter(x,y)
    i = 0
    for x,y in zip(x,y):
        plt.annotate(labellist[i],(x,y), rotation = 60)
        i+=1
    plt.title('Gold per minute comparison')
    plt.xlabel('Spelare')
    plt.ylabel('Gold per minute')
    plt.grid()
    plt.show()

def notAllplayerGPMScatter(list):
    gpmlist = []
    amountplayers = []
    try:
        for item in list:
            gpmlist.append(playerslist[int(item)-1].gpm)
            amountplayers.append(playerslist[int(item)-1].name)
    except IndexError:
        print('At least one player index is invalid')
        return
    x = np.array(amountplayers)
    y = np.array(gpmlist)
    plt.scatter(x,y)
    i = 0
    for x,y in zip(x,y):
        plt.annotate(amountplayers[i],(x,y), rotation = 60)
        i+=1
    plt.title('Gold per minute comparison')
    plt.xlabel('Spelare')
    plt.ylabel('Gold per minute')
    plt.show()

#
def allPlayerXPMScatter():  
    xpmlist = []
    amountplayers = []
    labellist = []
    for i in range(len(playerslist)):
        amountplayers.append(i+1)    
    for item in playerslist:
        xpmlist.append(item.xpm)
        labellist.append(item.name)       
    x = np.array(amountplayers)
    y = np.array(xpmlist)          
    plt.scatter(x,y)
    i = 0
    for x,y in zip(x,y):
        plt.annotate(labellist[i],(x,y), rotation = 60)
        i+=1
    plt.title('experience per minute comparison')
    plt.xlabel('Spelare')
    plt.ylabel('Experience per minute')
    plt.grid()
    plt.show()

def notAllplayerXPMScatter(list):
    xpmlist = []
    amountplayers = []
    try:
        for item in list:
            xpmlist.append(playerslist[int(item)-1].xpm)
            amountplayers.append(playerslist[int(item)-1].name)
    except IndexError:
        print('At least one player index is invalid')
        return
    x = np.array(amountplayers)
    y = np.array(xpmlist)
    plt.scatter(x,y)
    i = 0
    for x,y in zip(x,y):
       plt.annotate(amountplayers[i],(x,y), rotation = 60)
       i+=1
    plt.title('experience per minute comparison')
    plt.xlabel('Hero')
    plt.ylabel('Experience per minute')
    plt.show()


def allPlayerGPMxNET():
    networthlist = []
    gpmlist = []
    labellist =[]
    for item in playerslist:
        networthlist.append(item.networth)
        gpmlist.append(item.gpm)
        labellist.append(item.name)
    x = np.array (networthlist)
    y = np.array (gpmlist)
    plt.subplot(2,1,1)
    plt.xlabel('Networth')
    plt.ylabel('Gold per minute')
    plt.scatter(x,y)
    i = 0
    for x,y in zip(x,y):
        plt.annotate(labellist[i],(x,y), rotation = 60)
        i+=1            
    
    #plt.title('Gold per minute to net worth table')
    plt.grid()

    networthlist2 = []
    labellist2 = []
    explodelist = [0]*10
    i = 0
    y = 0
    netcheck = 0
    for item in playerslist:
        networthlist2.append(item.networth)
        labellist2.append(item.name)
        i+=1
        if item.networth > netcheck: # Finding the highest networth and using the index int i to set that pie slice to explode
            netcheck = item.networth
            y = i
    explodelist[y-1] = 0.2
    y = np.array (networthlist2)
    plt.title('Gold statistics')
    plt.subplot(2,1,2)
    plt.pie(y, labels = labellist2, autopct = '%1.f%%', explode = explodelist)



    plt.show()

def notAllplayerGPMxNET(list):
    networthlist = []
    gpmlist = []
    labellist = []
    for item in list:
        networthlist.append(playerslist[int(item)-1].networth)
        gpmlist.append(playerslist[int(item)-1].gpm)
        labellist.append(playerslist[int(item)-1].name)
    x = np.array(networthlist)
    y = np.array(gpmlist)
    plt.scatter(x,y)
    i = 0
    for x,y in zip(x,y):
        plt.annotate(labellist[i],(x,y), rotation = 60)
        i+=1
    plt.title('Gold per minute to net worth table')
    plt.xlabel('Networth')
    plt.ylabel('Gold per minute')
    plt.grid()
    plt.show()

def gpmvnetpm(list):
    netperminlist = [] #list used for storing net worth per minute values apllied to the x axis of the table
    gpmlist = [] # list used for storing gold per minute values apllied to the y axis of the table
    labellist = []  
    labellisteffic = [] # two separate lists for storing the point labels in this case hero name and percntage of gold earned that is in the heros networth at finished game
    try: #user input list by inputting player indexes 1-10 is used to accessing playerslist and getting their elements
        for item in list:
            netperminlist.append(playerslist[int(item)-1].networth/matchtime)
            gpmlist.append(playerslist[int(item)-1].gpm)
            labellist.append(playerslist[int(item)-1].name)
            potential = playerslist[int(item)-1].gpm*matchtime #if 100% of gpm was converted in to networth
            labellisteffic.append(playerslist[int(item)-1].networth/potential*100) #percentage of gold converted in to networth
    except IndexError:
        print('At least one player index is invalid')
        return
    x = np.array(netperminlist)
    y = np.array(gpmlist)
    plt.scatter(x,y)
    i=0
    for x,y in zip(x,y):
        plt.annotate(f'{labellist[i]}: {labellisteffic[i]:.1f}%',(x,y), rotation = 60) 
        i+=1
    plt.title('Gold per minute vs networth per minute graph')
    plt.xlabel('Networth per minute')
    plt.ylabel('Gold per minute')
    plt.grid()
    plt.show()
    

def netWorthPieChart():
    networthlist = []
    labellist = []
    explodelist = [0]*10
    i = 0
    y = 0
    netcheck = 0
    for item in playerslist:
        networthlist.append(item.networth)
        labellist.append(item.name)
        i+=1
        if item.networth > netcheck: # Finding the highest networth and using the index int i to set that pie slice to explode
            netcheck = item.networth
            y = i
    explodelist[y-1] = 0.2
    y = np.array (networthlist)
    plt.title('percentage of total networth in game')
    plt.pie(y, labels = labellist, autopct = '%1.f%%', explode = explodelist)
    plt.show()

def init():
    printWelcome()
    while True:
        inputMatchID = input('Ange matchid: ')
        fetchMatch(inputMatchID)
        try:
            initplayers()
        except KeyError:
            print('matchid verkar inte vara giltigt')
        else:
            setheronames()
            break
        
    

def reinit():
    playerslist.clear() 
    while True:
        inputMatchID = input('Ange matchid: ')
        fetchMatch(inputMatchID)
        try:
            initplayers()
        except KeyError:
            print('matchid verkar inte vara giltigt')
        else:
            setheronames()
            break

#Welcome text that will be appended througout the project depending how the functionality is implemented        
def printWelcome():
    welcomestring = 'Välkommen till detta DOTA2 matchanalysverktyg börja med att ange ett matchid för att se statitik för matchen.\n ange sedan vilken statistik du vill se en analys för, skriv hjälp för hjälp'
    print(welcomestring) 

"""
Started method for comparison of different stats towards the players total amount of wins but during testing the requests for wins and losses only returned
errors. So this is on hold for now.
def winComparisonGraph(list):
    playerstatlist = []
    labellist = []
    winlist = []
    comparisonstat = ''
    list[0] = comparisonstat
    del list[0]
    if comparisonstat == 'gpm':
        for item in list:
            playerstatlist.append(playerslist[int(item)-1].gpm)
            labellist.append(playerslist[int(item)-1].name)
    elif comparisonstat == 'networth':
        for item in list:
            playerstatlist.append(playerslist[int(item)-1].networth)
            labellist.append(playerslist[int(item)-1].name)
    elif comparisonstat == 'kills':
        for item in list:
            playerstatlist.append(playerslist[int(item)-1].kills)
            labellist.append(playerslist[int(item)-1].name)
    for item in list:
"""


init()
matchtime = settime()
printScoreboard()
while True:
    commandLine = input('Ange kommando för att se statistik, spara match eller kolla en ny match: ').split(' ') #commandline list to be used for letting the user choose wich players to compare
    if len(commandLine) == 1 and commandLine[0] == 'gpm'.lower():
        allPlayerGPMScatter()
    elif len(commandLine) > 1 and commandLine[0] == 'gpm'.lower():
        del commandLine[0]
        notAllplayerGPMScatter(commandLine)
    elif len(commandLine) == 1 and commandLine[0] == 'xpm'.lower():
        allPlayerXPMScatter()
    elif len(commandLine) > 1 and commandLine[0] == 'xpm'.lower():
        del commandLine[0]
        notAllplayerXPMScatter(commandLine)
    elif len(commandLine) == 1 and commandLine[0] == 'gold'.lower():
        allPlayerGPMxNET()
    elif len(commandLine) > 1 and commandLine[0] == 'gold'.lower():
        del commandLine[0]
        notAllplayerGPMxNET(commandLine)
    elif len(commandLine)> 1 and commandLine[0] == 'eff'.lower():
        del commandLine[0]
        gpmvnetpm(commandLine)
    elif commandLine[0] == 'save'.lower():
        saveMatchData()
    elif commandLine[0] == 'net'.lower():
        netWorthPieChart()
    elif commandLine[0] == 'new'.lower():
        reinit()
        matchtime = settime()
        printScoreboard()
    elif commandLine[0] == 'quit'.lower():
        print('På återseende!')
        quit()
    else:
        print('okänt kommando skriv hjälp för hjälp')
    








