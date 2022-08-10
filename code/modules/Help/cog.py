from nextcord.ext import commands

class Help(commands.Cog, name="Help Commands"):
    
    def __init__(self, bot):
        self.bot = bot





def setup(bot: commands.Bot):
    bot.add_cog(Help(bot))