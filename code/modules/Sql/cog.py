from nextcord.ext import commands

from modules.Help.cog import HelpCommands

class SQL(commands.Cog, name="SQL"):
    
    def __init__(self, bot):
        self.bot = bot
        HelpCommands.AddCommands(self.get_commands())

def setup(bot, **kwargs):
    bot.add_cog(SQL(bot))