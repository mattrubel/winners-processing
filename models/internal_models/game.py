class Game:
    def __init__(self, market_key: str, home_team_key: str, away_team_key: str, commence_time: str):
        self.market_key = market_key
        self.home_team_key = home_team_key
        self.away_team_key = away_team_key
        self.commence_time = commence_time
        self.game_key = hash(market_key + home_team_key + away_team_key + commence_time)
