import pathlib

class Consts:
    def __init__(self):
        self.working_directory = pathlib.Path(__file__).parent
        self.cache_directory = self.working_directory / "cache"
        
        self.original_video_file_name = "original_video.mp4"
        
    def original_video_path(self):
        return self.cache_directory / self.original_video_file_name