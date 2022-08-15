from nextcord.ext import commands
import modules.yTube.yTube as yt
from modules.Help.cog import HelpCommands

import asyncio
class yTube(commands.Cog, name="yTube"):
    """YouTube Commands"""
    
    def __init__(self, bot):
        self.bot = bot
        HelpCommands.AddCommands(self.get_commands())
    
    @commands.command(aliases=["yt"])
    async def __yt(self, ctx, *, source): 
        """yt - Busca un video en YouTube"""
        await ctx.send(yt.search(source))
    
    @commands.command(aliases=["ytlist"])
    async def __ytlist(self, ctx):  
        """ytlist - Lista de videos descargados"""  
        await ctx.send(yt.downloadedList())
    
    @commands.command(aliases=["ytdwl"])
    async def __ytdwl(self, ctx, *, source):   
        """ytdwl - Descarga un video de YouTube"""
        v = yt.downloadVideo(yt.search(source))
        await ctx.send(f"Se descargó: {v}") 
                

def setup(bot: commands.Bot):
    bot.add_cog(yTube(bot))