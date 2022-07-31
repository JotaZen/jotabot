#---------Functions---------#

def wordDetector(sentence: str, detect: str) -> bool:
    words_in_a = sentence.split()
    if detect in words_in_a:
        return True
    else:
        return False

def split(string, first=False):
    string = string.split()
    t = string.pop(0)
    if first:
        return t
    return " ".join(string)

    
if __name__ == "__main__":
    pass