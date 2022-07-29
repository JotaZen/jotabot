
class Help:
   
    all_instances = []

    def __init__(self, name, command, aliases, title, description, commands):  
        self.name        = name
        self.command     = command
        self.aliases     = aliases
        self.title       = title
        self.description = description
        self.commands    =  [
        {    
            "name" : i[0],
            "description" : i[1],
            "type" : i[2],
            "aliases"  : i[3]
        }       
        for i in commands
        ]
    
    def getCommands(self, description = False, aliases = False):
        if description == False:
            return [i["name"] for i in self.commands]

        elif description == True:
            return [f'{i["name"]} - {i["description"]}' for i in self.commands]

    def getListStr(self, separator = ">",):
        return (f"{separator} {self.title}\n> " + 
                f"\n{separator} ".join(self.getCommands(description = True))) 

    def getAllCommands(self):
        all_commands = []
        for i in self.all_instances:
            all_commands.append(i.getCommand())
            for j in i.getAlias():
                all_commands.append(j)
        return all_commands

    def getInstances(self, name = False):
        if name == False: return self.all_instances
        else:
            instances_names = []
            for i in self.all_instances:
                instances_names.append(i.name)
            return instances_names
   
    getAlias     = lambda self: self.aliases

    getCommand   = lambda self: self.command

    addInstance  = lambda self, instance: self.all_instances.append(instance)

""" COMMAND TYPES: SQL, SS, YT, MAIN, GIT """

"""
NOTA: PONER UN PARAMETRO ADICIONAL PARA CUANDO SE ENVIA TEXTO PLANO O UN ARCHIVO 
PARA ENVIAR EN DISCORD
"""

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
        ["yt", "Busca un video de YouTube", "YT",[]],
        ["ytdwl", "Descarga YT", "YT",[]],
        ["ytlist", "Que hay descargado", "YT",[]],
        ["scramshot", "Captura pantalla del servidor", "SS",[]],
        ["scramshow", "Capturas guardadas", "SS",[]],
        ["scram", "Muestra captura (indice de scramshow)", "SS",[]],
        ["-clear", "borra la cantidad de mensajes indicada(<6)", "MAIN",[]],
        ["venbot", "Bot a voz", "DISCORD",[]],
        ["salbot", "Saca al bot de voz", "DISCORD",[]],
        ["silksong", "Todavia no sale", "DISCORD",[]],      
    
    ]
)
help_commands.addInstance(help_commands)

databse_commands = Help(

    #--- NAME ---#
    "SQL",   
    #--- COMMAND ---#
    "-db",    
    #--- ALIASES ---#                                
    ["-database", "sql"],      
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
databse_commands.addInstance(databse_commands)

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
yTube_commands.addInstance(yTube_commands)

screenshot_commands = Help(

    #--- NAME ---#
    "Screenshot", 
    #--- COMMAND ---#
    "-help ss ",    
    #--- ALIASES ---#                                
    ["-ss"],      
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
screenshot_commands.addInstance(screenshot_commands)

def helpPicker(message):
    for i in help_commands.getInstances():
        if message in i.getAlias() or message == i.getCommand():
            return i
    else: return "Error"

#########################################################################################
def run():
    print(screenshot_commands.getInstances(name = True))
    print("All Right")

if __name__ == "__main__":
    run()



