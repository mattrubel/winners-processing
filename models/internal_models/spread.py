from decimal import Decimal


class Spread:
    def __init__(self, game_collection_key: str, team_name: str, points: Decimal, price: Decimal):
        self.game_collection_key = game_collection_key
        self.team_name = team_name
        self.points = points
        self.price = price
