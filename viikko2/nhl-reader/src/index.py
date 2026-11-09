import requests

from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.prompt import Prompt

from player import Player

console = Console()


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

    def _get_players_by_nationality(self, players, nationality):
        result = []
        for player in players:
            if player.nationality != nationality:
                continue
            result.append(player)
        return result

    def top_scorers_by_nationality(self, nationality):
        players = self._get_players_by_nationality(
            self.reader.get_players(), nationality
        )

        def points(player):
            return player.goals + player.assists
        
        players = sorted(players, key=points, reverse=True)
        return players


def main():
    console.print()

    season = Prompt.ask(
        "Season [magenta][2018-19/2019-20/2020-21/2021-22/2022-23/"
        "2023-24/2024-25/2025-26][/magenta] [teal](2024-25)[/teal]",
        default="2024-25",
        console=console
    )
    
    url = f"https://studies.cs.helsinki.fi/nhlstats/{season}/players"
    reader = PlayerReader(url)
    stats = PlayerStats(reader)

    options = (
        "USA/FIN/CAN/SWE/CZE/RUS/SLO/FRA/GBR/SVK/DEN/NED/"
        "AUT/BLR/GER/SUI/NOR/UZB/LAT/AUS"
    )
    
    while True:
        console.print()
        nationality = Prompt.ask(
            f"Nationality [magenta][{options}][/magenta]",
            default="",
            console=console
        )

        if not nationality:
            break
        
        players = stats.top_scorers_by_nationality(nationality)

        console.print()
        console.print(
            f"        Season {season} players from {nationality}",
            style="grey70"
        )
        console.print()

        table = Table(
            show_header=True,
            header_style="bold white",
            border_style="white",
            show_lines=True,
            padding=(0, 2),
            expand=False
        )

        table.add_column("Released", style="#45d6c2", min_width=16)
        table.add_column("teams", style="#b48bea", min_width=6)
        table.add_column("goals", style="green", justify="right")
        table.add_column("assists", style="green", justify="right")
        table.add_column("points", style="green", justify="right")

        for player in players:
            table.add_row(
                player.name,
                player.team,
                str(player.goals),
                str(player.assists),
                str(player.goals + player.assists)
            )

        console.print(table)
        console.print()

if __name__=="__main__":
    main()