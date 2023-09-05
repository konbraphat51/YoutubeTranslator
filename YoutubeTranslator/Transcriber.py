from YoutubeTranslator.Utils import Consts
from faster_whisper import WhisperModel
import pandas as pd

class Transcriber:
    '''
    Transcribes video to text data.
    '''
    
    def __init__(self, consts: Consts):
        self.consts = consts
        self.model_name = "large-v2"
    
    def run(self, file_name: str):
        '''
        input: file path of video to transcribe  
        output: [pandas.DataFrame(start, end, text), language(str)]
        '''
        df_transcription, lang = self.transcribe(file_name)
        
        return [df_transcription, lang]
    
    def transcribe(self, file_name: str):
        model = WhisperModel(self.model_name, device="cuda")
        
        segments, info = model.transcribe(file_name)
        
        transcriptions = []
        for segment in segments:
            transcriptions.append([segment.start, segment.end, segment.text])
            
        df_transcription = pd.DataFrame(transcriptions, columns=["start", "end", "text"])
        
        return df_transcription, info["language"]