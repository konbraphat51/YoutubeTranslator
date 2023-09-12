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
        
        return (df_transcription, lang)
    
    def transcribe(self, audio_file_name: str) -> Tuple[pd.DataFrame, Consts.LanguageCode]:
        '''
        input: audio file name
        output: [DataFrame(start, end, transcription), language]
        '''
        raise NotImplementedError("You must implement this method in a subclass.")
    
class TranscriberWhisper(Transcriber):
    def transcribe(self, audio_file_name: str) -> Tuple[pd.DataFrame, Consts.LanguageCode]:
        model = WhisperModel(self.model_name, device="cuda")
        segments, info = model.transcribe(audio_file_name)
        
        #convert into pd.DataFrame
        transcriptions = []
        for segment in segments:
            #connect in-the-row segments
            #if former end == this start
            if (len(transcriptions) > 0) and (segment.start - transcriptions[-1][1] < 0.1):
                transcriptions[-1][2] += " " + segment.text
                transcriptions[-1][1] = segment.end
            else:
                transcriptions.append([segment.start, segment.end, segment.text])
        df_transcription = pd.DataFrame(transcriptions, columns=["start", "end", "text"])
        
        return (df_transcription, self.consts.get_language_code_from_whisper(info.language))
    
if __name__ == "__main__":
    transcriber = TranscriberWhisper(Consts("test", "APIkey.txt"))
    print(transcriber.run()[1])