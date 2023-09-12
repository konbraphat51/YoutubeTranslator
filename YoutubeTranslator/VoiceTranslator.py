from YoutubeTranslator.Utils import Consts
from VALLEX.utils.prompt_making import make_prompt
from VALLEX.utils.generation import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav
import pandas as pd
from pydub import AudioSegment
import pathlib

class VoiceTranslator:
    '''
    Translate voice data according to the translated text data.
    '''
    
    def __init__(self, consts: Consts):
        self.consts = consts
        
    def run(self, df_translated: pd.DataFrame) -> None:
        '''
        input: pd.DataFrame(start, end, text, translated_text)
        '''
        for index, row in df_translated.iterrows():
            self.translate(index, row)
        
    def translate(self, index:int, row_translation: pd.Series) -> None:
        '''
        input: row of pd.DataFrame(start, end, text, translated_text)
        '''
        
        raise NotImplementedError("You must implement this method in a subclass.")
    
class VoiceTranslatorVALLEX(VoiceTranslator):
    '''
    Using VALLEX.
    '''
    def __init__(self, consts: Consts):
        super().__init__(consts)
        preload_models()
    
    def translate(self, index:int, row_translation: pd.Series) -> None:
        #cut
        cut_file_path = self.cutoff_original(index, int(row_translation["start"]*1000), int(row_translation["end"]*1000))
        
        #sample voice
        prompt_name = self.sample_voice(index, cut_file_path, row_translation["text"])
        
        #generate
        generation_sound_path = self.generate_voice(prompt_name, row_translation["translated_text"])
        
        return generation_sound_path
        
    def cutoff_original(self, index:int, start:int, end:int) -> pathlib.Path:
        '''
        make cutted original sound file.
        output: path of cutted original sound file
        '''
        
        #cut
        original_audio = AudioSegment.from_file(self.consts.original_video_path().as_posix())
        sound_cut = original_audio[start:end]
        
        #save
        cut_path = self.consts.original_sound_cut_folder / f"{index}.mp3"
        sound_cut.export(cut_path.as_posix(), format="mp3")
        
        return cut_path
    
    def sample_voice(self, index:int, cut_file_path:str, transcription:str) -> str:
        '''
        sample voice from cutted original sound file.
        output: prompt name made
        '''
        
        prompt_name = f"{self.consts.project_title}_{index}"
        
        make_prompt(
            name = prompt_name,
            audio_prompt_path=cut_file_path,
            transcript=transcription
        )
        
        return prompt_name
    
    def generate_voice(self, prompt_name:str, text_generating:str) -> pathlib.Path:
        '''
        generate voice from prompt.
        output: path of generated voice file
        '''
        
        #generate
        audio = generate_audio(
            text_generating,
            prompt=prompt_name
        )
        
        #save
        generated_path = self.consts.generated_sound_folder / f"{prompt_name}.wav"
        write_wav(generated_path.as_posix(), SAMPLE_RATE, audio)
        
        return generated_path
    
if __name__ == "__main__":
    ins = VoiceTranslatorVALLEX(Consts("test", "APIkey.txt"))
    df_translation = pd.read_csv(ins.consts.translation_text_path())
    ins.run(df_translation)