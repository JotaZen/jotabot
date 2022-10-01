import json
from datetime import datetime
from pathlib import Path

#---------Functions---------#

getParent = lambda x: Path(x).absolute().parent

def fileNameChars(filename: str, OS="W", add: str=",.\'") -> str: 
    """
    Removes prohibited characters in Windows(default)/Linux file names 
    
    -Use "add": str argument to append characters that you don't want in your file name
    -OS=['W','L']
    Windows restricted = <>:"/\|?*,.' 
    
    """
    restricted = ""   
    
    if OS == "W":
        restricted += '<>:"/\\|?*'
    elif OS == "L":
        restricted += '\\'     
    else: raise 'Not An OS'
      
    for i in (restricted + add):
        filename = filename.replace(i,"")   
    
    return filename
          
def orderJson(file: str):
    """Para ordenar un json. Parametros:\n  
    file = archivo.json"""
    
    with open(file,"r") as f:
        data = json.load(f)
    with open(file,"w") as f:    
        json.dump(data, f, indent=4)

#---------Decorators---------#
def executionTime(func):
    def wrapper():
        initial_time = datetime.now()
        func()
        final_time = datetime.now()
        time_elapsed = final_time - initial_time
        print(f"Finshed in {time_elapsed.total_seconds()} seconds.")
    return wrapper
    

 

      
    
    
    
    
    
    
    
    
if __name__ == "__main__":
    print(fileNameChars(",.,.xd", add=" x"))