import requests
from player import Player


class PlayerReader:
    def __init__(self, url):
        self.url = url

    def get_players(self):
        response = requests.get(self.url).json()
        
        players = []
        for d in response:
            players.append(Player(d))
        return players


class PlayerStats:
    def __init__(self, reader):
        self.reader = reader

    def top_scorers_by_nationality(self, nationality):
        players = self.reader.get_players()
        
        n_players = []
        for player in players:
            if player.nationality != nationality:
                continue
            n_players.append(player)

        def points(player):
            return player.goals + player.assists
        
        players = sorted(n_players, key=points, reverse=True)
        return players


def main():
    url = "https://studies.cs.helsinki.fi/nhlstats/2024-25/players"
    reader = PlayerReader(url)
    stats = PlayerStats(reader)

    players = stats.top_scorers_by_nationality("FIN")
    
    print("Players from FIN\n")
    for player in players:
        print(player)

if __name__=="__main__":
    main()