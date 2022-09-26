import json
from pathlib import Path

class Response:
    
    def __init__(self, file):
        self._jsonfile = file
    
    @property
    def jsonfile(self):
        return self._jsonfile
    
    @jsonfile.setter
    def setDir(self, dir):
        self._jsonfile = dir
        
    def loadJSON(self):
        with open(self.jsonfile, 'r') as f:
            return json.load(f)
            
    def getCommands(self):
        return list(self.loadJSON().keys())
    
    def response(self, command):
        responses = self.loadJSON()
        if command in responses:
            return responses[command]
    
    def orderFile(self):
        """Para ordenar un json.""" 
        data = self.loadJSON()
        with open(self.jsonfile,"w") as f:    
            json.dump(data, f, indent=4)
    
    def addResponse(self, command, response):
        data = self.loadJSON()
        if command in data or type(command) != str or type(response) != str:
            raise
        data[command] = response
        with open(self.jsonfile,"w") as f:    
            json.dump(data, f, indent=4)

SimpleResponse = Response('./modules/Commands1/responses.json') 

if __name__=='__main__':
    n = './modules/Commands1/responses.json'
    a = Response(n)
    a.addResponse('papa', 'papa')
    print(a.orderFile())