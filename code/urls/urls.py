import os
import json

"""
A Class made to access saved urls in json files
To do:
change the self.urls so every time get method is called, it opens the json file and returns the url

"""
class URLManager:  
    
    def __init__(self,directory, *args, **kwargs):
        """
        URLs -> directory='urls.json folder from python script'
        
        extra=list of extra json files with urls
        """
        self._urls = {}
        self._directory = directory
        self.setAllURL(*args, **kwargs)

    @property
    def directory(self)-> str:
        return self._directory
    
    @directory.setter
    def directory(self, dir: str) -> None:
        if type(dir) != str:
            raise "Must be a folder path"    
        self._directory = dir
    
    @property
    def urls(self) -> dict:
        return self._urls
    
    @urls.setter
    def urls(self, url: dict) -> None:
        if type(url) != dict:
            raise "Needs a Dictionary"    
        self._urls = dir
        
     
    def setAllURL(self, extra=False, *args, **kwargs): 
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
    
    
    def add(self, 
            name: str, 
            url: str,
            type: str="Uncategorized", 
            overwritte: bool=True,
            *args, **kwargs):
        
        file = f"{self.directory}/{type}.json"
        try:
            open(file, "x")
            with open(file, "w") as f:
                f.write("{}")          
        except:
            pass
        
        new = {"url": url}
        new.update(kwargs)
        
        with open(file,"r") as f:    
            data = json.load(f)

        if not overwritte:
            while name in data.keys() and not overwritte:
                name = f"{name} copy"
             
            data.update({name:new})
                            
        if overwritte and name in data.keys():                
            data[name] = new 
        
        with open(file,"w") as f:    
            json.dump(data, f, indent=4)
  
    
    def updateURL(self, type, name):pass
    
          
    def orderFile(self, file: str):
        """Para ordenar un json. Parametros:\n  
        file = archivo.json"""
        
        with open(f"{self.directory}/{file}","r") as f:
            data = json.load(f)
        with open(f"{self.directory}/{file}","w") as f:    
            json.dump(data, f, indent=4)



def run(): 
    url = URLManager(directory=".")
    url.add("papa", "papa.cl", a="axd" )
    print(url.types())
    print(url.getAny("weather_clear"))
    
    
if __name__ == "__main__":
    run()
