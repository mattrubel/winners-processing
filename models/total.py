from decimal import Decimal


class Total:
    def __init__(self, game_collection_key: str, points: Decimal, over_price: Decimal, under_price: Decimal):
        self.game_collection_key = game_collection_key
        self.points = points
        self.over_price = over_price
        self.under_price = under_price
