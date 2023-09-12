from YoutubeTranslator.Utils import Consts
import pandas as pd
from typing import List
import deepl

class LanguageTranslator:
    '''
    Translate transcribed text data to another language.
    '''
    
    def __init__(self, consts: Consts):
        self.consts = consts
        
    def run(
        self,
        df_transcription: pd.DataFrame,
        original_language: Consts.LanguageCode,
        destination_language: Consts.LanguageCode
    ) -> pd.DataFrame:
        '''
        output: pd.DataFrame(start, end, text, translated_text)
        '''
        
        output = []
        translated_texts = self.translate(list(df_transcription["text"]), original_language, destination_language)
        
        df_output = df_transcription.copy()
        df_output["translated_text"] = translated_texts
        
        return df_output
    
    def translate(self, texts: List[str], original_language: Consts.LanguageCode, destination_language: Consts.LanguageCode) -> List[str]:
        '''
        input: list of text
        output: list of translated text
        '''
        raise NotImplementedError("You must implement this method in a subclass.")
            
class LanguageTranslatorDeepl(LanguageTranslator):
    def translate(self, texts: List[str], original_language: Consts.LanguageCode, destination_language: Consts.LanguageCode) -> List[str]:
        #using deepl
        translator = deepl.Translator(self.consts.deepl_api_key)
        
        results = translator.translate_text(
            texts,
            source_lang=original_language.deepl,
            target_lang=destination_language.deepl
        )
        
        results_texts = []
        for result in results:
            results_texts.append(result.text)
        
        return results_texts