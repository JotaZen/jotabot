
import re
from urllib import request
import requests
import random

def booruImgs(api: str, tags: list =[], tag_separator: str = "&", limit= 100) -> list:
    """Gets latest booru pages images from an url, tags (like: "tags=something") with "&" as default separator"""
    
    for i in tags:
        api += f"{tag_separator}{i}" # Modulo request puede hacer autom. esto
        
    index_content = request.urlopen(api) 
    search_results = re.findall("file_url=\"([^\"]*)", index_content.read().decode("utf-8"))
    
    if len(search_results) <= limit:
        limit = len(search_results)
    
    return search_results[0:limit]

def pokeAPI(api):
    content = requests.get(api)
    content = content.json()

def pokeRandom(api):
    content = requests.get(api)
    content = content.json()
    count = content["count"]

    i = random.randrange(count)
    url_pkmn = content["results"][i]["url"]
    pkmn = requests.get(url_pkmn)
    pkmn = pkmn.json()
    return pkmn

