from nextcord.ext import commands

class SQL(commands.Cog, name="SQL"):
    
    def __init__(self, bot):
        self.bot = bot

def setup(bot: commands.Bot):
    bot.add_cog(SQL(bot))