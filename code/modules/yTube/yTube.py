
from pytube import YouTube
from urllib import parse, request
import re
import os


downloads_dir = "../files/ytDownloads"

source = lambda source: YouTube(source)

def search(search, console = False, index = 0):
    query_string = parse.urlencode({"search_query": search})
    html_content = request.urlopen("https://www.youtube.com/results?" + query_string)
    search_results = re.findall("watch\?v=(.{11})", html_content.read().decode("utf-8"))
    
    if console == True: 
        print(search_results)
        
    return f"https://www.youtube.com/watch\?v={search_results[index]}" 


    
def download(source, quality="high", dir = downloads_dir):
    pytube_video = YouTube(source)
    
    if quality=="low":
        pytube_video.streams.first().download(dir)
        
    elif quality=="high":
        #pytube_video.streams.filter(progressive=True).get_highest_resolution().download(dir)
        pytube_video.streams.get_audio_only().download(dir)
        
    
    return source


    
def downloadedList(separator=">", dir=downloads_dir):
    videos = os.listdir(downloads_dir)
    videos = f"{separator} " + f"\n{separator} ".join(videos)  
    return videos


#--DEBUG--#
def __test():
    print(search("guaasrsa"))


if __name__ == "__main__":
    __test()