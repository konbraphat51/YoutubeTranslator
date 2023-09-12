import pathlib
from typing import List
from os import mkdir

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
    
    def __init__(self, project_title:str, api_txt: pathlib) -> None:
        self.project_title:str = project_title
        
        self.working_directory:pathlib.Path = pathlib.Path(__file__).parent
        self.project_directory:pathlib.Path = self.working_directory / "output" / self.project_title
        
        #make directory in advance
        if not self.project_directory.exists():
            mkdir(self.project_directory)
        
        self.original_video_file_name:str = "original_video.mp4"
        self.translation_text_file_name:str = "translation_text.csv"
        
        self.original_sound_cut_folder:pathlib.Path = self.project_directory / "original_sound_cut"
        if not self.original_sound_cut_folder.exists():
            mkdir(self.original_sound_cut_folder)
        
        self.generated_sound_folder:pathlib.Path = self.project_directory / "generated_sound"
        if not self.generated_sound_folder.exists():
            mkdir(self.generated_sound_folder)
        
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
        
        return self.project_directory / self.original_video_file_name
    
    def translation_text_path(self) -> pathlib:
        '''
        Get path of translation text file.
        '''
        
        return self.project_directory / self.translation_text_file_name
    
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