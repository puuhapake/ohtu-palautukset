"""Unit tests for PlayerStats using an in-memory PlayerReader stub."""

import sys
import unittest
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from index import PlayerStats


class StubPlayerReader:
    """Return predefined players without making any network requests."""

    def __init__(self, players):
        self.players = players

    def get_players(self):
        return self.players


def make_player(name, nationality, team, goals, assists):
    return SimpleNamespace(
        name=name,
        nationality=nationality,
        team=team,
        goals=goals,
        assists=assists,
    )


class TestPlayerStats(unittest.TestCase):
    def setUp(self):
        self.players = [
            make_player("Alex", "FIN", "DAL", 10, 20),
            make_player("Blake", "USA", "DAL", 15, 5),
            make_player("Casey", "FIN", "BOS", 12, 15),
            make_player("Drew", "FIN", "DAL", 8, 12),
        ]
        self.stats = PlayerStats(StubPlayerReader(self.players))

    def test_top_scorers_by_nationality_filters_and_sorts_by_points(self):
        result = self.stats.top_scorers_by_nationality("FIN")

        self.assertEqual(
            [player.name for player in result], ["Alex", "Casey", "Drew"]
        )

    def test_top_scorers_by_team_filters_and_sorts_by_points(self):
        result = self.stats.top_scorers_by_team("DAL")

        self.assertEqual(
            [player.name for player in result], ["Alex", "Blake", "Drew"]
        )

    def test_top_scorers_by_team_returns_empty_list_for_unknown_team(self):
        self.assertEqual(self.stats.top_scorers_by_team("XXX"), [])

    def test_top_goal_scorers_sorts_by_goals_and_limits_results(self):
        result = self.stats.top_goal_scorers(2)

        self.assertEqual([player.name for player in result], ["Blake", "Casey"])


if __name__ == "__main__":
    unittest.main()
