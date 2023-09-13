from YoutubeTranslator.Utils import Consts
import pandas as pd
from pydub import AudioSegment
import srt

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
        should_make_sub: bool,        
    ):
        #must
        df_generated = self.make_single_audio(df_translated)
        
        #save df
        df_generated.to_csv((self.consts.generated_translation_path()).as_posix(), index=True)
        
        #make sub
        if should_make_sub:
            self.make_sub(df_generated)
    
    def make_single_audio(self, df_translated: pd.DataFrame, format:str = "wav") -> pd.DataFrame:
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
        combined.export((self.consts.integrated_sound_path(format)).as_posix(), format=format)
        
        #add to df
        df_output = df_translated.copy()
        df_output["generated_start"] = starts
        df_output["generated_end"] = ends
        
        return df_output
    
    def make_sub(self, df_generated: pd.DataFrame) -> None:
        '''
        Make sub and save it as "sub.srt"
        '''
        
        #make individual sub
        subs = []
        for index, row in df_generated.iterrows():
            sub = srt.Subtitle(
                index=index,
                start=srt.timedelta(seconds=row["generated_start"]),
                end=srt.timedelta(seconds=row["generated_end"]),
                content=self.make_sub_text(row["text"], row["translated_text"])
            )
            subs.append(sub)
            
        #integrate
        sub_integrated = srt.compose(subs)
        
        #save
        with open((self.consts.srt_path()).as_posix(), "w", encoding="utf-8") as f:
            f.write(sub_integrated)
            
    def make_sub_text(self, text_before:str, text_after:str) -> str:
        '''
        Make sub text from before and after text.
        '''
        
        return f"{text_before}\n{text_after}"
    
if __name__ == "__main__":
    ins = VideoDataMaker(Consts("test", "APIkey.txt"))
    df_translation = pd.read_csv(ins.consts.translation_text_path(), index_col=0)
    ins.run(df_translation, True)