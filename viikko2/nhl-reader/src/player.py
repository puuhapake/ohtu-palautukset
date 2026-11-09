class Player:
    # pylint: disable=too-few-public-methods
    def __init__(self, player_dict):
        self.name = player_dict['name']
        self.nationality = player_dict['nationality']
        self.team = player_dict['team']
        self.games = player_dict['games']
        self.goals = player_dict['goals']
        self.assists = player_dict['assists']

    # deprecated
    def __str__(self):
        _name = f"{self.name:24}"
        _team = f"{self.team:16}"
        _points = f"{self.goals:2} + {self.assists:2} = "
        _total_points = f"{(self.goals+self.assists):3}"
        return _name + _team + _points + _total_points
