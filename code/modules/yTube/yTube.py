from pytube import YouTube
from urllib import parse, request
import re
import os

import threading

YOUTUBE_URL = 'https://www.youtube.com'
ERROR_LOG_REQUEST = 'a'
LIMIT_EXCEED_MESSAGE = 'mucho'
ERROR_NOT_FOUND = 'a'

source = lambda source: YouTube(source)

def thread(func):
    def wrapper(*args, **kwargs):    
        download_thread = threading.Thread(target=lambda: func(*args, **kwargs))
        download_thread.start()
    return wrapper

def download(func):
    def wrapper():
        pytube_object = func()
        pytube_object.download(dir)
    return wrapper
        

def search(search: str,console: bool=False,log: bool=True,cant: int=1) -> str:
    """
    Searchs for a youtube video
    returns a list with cant=youtube_links - default: 1

    """
    query_string = parse.urlencode({"search_query": search})
    search_results = []
    
    try:
        html_content = request.urlopen(f"{YOUTUBE_URL}/results?" + query_string)
        search_results = re.findall("watch\?v=(.{11})", html_content.read().decode("utf-8"))
        if console == True: 
            print(search_results)              
    except: 
        if log == True: 
            print(ERROR_LOG_REQUEST)     
      
    links = [f"{YOUTUBE_URL}/watch\?v={search_results[i]}" 
             for i in (range(cant if cant < len(search_results) else len(search_results)))] 
        
    return links

def downloadAudioYT(source: str, dir:str, filename:str='', size_limit_mb: int = 1024):
    """
    Downloads a yt audio link (use search)
    returns the path where the file was downloaded
    """
    pytube_video = YouTube(source)
    audio = pytube_video.streams.get_audio_only()  
    
    if (audio.filesize / 1024 )/1024 > size_limit_mb:
        return LIMIT_EXCEED_MESSAGE
    
    path = audio.download(dir)      
    return path
    

def downloadAudioFromList(sources: list,*args, **kwargs): 
    """ Give search function as argument"""
    for source in sources:
        try:
            dw_path = downloadAudioYT(source)
            if dw_path != LIMIT_EXCEED_MESSAGE:
                return dw_path
            
        except: pass

    return ERROR_NOT_FOUND


@thread
def downloadVideo(source, dir, quality="high"):   

    video = YouTube(source)
    if quality=="low":
        video.streams.first().download(dir)
            
    elif quality=="high":
            video.streams.filter(progressive=True).get_highest_resolution().download(dir) 
    
    else:
        raise TypeError

    return source


def downloadedList(dir, separator=">"):
    videos = os.listdir('../files/ytDownloads')
    videos = f"{separator} " + f"\n{separator} ".join(videos)  
    return videos




#--DEBUG--#
def __test():
    # lin = search("guaasrsa")[0]
    # print(lin)
    # yt = source(lin)
    # print(yt.streams)
   # print(yt.streams)
   print(downloadAudioYT(search('elira pendora shoujo')[0], dir=this))



if __name__ == "__main__":
    this = './test/'
    
    __test()