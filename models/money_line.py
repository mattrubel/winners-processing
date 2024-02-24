from decimal import Decimal


class MoneyLine:
    def __init__(self, game_collection_key: str, team_name: str, price: Decimal):
        self.game_collection_key = game_collection_key
        self.team_name = team_name
        self.price = price
