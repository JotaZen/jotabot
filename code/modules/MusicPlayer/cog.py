import nextcord
import nextcord.utils
from nextcord.ext import commands
from nextcord.utils import get

from modules.Help.cog import HelpCommands
import modules.yTube.yTube as yt
import asyncio
import json
import threading
class MusicPlayer(commands.Cog, name="Music Player"):
    """Music"""
    
    def __init__(self, bot, CONFIGS, **kwargs):
        self._bot            = bot
        self._song_queue     = {i : [] for i in bot.guilds}   # {'guild': [{'url':str, 'path':'./'},]}
        self._past_songs     = {}
        self.estatus         = 'Active' 
        self.dir             = CONFIGS.get(self.__cog_name__, 'downloads_path')
        self.permissions     = None #Dict with clients and permisses / whitelist
        self.inactive_time   = None #timeout
        HelpCommands.AddCommands(self.get_commands())
        
    @property
    def bot(self):
        return self._bot
       
    @property
    def song_queue(self):
        return self._song_queue
    
    @property
    def past_songs(self):
        return self._past_songs
    
    def clearQueue(self, guild):
        if guild in self.song_queue:
            self._song_queue[guild] = []
            
    def addSongToQueue(self, guild, url, path, title=None):
        if guild in self.song_queue:      
            self._song_queue[guild].append(
                {
                    'title' : title,
                    'url'   : url,
                    'path'  : path              
                }
            )
            
    def addSongToPast(self, guild, song): #Not working
        if guild in self.song_queue:      
            self.past_songs[guild].append(song)

    def removeSongFromQueue(self, guild, title=None, url=None, path=None):
        if guild in self.song_queue:
            
            for i in self._song_queue[guild]:
                if url == i['url'] or path == i['path'] or title == i['title']:
                    
                    self._song_queue[guild].remove(i)

    async def voiceConnect(self, ctx): pass
        
                       
    @commands.command(aliases=["-p"])
    async def __play(self, ctx, *, search):             
        """-p - Reproduce una canción de YouTube o la pone a la cola"""

        try:
            channel = ctx.message.author.voice.channel          
        except:     
            await ctx.send("No estas en un canal de voz ~")
            return
            
        voice = get(self.bot.voice_clients, guild = ctx.guild)
        if not voice: 
            await channel.connect() 
            voice = get(self.bot.voice_clients, guild = ctx.guild)           
                
        
        yt_links = yt.search(search, cant=2)
             
        #expresion regular para poner opcion1-N
        if 'opcion2' in ctx.message.content.split():
            song_yt_link = yt_links[1]
        else:
            song_yt_link = yt_links[0]
        
        song_path = yt.downloadAudioYT(source=song_yt_link, dir=self.dir)
        video_title = yt.source(song_yt_link).title 
       
        if voice.is_playing() and self.song_queue[ctx.guild] == []:
            voice.stop()    
            
        self.addSongToQueue(ctx.guild, song_yt_link, song_path, video_title)       
        
        if voice.is_playing() and len(self.song_queue[ctx.guild]) > 1:
            await ctx.send(f'> Song queued -> {video_title}') 
            return
        
        if not voice.is_playing():
            current_song = self.song_queue[ctx.guild][0]['path']
            
            music_thread = threading.Thread(target= lambda:    
                voice.play(
                    nextcord.FFmpegPCMAudio(source=current_song),
                    after=lambda e: self.nextSong(ctx, song_yt_link, voice)
                    )
                )    
            music_thread.run()
            
            print(f"Playing {self.song_queue[ctx.guild][0]['title']}")
            voice.pause()
            await asyncio.sleep(2)
            voice.resume()
            
            await ctx.send(f"> Playing: {self.song_queue[ctx.guild][0]['url']}")


        
    async def nextSong(self, ctx, link, voice):
        if len(self.song_queue[ctx.guild]) > 1:
            past_song = self.song_queue[ctx.guild].pop(0)    
            
            current_song = self.song_queue[ctx.guild][0]['path']     
            link = self.song_queue[ctx.guild][0]['url']    
             
            music_thread = threading.Thread(target= lambda:    
                voice.play(
                    nextcord.FFmpegPCMAudio(source=current_song),
                    after=lambda e: self.nextSong(ctx, link, voice)
                    ) 
                )
            music_thread.run()
            
            voice.pause()
            await asyncio.sleep(2)
            voice.resume()
            
            await ctx.send(f"> Playing: {link}")     
    

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
        if len(self.song_queue[ctx.guild]) <= 1:
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
        
        if self.song_queue[ctx.guild] == []: 
            await ctx.send("> No hay canciones en la playlist")
            return
        
        temp = []
        for song in self.song_queue[ctx.guild]:
            temp.append(song['title'])
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
        
        
def setup(bot, **kwargs):
    bot.add_cog(MusicPlayer(bot, **kwargs))