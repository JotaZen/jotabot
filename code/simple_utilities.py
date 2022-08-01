#---------Functions---------#

def split(string, first=False):
    string = string.split()
    t = string.pop(0)
    if first: return t     
    return " ".join(string)

    
    
    
    
if __name__ == "__main__":
    pass