class Market:
    def __init__(self, market_key: str, sport: str, title: str, description: str, active: bool, futures: bool):
        self.market_key = market_key
        self.sport = sport
        self.title = title
        self.description = description
        self.active = active
        self.futures = futures
        self.collect = False

    def toggle_collection(self, collect_flag: bool):
        self.collect = collect_flag
