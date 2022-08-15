import nextcord
from nextcord.ext import commands
from nextcord.utils import get

from modules.Help.cog import HelpCommands
import modules.yTube.yTube as yt
import asyncio

class MusicPlayer(commands.Cog, name="Music Player"):
    """Music"""
    
    def __init__(self, bot):
        self.bot = bot
        self.song_queue = []       
        self.dir = "./modules/MusicPlayer/temp"
        HelpCommands.AddCommands(self.get_commands())
                           
                       
    @commands.command(aliases=["-p"])
    async def __play(self, ctx, *, search):             
        """-p - Reproduce una canción de YouTube o la pone a la cola"""
        
        channel = ctx.message.author.voice.channel
        if not channel:
            await ctx.send("No estas en un canal de voz ~")
            return
       
        voice = get(self.bot.voice_clients, guild = ctx.guild)
        if not voice: 
            await channel.connect() 
            voice = get(self.bot.voice_clients, guild = ctx.guild)           
                
        song_yt_link = yt.search(search)
        yt.download(source=song_yt_link, dir=self.dir)
        
        video_title = yt.source(song_yt_link).title      
        for i in '!<>/\\:?|*,.\'"':
            video_title = video_title.replace(i,"")
        
        self.song_queue.append(video_title)
        
        if not voice.is_playing():
            
            song = f"{self.dir}/{self.song_queue[0]}.mp4"
                        
            voice.play(nextcord.FFmpegPCMAudio(source=song),after=lambda e: self.nextSong(ctx, song_yt_link))
            print(f"Playing {self.song_queue[0]}")
            voice.pause()
            await asyncio.sleep(2)
            voice.resume()
            await ctx.send(f"> Playing: {song_yt_link}")
        else:
            await ctx.send('Song queued') 
        
    async def nextSong(self, ctx, link):
        if len(self.song_queue) > 0:
            voice = get(self.bot.voice_clients, guild = ctx.guild) 
            
            self.song_queue.pop(0)    
            song = f"{self.dir}/{self.song_queue[0]}.mp4"
            
            link = yt.search(self.song_queue[0])            
            voice.play(nextcord.FFmpegPCMAudio(source=song),after=lambda e: self.nextSong(ctx, link))
            voice.pause()
            await asyncio.sleep(2)
            voice.resume()
            
            await ctx.send(f"> Playing: {yt.search(link)}")     
    

    @commands.command(aliases=["-pause", "-play"])
    async def __pause(self, ctx): 
        """-pause - Pausa"""
        try:    
            voice = get(self.bot.voice_clients, guild = ctx.guild)
            
            if voice.is_playing():
                voice.pause()
            else:
                voice.resume()
        except:
            print("Disconnected")

    
    @commands.command(aliases=["-next","-n"])
    async def __next(self, ctx):    
        """-n - Reproduce la siguiente canción en la cola"""
        if len(self.song_queue) == 0:
            await ctx.send(f"> No hay mas")
            return
        
        voice = get(self.bot.voice_clients, guild = ctx.guild)
        voice.stop()

        
    @commands.command(aliases=["-quit"])    
    async def __quit(self, ctx):    
        """-quit - Borra toda la playlist"""
        try: 
            voice = get(self.bot.voice_clients, guild = ctx.guild)
            voice.stop()
            self.song_queue = [] 
            await voice.disconnect() 
            await ctx.send("> Se limpio la playlist") 
        except:
            print("Disconnected")


    @commands.command(aliases=["-playlist"])
    async def __playlist(self, ctx):  
        """-playlist - Muestra la Playlist"""      
        if self.song_queue == []: 
            await ctx.send("> No hay canciones en la playlist")
            return
        
        temp = []
        for song in self.song_queue:
            temp.append(song)
        await ctx.send("> Playlist:\n> Actual: " + "\n> ".join(temp))
  
    
    @commands.command(aliases=["-force"])
    async def __playforce(self, ctx, *, search):      
        """-force - Fuerza una canción en la cola para que se reproduzca a continuación"""
        if len(self.song_queue) <= 2: return
        """Checks if User is connected to voice"""
        channel = ctx.message.author.voice.channel
        if not channel:
            await ctx.send("No estas en un canal de voz ~")
            return
       
        voice = get(self.bot.voice_clients, guild = ctx.guild)
        if not voice: 
            await channel.connect() 
            voice = get(self.bot.voice_clients, guild = ctx.guild)           
                
        song_yt_link = yt.search(search)
        yt.download(source=song_yt_link, dir=self.dir)
        
        video_title = yt.source(song_yt_link).title      
        for i in '!<>/\\:?|*."':
            video_title = video_title.replace(i,"")
        
        self.song_queue.insert(1, video_title)
        await ctx.send(f"> Se forzo: {song_yt_link}")
    
    
    @commands.command(aliases=["-testp"])
    async def __testplay(self, ctx, *, search):  
        """-testp - Pruebas"""
        channel = ctx.message.author.voice.channel
        if not channel:
            await ctx.send("No estas en un canal de voz ~")
            return
       
        voice = get(self.bot.voice_clients, guild = ctx.guild)
        if not voice: 
            await channel.connect() 
            voice = get(self.bot.voice_clients, guild = ctx.guild)
            
        song = f"../files/ytDownloads/{search}"
        voice.play(nextcord.FFmpegPCMAudio(source=song))    
        voice.pause()
        await asyncio.sleep(2)
        voice.resume()
        
def setup(bot: commands.Bot):
    bot.add_cog(MusicPlayer(bot))