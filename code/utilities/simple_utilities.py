from datetime import datetime


#---------Functions---------#

def fileNameChars(filename: str, OS="Windows", add: str=",.\'") -> str: 
    """
    Removes prohibited characters in Windows(default)/Linux file names 
    
    -Use "add": str argument to append characters that you don't want in your file name
    
    Windows restricted = <>:"/\|?*,.' 
    
    """
    restricted = ""   
    
    if OS == "Windows":
        restricted += '<>:"/\\|?*'
    elif OS == "Linux":
        restricted += '\\'     
    else: raise 'Not An OS'
      
    for i in (restricted + add):
        filename = filename.replace(i,"")   
    
    return filename


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