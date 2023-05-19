import requests
import json
import matplotlib.pyplot as plt
import numpy as np
#klass för match som jag initialt trodde skulle behövas men är tveksam nu finns kvar för stunden
class match:
    def __init__(self, id, playerlist):
        self.id = id
        self.player = playerlist
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

#response = requests.get ("https://api.opendota.com/api/matches/7118189341") 
#mydict = json.loads(response.text)

#with open('match.json', 'w') as datafh:
#    json.dump(mydict, datafh, indent = 4)         kod som använts för att hämta information från en match men som nu är utkommenterad för att labba med en konstant JSONfil i nuläget
#lista för att kunna stoppa in objekten spelare från matchen

playerslist = []

# öppnar och laddar JSONfilen
with open ('match.json') as datafh:
    data = json.load(datafh)
#generellt labbanda kring att plocka ut information för varje spelare och appenda plarslist med
players = data['players']
for key in players:
    print(key['match_id'])
    print(key['gold_per_min'])
    p = player(key['player_slot'], key['gold_per_min'], key['xp_per_min'], key['kills'], key['deaths'], key['assists']) #initierar 
    playerslist.append(p)

# genereellt smålabbande kring matplotlib och hur spelares statistik kan användas för att visas upp i det 
x = np.array([1,2,3,4,5,6,7,8,9,10])
y = np.array([playerslist[0].gpm,playerslist[1].gpm,playerslist[2].gpm,playerslist[3].gpm,playerslist[4].gpm,playerslist[5].gpm,playerslist[6].gpm,playerslist[7].gpm,playerslist[8].gpm,playerslist[9].gpm])
colors = np.array(["red","green","blue","yellow","pink","black","orange","purple","brown","cyan"])            
plt.scatter(x,y, c=colors)
plt.show()
for p in playerslist:
    print(repr(p))