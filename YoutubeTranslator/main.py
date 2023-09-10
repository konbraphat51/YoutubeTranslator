from YoutubeTranslator.Utils import Consts
from YoutubeTranslator.VideoGetter import VideoGetter
from YoutubeTranslator.Transcriber import Transcriber
from YoutubeTranslator.LanguageTranslator import LanguageTranslator
# from YoutubeTranslator.VoiceSampler import VoiceSampler
# from YoutubeTranslator.VoiceTranslator import VoiceTranslator

class YoutubeTranslator:
    def __init__(self, consts: Consts):
        self.consts = consts
        
    def run(
        self,
        video_link: str,
        language_destination:str = "English"
    ):
        VideoGetter(self.consts).run(video_link)
        df_transcription, original_language = Transcriber(self.consts).run()
        df_translated = LanguageTranslator(self.consts).run(df_transcription, original_language, self.consts.get_language_code_from_full(language_destination))
        
        print(df_translated)
        
if __name__ == "__main__":
    YoutubeTranslator(Consts("APIkey.txt")).run("https://www.youtube.com/watch?v=ThhhNAMaJcw")