import pytube
from YoutubeTranslator.Utils import Consts

class VideoGetter:
    '''
    Downloads video from youtube.  
    The file will be save in cache/original.mp4
    '''
    
    def __init__(self, consts: Consts):
        self.consts = consts
        self.file_name = self.consts.cache_directory /  "original.mp4"
    
    def run(self, url: str):
        '''
        input: url of youtube video to process  
        output: file path of downloaded video
        '''
        
        return self.download(url)
        
    def download(self, url):
        yt = pytube.YouTube(url)
        return yt.streams.filter(file_extension='mp4').first().download(filename=self.file_name)
    
if __name__ == "__main__":
    VideoGetter(Consts()).run("https://www.youtube.com/watch?v=ThhhNAMaJcw")