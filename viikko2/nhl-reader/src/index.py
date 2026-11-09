import requests
from player import Player

def main():
    url = "https://studies.cs.helsinki.fi/nhlstats/2024-25/players"
    response = requests.get(url).json()

    players = []

    for player_dict in response:
        player = Player(player_dict)
        players.append(player)

    fin_players = []
    for player in players:
        if player.nationality != "FIN":
            continue
        fin_players.append(player)
    
    def points(player):
        return player.goals + player.assists

    players = sorted(fin_players, key=points, reverse=True)

    print("Players from FIN")
    for player in players:
        print(player)

if __name__=="__main__":
    main()