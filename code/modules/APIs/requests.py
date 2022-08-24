
import re
from urllib import request

def booruImgs(api: str, tags: list =[], tag_separator: str = "&", limit= 100) -> list:
    """Gets latest booru pages images from an url, tags (like: "tags=something") with "&" as default separator"""
    for i in tags:
        api = f"{api}{tag_separator}{i}"
        
    index_content = request.urlopen(api) 
    search_results = re.findall("file_url=\"([^\"]*)", index_content.read().decode("utf-8"))
    
    if len(search_results) <= limit:
        limit = len(search_results)
    
    return search_results[0:limit]
    
