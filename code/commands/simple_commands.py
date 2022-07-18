
class Responses:
    commands_responses = dict

    def __init__(self, commands_responses):
        self.commands_responses = commands_responses
    
    def commands(self):
        commands = []
        for key in self.commands_responses: commands.append(key)
        else: return commands

Memes = Responses(
    {
    "uwu":"uwu",
    "xdd":"(๑╹ᆺ╹)",
    "hola":"uwu",
    "awa":"awita",
    "jota":"jota ql",
    "jotabot":"**Bot multiuso hecho al lote**",
    "github":"**https://github.com/JotaZen/jotabot**"
    }
)



def plainText(command):
    return Memes.commands_responses.get(command, "")