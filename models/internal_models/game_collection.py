class GameCollection:
    def __init__(self, book_key: str, game_key: str, last_update: str, collection_time: str = None):
        self.book_key = book_key
        self.game_key = game_key
        self.last_update = last_update
        self.collection_time = collection_time
        self.game_collection_key = hash(book_key + game_key + last_update + collection_time)
