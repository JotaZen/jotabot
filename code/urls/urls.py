class URL:
    
    def __init__(self, urls:dict):
        self.urls = urls
        
    def get(self, name):
        return self.urls[name]
    
