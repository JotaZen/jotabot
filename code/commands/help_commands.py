
class Help:

    description = str
    commands = list
    
    def __init__(self, description, commands):
        self.description = description
        self.commands = commands

    def get(self, separator = ">",):
        return f"{separator} {self.description}\n> "+ f"\n{separator} ".join(self.commands)

help_commands = Help(

    "**COMANDOS**",

    [
        "**-help -? -ayuda -h**",
        "-db - Comandos bases de datos",
        "yt - Busca un video de YouTube",
        "ytdwl - Descarga YT",
        "ytlist - Que hay descargado",
        "scramshot - Captura pantalla del servidor",
        "scramshow - Capturas guardadas",
        "scram - Muestra captura (indice de scramshow)",
        "-clear (numero) - borra la cantidad de mensajes (<6)",
        "venbot - Bot a voz",
        "salbot - Saca al bot de voz",
        "silksong - Todavia no sale",      
    ]
)

datab_commands = Help(

    "**COMANDOS DATABASES**",

    [
        "**-db**",
        "data - Muestra las bases de datos existentes",
        "sql (query) - Consulta SQL simple",
        "create database + (name) - Crea una base datos",
        "drop database + (name) - Borra una base datos (!!!)",
    ]

)




