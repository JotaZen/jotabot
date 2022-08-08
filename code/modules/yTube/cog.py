from nextcord.ext import commands
import modules.yTube.yTube as yt

class yTube(commands.Cog, name="yTubexd"):
    """YouTube Commands"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def yt(self, ctx, *, source): 
        await ctx.send(yt.search(source))
    
    @commands.command()
    async def ytlist(self, ctx):    
        await ctx.send(yt.downloadedList())
    
    @commands.command()
    async def ytdwl(self, ctx, *, source):   
        v = yt.download(yt.search(source))
        await ctx.send(f"Se descargó: {v}")
        

def setup(bot: commands.Bot):
    bot.add_cog(yTube(bot))