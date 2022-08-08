class Help:
   
    all_instances = []
   
    def __init__(self, name: str, command: str, aliases: list, title: str, description: str, commands: list) -> None:  
        self.name        = name
        self.command     = command
        self.aliases     = aliases
        self.title       = title
        self.description = description
        self.commands    =  [          
            {    
            "command" : i[0],
            "description" : i[1],
            "type" : i[2],
            "aliases"  : i[3]
            }       
        for i in commands
        ]        
        
        self.all_instances.append(self)
 
 
    def __str__(self) -> str:
        return self.name

    def getName(self)          : return self.name      
    def getCommand(self)       : return self.command
    def getAlias(self)         : return self.aliases
    def getTitle(self)         : return self.title   
    def getDescript(self)      : return self.description 
             
    def getCommandList(self, description = False, aliases = False):
        if description == False:
            return [i["command"] for i in self.commands]

        elif description == True:
            return [f'{i["command"]} - {i["description"]}' for i in self.commands] 
 
    
    """DISCORD"""
    
    def getInstances(self, name = False):
        if name == False: return self.all_instances
        else:
            instances_names = []
            for i in self.all_instances:
                instances_names.append(i.name)
            return instances_names
        
    def getListStr(self, separator = ">",):
        return (f"{separator} {self.title}\n> " + 
                f"\n{separator} ".join(self.getCommandList(description = True)))
    



""" COMMAND TYPES: SQL, SS, YT, MAIN, GIT """


help_commands = Help(

    #--- NAME ---#
    "Help",   
    #--- COMMAND ---#
    "-help",    
    #--- ALIASES ---#                                
    ["-ahelp", "-ayuda", "-h"],      
    #--- TITLE ---#
    "**COMANDOS**",
    #--- DESCRIPTION ---#
    "Comandos generales",

    #--- ["COMMAND", "DESCRIPTION", "TYPE", ["ALIASES"]] ---#
    [
        ["-db", "Comandos bases de datos", "SQL",[]],
        ["-yt", "Comandos YouTube", "YT",[]],
        ["-ss", "Comandos Screenshot", "YT",[]],
        ["-pend", "Cosas por hacer", "YT",[]],

        ["-clear", "borra la cantidad de mensajes indicada(<6)", "MAIN",[]],
        ["venbot", "Bot a voz", "DISCORD",[]],
        ["salbot", "Saca al bot de voz", "DISCORD",[]],
        ["silksong", "Todavia no sale", "DISCORD",[]],      
    
    ]
)


database_commands = Help(

    #--- NAME ---#
    "SQL",   
    #--- COMMAND ---#
    "-db",    
    #--- ALIASES ---#                                
    ["-database"],      
    #--- TITLE ---#
    "**COMANDOS BASES DE DATOS**",
    #--- DESCRIPTION ---#
    "Comandos SQL",

    #--- ["COMMAND", "DESCRIPTION", "TYPE", ["ALIASES"]] ---#
    [
        ["data", "Muestra las bases de datos existentes", "SQL",[]],
        ["sql", "Consulta SQL simple", "SQL",[]],
        ["create database", "Crea una base datos", "SQL",[]],
        ["drop database", "Borra una base datos", "SQL",[]], 
    
    ]
)


yTube_commands = Help(

    #--- NAME ---#
    "YouTube", 
    #--- COMMAND ---#
    "-yt",    
    #--- ALIASES ---#                                
    ["-youtube"],      
    #--- TITLE ---#
    "**COMANDOS YouTube**",
    #--- DESCRIPTION ---#
    "Comandos de videos Youtube",

    #--- ["COMMAND", "DESCRIPTION", "TYPE", ["ALIASES"]] ---#
    [
        ["yt", "Busca un video de YouTube", "YT",[]],
        ["ytdwl", "Descarga YT", "YT",[]],
        ["ytlist", "Que hay descargado", "YT",[]],    
    ]
)


screenshot_commands = Help(

    #--- NAME ---#
    "Screenshot", 
    #--- COMMAND ---#
    "-ss",    
    #--- ALIASES ---#                                
    ["-sshelp"],      
    #--- TITLE ---#
    "**COMANDOS SCREENSHOT**",
    #--- DESCRIPTION ---#
    "Comandos generales",

    #--- ["COMMAND", "DESCRIPTION", "TYPE", ["ALIASES"]] ---#
    [
        ["scramshot", "Captura pantalla del servidor", "SS",[]],
        ["scramshow", "Capturas guardadas", "SS",[]],
        ["scram", "Muestra captura (indice de scramshow)", "SS",[]],       
    ]
)

to_doList = Help(

    #--- NAME ---#
    "Pendiente",   
    #--- COMMAND ---#
    "-pend",    
    #--- ALIASES ---#                                
    [],      
    #--- TITLE ---#
    "**POR HACER**",
    #--- DESCRIPTION ---#
    "Comandos pendientes",

    #--- ["COMMAND", "DESCRIPTION", "TYPE", ["ALIASES"]] ---#
    [
        ["Conversor moneda", "https://api.gael.cloud/general/public/monedas", "",[]],
        ["Ver Clima", "https://www.meteored.cl/api/#/panel/ayuda", "",[]],

    
    ]
)

def helpCommands():
    commands = []
    for i in help_commands.getInstances():
        commands.append(i.getCommand())
        for j in i.getAlias():
            commands.append(j)
    return commands
        
def helpPicker(message):
    for i in help_commands.getInstances():
        if message in i.getAlias() or message == i.getCommand():
            return i
    else: return "Error"

#########################################################################################
def run():
    pass




    
if __name__ == "__main__":
    run()



