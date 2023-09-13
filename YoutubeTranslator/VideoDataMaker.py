from YoutubeTranslator.Utils import Consts
import pandas as pd
from pydub import AudioSegment

class VideoDataMaker:
    '''
    Make data for making video.  
    Select what to do by parameters of run()
    '''
    
    def __init__(self, consts: Consts):
        self.consts = consts
    
    def run(
        self,
        df_translated: pd.DataFrame,
        should_make_dub: bool,        
    ):
        #must
        df_generated = self.make_single_audio(df_translated)
        
        #save df
        df_generated.to_csv((self.consts.project_directory / "generated.csv").as_posix(), index=True)
    
    def make_single_audio(self, df_translated: pd.DataFrame) -> pd.DataFrame:
        '''
        Make single audio file from translated text.  
        Output: DataFrame of (start, end, text, translated_text, generated_start, generated_end)
        '''
        
        #get files
        audio_file_pathes = [(self.consts.generated_sound_folder / f"{self.consts.project_title}_{index}.wav").as_posix() for index in range(df_translated.shape[0])]
        
        #initialize
        combined = AudioSegment.empty()
        starts = []
        ends = []
        
        #conbine
        for path in audio_file_pathes:
            audio = AudioSegment.from_file(path)
            starts.append(combined.duration_seconds)
            combined += audio
            ends.append(combined.duration_seconds)
            
        #save
        combined.export((self.consts.generated_sound_folder / "integrated.mp3").as_posix(), format="mp3")
        
        #add to df
        df_output = df_translated.copy()
        df_output["generated_start"] = starts
        df_output["generated_end"] = ends
        
        return df_output
    
if __name__ == "__main__":
    ins = VideoDataMaker(Consts("test", "APIkey.txt"))
    df_translation = pd.read_csv(ins.consts.translation_text_path(), index_col=0)
    ins.run(df_translation, True)