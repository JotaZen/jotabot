from nextcord.ext import commands
import modules.yTube.yTube as yt
from modules.Help.cog import HelpCommands
class yTube(commands.Cog, name="YouTube"):
    """YouTube Commands"""
    
    def __init__(self, bot, CONFIGS, **kwargs):
        self.bot = bot  
        self.downloads_dir = CONFIGS.get(self.__cog_name__, 'downloads_path')
        self.audio_size_limit_mb = CONFIGS.get(self.__cog_name__, 'audio_size_limit_mb')
        HelpCommands.AddCommands(self.get_commands())
    
    @commands.command(aliases=["yt"])
    async def __yt(self, ctx, *, source): 
        """yt - Busca un video en YouTube"""
        await ctx.send(yt.search(source))
    
    @commands.command(aliases=["ytlist"])
    async def __ytlist(self, ctx):  
        """ytlist - Lista de videos descargados"""  
        await ctx.send(yt.downloadedList(self.downloads_dir))
    
    @commands.command(aliases=["ytdwl"])
    async def __ytdwl(self, ctx, *, source):   
        """ytdwl - Descarga un video de YouTube"""
        video = yt.search(source)[0]
        yt.downloadVideo(video, self.downloads_dir)
        await ctx.send(f"Se descargó: {video}") 
                

def setup(bot, **kwargs):
    bot.add_cog(yTube(bot, **kwargs))