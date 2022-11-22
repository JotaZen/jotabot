import configparser
import os

class JotabotConfig(configparser.ConfigParser):
    
    def __init__(self, config_file:str, default_configs:str,*args, **kwargs):
        """_summary_

        Args:
            config_file (str): must be in the same main file's directory
            default_configs (str): _description_
        """
        super().__init__(*args, **kwargs)
        self.config_file = config_file
        self.default_configs = default_configs     
       
        if not os.path.exists(f'{self.config_file}'):       
            with open(config_file, "x") as cfg:
                with open(self.default_configs, 'r') as dft:
                    cfg.write(dft.read())              
             
        self.read(self.config_file)  
          
    def resetAllToDefault(self):
        self.read(self.default_configs) 
        with open(self.config_file, 'w') as configfile:
            self.write(configfile) 

    def getItems(self, section):  
        return {i:j for i,j in self.items(section)}
    
    def getAllConfigs(self):
        return {i : self.getItems(i) for i in self.sections()}
    
    def addSections(self, new_sections:list, data:bool= False, keys:list=['key'], values:list=['values']):
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






