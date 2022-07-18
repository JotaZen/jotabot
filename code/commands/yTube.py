import pytube
from urllib import parse, request
import re
import os

downloads_dir = "..\..\files\ytDownloads"

def ytSearch(search, console = False, index = 0):
    query_string = parse.urlencode({"search_query": search})
    html_content = request.urlopen("https://www.youtube.com/results?" + query_string)
    search_results = re.findall("watch\?v=(.{11})", html_content.read().decode("utf-8"))
    if console == True: print(search_results)
    return f"https://www.youtube.com/watch\?v={search_results[index]}" 

def ytDownload(search, console = False, index = 0, dir = downloads_dir):
    link_yt = pytube.YouTube(ytSearch(search, console, index))
    link_yt.streams.first().download(dir)

def dwList(separator):
    videos = os.listdir("../files/ytDownloads")
    videos = f"{separator} " + f"\n{separator} ".join(videos)  
    return videos




#--DEBUG--#
def test():
    print(ytSearch("guaasrsa"))


if __name__ == "__main__":
    test()