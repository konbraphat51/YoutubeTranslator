import pathlib
from typing import List

class Consts:
    class LanguageCode:
        def __init__(
            self,
            full: str,
            whisper: str,
            deepl: str
        ):
            self.full:str = full
            self.whisper:str = whisper
            self.deepl:str = deepl
    
    def __init__(self, api_txt: pathlib) -> None:
        self.working_directory:pathlib.Path = pathlib.Path(__file__).parent
        self.cache_directory:pathlib.Path = self.working_directory / "cache"
        
        self.original_video_file_name:str = "original_video.mp4"
        
        self.__initialize_api(api_txt)
        
        self.language_codes:List[Consts.LanguageCode] = [
            self.LanguageCode("English", "en", "EN-GB"),
            self.LanguageCode("Japanese", "ja", "JA"),
        ]
        
    def __initialize_api(self, api_txt: pathlib) -> None:
        with open(api_txt, "r") as f:
            #by row
            for row in f.readlines():
                name, key = row.split("=")
                
                if name == "deepl":
                    self.deepl_api_key:str = key
        
    def original_video_path(self) -> pathlib:
        '''
        Get path of original video file got from youtube.
        '''
        
        return self.cache_directory / self.original_video_file_name
    
    def get_language_code_from_full(self, full: str) -> LanguageCode:
        '''
        Get LanguageCode instance.
        '''
        
        for language_code in self.language_codes:
            if language_code.full == full:
                return language_code
        return None
    
    def get_language_code_from_whisper(self, whisper: str) -> LanguageCode:
        '''
        Get LanguageCode instance.
        '''
        
        for language_code in self.language_codes:
            if language_code.whisper == whisper:
                return language_code
        return None
    
    def get_language_code_from_deepl(self, deepl: str) -> LanguageCode:
        '''
        Get LanguageCode instance.
        '''
        
        for language_code in self.language_codes:
            if language_code.deepl == deepl:
                return language_code
        return None
    