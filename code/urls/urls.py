import os
import json

class URLManager:  
    def __init__(self,directory, *args, **kwargs):
        """
        A Class made to access saved urls in json files
        
        directory:str= Path to the json files folder
        
        extra:list= List with additional json files paths 
        
        To do:
        change the self.urls so every time get method is called, it opens the json file and returns the url
        
        currently: loading all the json files into a dictionary (loaded in RAM)

        """
        
        self._urls = {}
        self._directory = directory
        self.setAllURL(*args, **kwargs)

    @property
    def directory(self)-> str:
        return self._directory
    
    @directory.setter
    def setDirectory(self, dir: str) -> None:
        if type(dir) != str:
            raise TypeError("Expected a String")         
        if not os.path.exists(dir):
            raise TypeError("Must be a folder path") 
        self._directory = dir
        
    @property
    def urls(self)-> str:
        return self._urls
   
    def setAllURL(self, extra: list=None, *args, **kwargs): 
        for file in os.listdir(self.directory):      
            if file.endswith(".json"):                                        
                with open(f"{self.directory}/{file}","r") as f:
                    type = file.replace(".json", "")
                    data = json.load(f)
                    self.urls[type] = data                                      
    
    def getAll(self) -> dict:
        return self.urls
    
    def get(self, type: str, name: str):
        """Returns an URL, needs the type and name of the file/api"""
        
        if type in self.urls and name in self.urls[type]:
            return self.urls[type][name]["url"]
        else: 
            return "Does not exist"
    
    def getAny(self, name: str) -> str:
        """Returns an URL from a name, returns the first one found"""
        
        for key, values in self.urls.items():
            if name in values:
                return self.urls[key][name]["url"]
        return "Not Found"  
    
    def getAllFromType(self, type: str):
        if type in self.urls:
            return self.urls[type]
        else: 
            return "Does not exist" 
    
    def types(self):
        return list(self.urls.keys())
          
    def orderFile(self, file: str):
        """Sorts a Json file. Paramethers:\n  
        file = filename"""
        
        with open(f"{self.directory}/{file}.json","r") as f:
            data = json.load(f)
        with open(f"{self.directory}/{file}.json","w") as f:    
            json.dump(data, f, indent=4)






def run(): 
    url = URLManager(directory=".")
    url.add("papa", "papa.cl", a="axd" )
    print(url.types())
    print(url.getAny("weather_clear"))
    
    
if __name__ == "__main__":
    run()
