from nextcord.ext import commands
class Help:
    def  __init__(self, commands):
        self.allCommands = commands
        
    def AddCommands(self, commands):
        self.allCommands.extend(commands)
    
HelpCommands = Help([])
class HelpCog(commands.Cog, name="Help Commands"):
    
    def __init__(self, bot):
        self.bot = bot
        HelpCommands.AddCommands(self.get_commands())

    @commands.command(aliases=["-h"])
    async def __help(self, ctx):
        await ctx.send("> " + "\n> ".join([" ,".join(i.aliases) for i in HelpCommands.allCommands]))
    
def setup(bot, **kwargs):
    bot.add_cog(HelpCog(bot, **kwargs))