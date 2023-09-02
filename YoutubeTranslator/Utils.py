import pathlib

class Consts:
    def __init__(self):
        self.working_directory = pathlib.Path(__file__).parent
        self.cache_directory = self.working_directory / "cache"