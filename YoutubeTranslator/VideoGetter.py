import pytube
from YoutubeTranslator.Utils import Consts

class VideoGetter:
    def __init__(self):
        self.file_name = "original.mp4"
    
    def run(self, url):
        '''
        input: url of youtube video to process
        output: file name of downloaded video
        '''
        
        self.download(url)
        return self.file_name
        
    def download(self, url):
        yt = pytube.YouTube(url)
        return yt.streams.filter(file_extension='mp4').first().download(filename=self.file_name)
    
if __name__ == "__main__":
    VideoGetter().run("https://www.youtube.com/watch?v=ThhhNAMaJcw")