import requests

from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt

from player import Player

console = Console()

# pylint: disable=too-few-public-methods
class PlayerReader:
    def __init__(self, url):
        self.url = url

    def get_players(self):
        response = requests.get(self.url, timeout=4).json()

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

        players = sorted(players, key=self._points, reverse=True)
        return players

    def _get_players_by_team(self, players, team):
        return [player for player in players if player.team == team]

    @staticmethod
    def _points(player):
        return player.goals + player.assists

    def top_scorers_by_team(self, team):
        players = self._get_players_by_team(self.reader.get_players(), team)
        return sorted(players, key=self._points, reverse=True)

    def top_goal_scorers(self, how_many):
        """Returns how_many top goal-scoring players by goal count descending"""
        players = sorted(
            self.reader.get_players(),
            key=lambda player: player.goals,
            reverse=True
        )
        return players[:how_many]


def create_table(stats):
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

    for player in stats:
        table.add_row(
            player.name,
            player.team,
            str(player.goals),
            str(player.assists),
            str(player.goals + player.assists)
        )

    return table

def main():
    # pylint: disable=too-many-statements
    season = Prompt.ask(
        "Season [magenta][2018-19/2019-20/2020-21/2021-22/2022-23/"
        "2023-24/2024-25/2025-26][/magenta] [teal](2024-25)[/teal]",
        default="2024-25",
        console=console
    )

    stats = PlayerStats(PlayerReader(
        f"https://studies.cs.helsinki.fi/nhlstats/{season}/players"
    ))

    options = (
        "USA/FIN/CAN/SWE/CZE/RUS/SLO/FRA/GBR/SVK/DEN/NED/"
        "AUT/BLR/GER/SUI/NOR/UZB/LAT/AUS"
    )

    while True:
        console.print()
        search_type = Prompt.ask(
            "Search by [magenta][nationality/team][/magenta] (blank to quit)",
            choices=["nationality", "team", ""],
            default="",
            console=console
        )

        if not search_type:
            break

        if search_type == "nationality":
            value = Prompt.ask(
                f"Nationality [magenta][{options}][/magenta]",
                console=console
            )
            players = stats.top_scorers_by_nationality(value)
            description = f"players from {value}"
        else:
            value = Prompt.ask("Team abbreviation", console=console)
            players = stats.top_scorers_by_team(value)
            description = f"players in {value}"

        console.print(
            f"        Season {season} {description}\n",
            style="grey70"
        )

        console.print(create_table(players))

if __name__=="__main__":
    main()
