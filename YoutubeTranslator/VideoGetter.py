import pytube
from YoutubeTranslator.Utils import Consts
import pathlib

class VideoGetter:
    '''
    Downloads video from youtube.  
    The file will be save in cache/original.mp4
    '''
    
    def __init__(self, consts: Consts):
        self.consts = consts        
    
    def run(self, url: str) -> pathlib.Path:
        '''
        input: url of youtube video to process  
        output: mp4path
        '''
        
        self.download(url)
        
        return self.consts.original_video_path()
        
    def download(self, url):
        yt = pytube.YouTube(url)
        
        #mp4
        yt.streams.filter(file_extension='mp4').first().download(filename=self.consts.original_video_path())
    
if __name__ == "__main__":
    VideoGetter(Consts("APIkey.txt")).run("https://www.youtube.com/watch?v=ThhhNAMaJcw")