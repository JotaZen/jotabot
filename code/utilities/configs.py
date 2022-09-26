import configparser

class JotabotConfig(configparser.ConfigParser):
    
    def __init__(self, config_file, deafault_file,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config_file = config_file
        self.deafault_file = deafault_file
        self.read(self.config_file)  
          
    def resetAllToDefault(self):
        self.read(self.deafault_file) 
        with open(self.config_file, 'w') as configfile:
            self.write(configfile) 

    def getItems(self, section):  
        return {i:j for i,j in self.items(section)}
    
    def getAllConfigs(self):
        return { i : self.getItems(i) for i in self.sections()}
    
    def addSections(self, new_sections: list, data: bool= False, keys: list=['key'], values: list=['values']):
        for n in new_sections:
            if n not in self.sections():
                self[n] = {}
                if data == True:
                    for key, value in zip(keys,values):
                        self[n][key] = value  
        with open(self.config_file, 'w') as configfile:
            self.write(configfile)
        
    
    

if __name__ == '__main__':
    config = JotabotConfig()
    print(config.addSections(['Papa']))






