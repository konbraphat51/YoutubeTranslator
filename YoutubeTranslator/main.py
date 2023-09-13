from YoutubeTranslator.Utils import Consts
from YoutubeTranslator.VideoGetter import VideoGetter
from YoutubeTranslator.Transcriber import TranscriberWhisper
from YoutubeTranslator.LanguageTranslator import LanguageTranslatorDeepl
from YoutubeTranslator.VoiceTranslator import VoiceTranslatorVALLEXAllPrompt, VoiceTranslatorVALLEXSingle
from YoutubeTranslator.VideoDataMaker import VideoDataMaker

class YoutubeTranslator:
    def __init__(self, consts: Consts):
        self.consts = consts
        
    def run(
        self,
        video_link: str,
        voice_translation_option:str = "vallex_all_prompt",
        language_destination:str = "English"
    ):
        '''
        Args:
            voice_translation_option: "vallex_all_prompt", "vallex_one_prompt"
            "vallex_all_prompt": Using VoiceTranslatorVALLEXAllPrompt
            "vallex_one_prompt": Using VoiceTranslatorVALLEXSingle
        '''
        
        #download video
        VideoGetter(self.consts).run(video_link)

        #transcribe
        df_transcription, original_language = TranscriberWhisper(self.consts).run()

        #translate language
        df_translated = LanguageTranslatorDeepl(self.consts).run(df_transcription, original_language, self.consts.get_language_code_from_full(language_destination))
        df_translated.to_csv(self.consts.translation_text_path(), index=True)
        
        #translate voice
        if voice_translation_option == "vallex_all_prompt":
            VoiceTranslatorVALLEXAllPrompt(self.consts).run(df_translated)
        elif voice_translation_option == "vallex_one_prompt":
            VoiceTranslatorVALLEXAllPrompt(self.consts).run(df_translated)
            
            print(
                "Please input prompt name from customs folder in your working directory. \n"\
                "You can compare prompt by listening to output/(this_project_name)/generated_sound/(index).mp3."
            )
            
            #wait for user
            while True:
                prompt = input()
                
                if VoiceTranslatorVALLEXSingle.check_prompt_exists(self.consts, prompt):
                    break
                else:
                    print("Invalid prompt. Please input again. Prompt should exists from customs folder in your working directory.")
                
            #apply
            VoiceTranslatorVALLEXSingle(self.consts, prompt).run(df_translated)
        
        #make video data
        VideoDataMaker(self.consts).run(df_translated, should_make_sub=True)
                
if __name__ == "__main__":
    YoutubeTranslator(Consts("test", "APIkey.txt")).run("https://www.youtube.com/watch?v=ThhhNAMaJcw")