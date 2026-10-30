import unittest
from statistics_service import StatisticsService
from player import Player

class PlayerReaderStub:
    def get_players(self):
        return [
            Player("Semenko", "EDM", 4, 12),  #  4+12 = 16
            Player("Lemieux", "PIT", 45, 54), # 45+54 = 99
            Player("Kurri",   "EDM", 37, 53), # 37+53 = 90
            Player("Yzerman", "DET", 42, 56), # 42+56 = 98
            Player("Gretzky", "EDM", 35, 89)  # 35+89 = 124
        ]

class TestStatisticsService(unittest.TestCase):
    def setUp(self):
        # annetaan StatisticsService-luokan oliolle "stub"-luokan olio
        self.stats = StatisticsService(
            PlayerReaderStub()
        )

    def test_search_by_name_ok(self):
        player = self.stats.search("Kurri")
        self.assertEqual(str(player), "Kurri EDM 37 + 53 = 90")

    def test_search_unknown_player_ok(self):
        player = self.stats.search("Toope Tuntematon")
        self.assertIsNone(player)

    def test_team_list_ok(self):
        team = self.stats.team("EDM")
        team = [str(p) for p in team]
        
        ans = [
            "Semenko EDM 4 + 12 = 16",
            "Kurri EDM 37 + 53 = 90",
            "Gretzky EDM 35 + 89 = 124"
        ]

        self.assertEqual(team, ans)

    def test_top_player_ok(self):
        top = self.stats.top(1)
        self.assertEqual(top[0].name, "Gretzky")

    def test_num_top_players_ok(self):
        # under the assumption that top(n) 
        # correctly intends to return n+1 players
        top = self.stats.top(2)
        
        self.assertEqual(len(top), 3)


