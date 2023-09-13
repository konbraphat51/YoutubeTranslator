from YoutubeTranslator.Utils import Consts
from YoutubeTranslator.VideoGetter import VideoGetter
from YoutubeTranslator.Transcriber import TranscriberWhisper
from YoutubeTranslator.LanguageTranslator import LanguageTranslatorDeepl
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
        #download video
        VideoGetter(self.consts).run(video_link)

        #transcribe
        df_transcription, original_language = TranscriberWhisper(self.consts).run()

        #translate language
        df_translated = LanguageTranslatorDeepl(self.consts).run(df_transcription, original_language, self.consts.get_language_code_from_full(language_destination))
        df_translated.to_csv(self.consts.translation_text_path(), index=True)
        
if __name__ == "__main__":
    YoutubeTranslator(Consts("test", "APIkey.txt")).run("https://www.youtube.com/watch?v=ThhhNAMaJcw")