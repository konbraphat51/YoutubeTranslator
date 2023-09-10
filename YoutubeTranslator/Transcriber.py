from typing import Tuple
from YoutubeTranslator.Utils import Consts
from faster_whisper import WhisperModel
import pandas as pd

class Transcriber:
    '''
    Transcribes video to text data.
    '''
    
    def __init__(self, consts: Consts, model_name: str = "large-v2"):
        self.consts = consts
        self.model_name = model_name
    
    def run(self) -> Tuple[pd.DataFrame, Consts.LanguageCode]:
        '''  
        output: [DataFrame(start, end, transcription), language]
        '''
        df_transcription, lang = self.transcribe(self.consts.original_video_path().as_posix())
        
        #convert language code
        lang_code = self.consts.get_language_code_from_whisper(lang)
        
        return (df_transcription, lang_code)
    
    def transcribe(self, audio_file_name: str):
        model = WhisperModel(self.model_name, device="cuda")
        segments, info = model.transcribe(audio_file_name)
        
        #convert into pd.DataFrame
        transcriptions = []
        for segment in segments:
            transcriptions.append([segment.start, segment.end, segment.text])
        df_transcription = pd.DataFrame(transcriptions, columns=["start", "end", "text"])
        
        return (df_transcription, info.language)
    
if __name__ == "__main__":
    transcriber = Transcriber(Consts("APIkey.txt"))
    print(transcriber.run()[1])