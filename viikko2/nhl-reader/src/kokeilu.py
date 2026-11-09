from index import PlayerReader, PlayerStats

# pylint: disable=invalid-name
url = "https://studies.cs.helsinki.fi/nhlstats/2026-27/players"
stats = PlayerStats(PlayerReader(url))

for p in stats.top_scorers_by_team("DAL"):
    print(p)
