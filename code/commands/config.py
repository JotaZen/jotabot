
import json

class Config:
    
    def __init__(self, settings: dict) -> None:
        self.settings = settings
    
    def cfg(self, key):
        if key in self.settings:
            return self.settings[key]
        else:
            raise "Setting not found"
           
        
screenshot_settings = Config(
    {
        "directory" : "../files/ss",
        "screenshot_limit": 1,
    }    
)

yTube_settings = Config(
    {
        "directory" : "../files/ytDownloads",
    }    
)


