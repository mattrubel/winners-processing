class Book:
    def __init__(self, name: str, active: bool = True, regulated: bool = False):
        self.name = name
        self.active = active
        self.regulated = regulated

    def set_active(self, flag: bool):
        self.active = flag

    def set_regulated(self, flag: bool):
        self.regulated = flag
