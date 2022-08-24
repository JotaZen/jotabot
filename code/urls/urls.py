import os
import json

main_directory = "./urls"
class URLManager:  
    
    def __init__(self,directory: str=main_directory):
        """URLs -> directory='urls.json folder from python script'"""
        self.urls = {}
        self.directory = directory
        self.setAllURLS()

     
    def setAllURLS(self): 
        for file in os.listdir(self.directory):      
            if file.endswith(".json"):                                        
                with open(f"{self.directory}/{file}","r") as f:
                    type = file.replace(".json", "")
                    data = json.load(f)
                    self.urls[type] = data
                                
    
    def getAll(self):
        return self.urls
    
    
    def get(self, type: str, name: str):
        """Returns an URL, needs the type and name of the file/api"""
        
        if type in self.urls and name in self.urls[type]:
            return self.urls[type][name]["url"]
        else: 
            return "Does not exist"
            
            
    def orderFile(self, file: str):
        """Para ordenar un json. Parametros:\n  
        file = directorio/archivo \n
        data = diccionario con data"""
        
        with open(f"{self.directory}/{file}","r") as f:
            data = json.load(f)
        with open(f"{self.directory}/{file}","w") as f:    
            json.dump(data, f, indent=4)


URL = URLManager()


def run(): 

    url = URLManager(directory=".")
    url.setAllURLS()

    print(url.get("API","Gael Monedas API"))
    
    
if __name__ == "__main__":
    run()