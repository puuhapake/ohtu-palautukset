class Player:
    def __init__(self, dict):
        self.name = dict['name']
        self.nationality = dict['nationality']
        self.team = dict['team']
        self.games = dict['games']
        self.goals = dict['goals']
        self.assists = dict['assists']
    
    def __str__(self):
        _name = f"{self.name:24}"
        _team = f"{self.team:16}"
        _points = f"{self.goals:2} + {self.assists:2} = "
        _total_points = f"{(self.goals+self.assists):3}"
        return _name + _team + _points + _total_points
