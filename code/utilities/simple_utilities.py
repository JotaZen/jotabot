#---------Functions---------#

def splitWord(string, splitter=" ", first=False):
    string = string.split(splitter)
    t = string.pop(0)
    if first: return t     
    return " ".join(string)


def fileNameChars(filename: str, OS="Windows", add: str="") -> str: 
    """
    Removes characters prohibited in Windows(default)/Linux file names 
    
    -Use "add" argument to append characters that you don't want in your file name
    
    """
    restricted = str   
    
    if OS == "Windows":
        restricted = '<>:"/\\|?*,.\''
    
    elif OS == "Linux":
        restricted = '\\'
        
    else: raise 'Not An OS'
     
    for i in (restricted + add):
        filename = filename.replace(i,"")   
    return filename


    
    
if __name__ == "__main__":
    print(fileNameChars(",.,.xd", add=" x"))