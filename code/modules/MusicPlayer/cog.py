import nextcord
import nextcord.utils
from nextcord.ext import commands
from nextcord.utils import get

from modules.Help.cog import HelpCommands
import modules.yTube.yTube as yt
import asyncio
import random
import json
import threading
class MusicPlayer(commands.Cog, name="Music Player"):
    """Music"""
    
    def __init__(self, bot, CONFIGS, **kwargs):
        self._bot            = bot
        self.playlist        = CONFIGS.get(self.__cog_name__, 'playlist_path')
        self.dir             = CONFIGS.get(self.__cog_name__, 'downloads_path')
        self.max_audio_size  = int(CONFIGS.get(self.__cog_name__, 'audio_size_limit_mb'))
        self.change_status_to_all_playlists(False)
        self.permissions     = None #Dict with clients and permisses / whitelist
        self.inactive_time   = None #timeout
        HelpCommands.AddCommands(self.get_commands())
    
    @property        
    def bot(self): return self._bot
    
    #################################################
    #                  PLAYLIST                     #                                       
    #                                               #
    #################################################   
    
    def read_json_file(self):                           #care with the recursion
        try: 
            with open(self.playlist, 'r') as f:
                return json.load(f)  
        except:     
            with open(self.playlist, 'w') as f:
                f.write('{}')     
            self.read_json_file()  
    
    def write_json_file(self,  DATA):
        with open(self.playlist, 'w') as f:
            json.dump(DATA, f, indent=4)
        
    def get_playlist(self, guild: str, guild_only: bool=False) -> dict: 
        playlist = self.read_json_file()
        if not guild in playlist:
            playlist.update(
                {  
                    guild : {
                        "active": False,
                        "settings": {
                                "shuffle": False
                            },
                        "current": {},
                        "queue" : [],
                        "previous" : []
                    }
                }
            )
            self.write_json_file(playlist)          
                    
#        if guild_only: return playlist[guild]     
        return playlist if not guild_only else playlist[guild] 

    def get_status(self, guild):
        playlist = self.get_playlist(guild, guild_only=True)
        if not guild in playlist:
            playlist.update(
                {  
                    guild : {
                        "active": False,
                        "settings": {
                                "shuffle": False
                            },
                        "current": {},
                        "queue" : [],
                        "previous" : []
                    }
                }
            )
        return playlist[guild]['active']
    
    def set_status(self, guild, status):
        playlist = self.get_playlist(guild)
        playlist[guild]['active'] = status
        self.write_json_file(playlist)

    def change_status_to_all_playlists(self, status):
        playlist = self.read_json_file()
        for i in playlist:
            playlist[i]['active'] = status
        self.write_json_file(playlist)  
         
    def get_current_song(self, guild): 
        playlist = self.get_playlist(guild, guild_only=True)
        return playlist['current']
    
    def set_current_song(self, guild, song):
        playlist = self.get_playlist(guild)
        playlist[guild]['current'] = song
        self.write_json_file(playlist)
        return playlist[guild]['current']
    
    def set_next_song(self, guild):
        playlist = self.get_playlist(guild)
        playlist[guild]['previous'].append(playlist[guild]['current'])
        
        if len(playlist[guild]['queue']) == 0: 
            playlist[guild]['current'] = {}    
        else: 
            playlist[guild]['current'] = playlist[guild]['queue'].pop(0)   
        self.write_json_file(playlist)
        return playlist[guild]['current']
    
    def clear_current_song(self, guild):
        playlist = self.get_playlist(guild)
        playlist[guild]['current'] = {}
        self.write_json_file(playlist)
        
    ###### Queue
    def get_queue(self, guild): 
        playlist = self.get_playlist(guild, guild_only=True)
        return playlist['queue']
    
    def clear_queue(self, guild): 
        playlist = self.get_playlist(guild)
        playlist[guild]['queue'] = []
        self.write_json_file(playlist)
    
    def remove_last_queue(self, guild):
        playlist = self.get_playlist(guild)
        queue = playlist[guild]['queue']
        if len(queue) > 0: 
            queue.pop(-1)
            self.write_json_file(playlist)
       
    def remove_queue_index(self, guild:str, index:int): 
        playlist = self.get_playlist(guild)
        queue = playlist[guild['queue']]
                         
        if len(queue) < index or index <= 0:
            return None
        removed = queue.pop(index-1)
        self.write_json_file(playlist)
        return removed
        
    def remove_queue_duplicates(self, guild): 
        playlist = self.get_playlist(guild)
        queue = playlist[guild['queue']]
        
        uniques = set()
        new = []
        for i in queue:
            item = tuple(i.items())
            if item not in uniques:
                uniques.add(item)
                new.append(i)
                
        queue = new      
        self.write_json_file(playlist)
        
    def shuffle_queue(self, guild):
        playlist = self.get_playlist(guild)
        random.shuffle(playlist[guild]['queue'])
        self.write_json_file(playlist)
        
    def add_song_to_queue(self, guild, url, path, title=None):
        playlist = self.get_playlist(guild)
        playlist[guild]['queue'].append(
            {
                'title' : title,
                'url'   : url,
                'path'  : path              
            }
        )
        self.write_json_file(playlist)
            
    ###### Previous
    def add_song_previous(self, guild, song: dict):
        if song == {}:
            return False
        playlist = self.get_playlist(guild)
        playlist[guild]['previous'].append(song)
        self.write_json_file(playlist)
        return True
        
    def clear_playlist(self, guild: str):
        playlist = self.read_json_file()
        playlist.pop(guild, 0)
        self.write_json_file(playlist) 
    
    #### To do
    # SWTCH CAMELCASE FOR SNAKECASE
    def addDefaultPlaylist(self): pass
    def loadSavedPlaylist(self): pass
    def savePlaylistPrivate(self): pass
    def savePlaylistPublic(self): pass
    
    def downloadPlaylist(self): pass
    def loadPlaylist(self): pass
            
    #################################################
    #                  PLAYLIST                     #                                       
    #                                               #
    #################################################   
                       
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
                
        guild = str(ctx.guild.id)
        yt_links = yt.search(search, cant=2)
             
        #expresion regular para poner opcion1-N
        if 'opcion2' in ctx.message.content.split():
            song_yt_link = yt_links[1]
        else:
            song_yt_link = yt_links[0]
        video_title = yt.source(song_yt_link).title   

        if self.get_status(guild): 
            await ctx.send(f'> Song queued -> {video_title}')
            
        song_path = yt.downloadAudioYT(source=song_yt_link, size_limit_mb=self.max_audio_size, dir=self.dir)
   
        self.add_song_to_queue(guild, 
                        song_yt_link, 
                        song_path, 
                        video_title) 
        
        if not self.get_status(guild): 
            if voice.is_playing(): voice.stop()
            self.set_next_song(guild)
            self.set_status(guild, True)
             
        else: return

        voice.play(
            nextcord.FFmpegPCMAudio(source=self.get_current_song(guild)['path']),
            after=lambda e: self.next_song(ctx, voice, guild)
            )
           
        voice.pause()
        await asyncio.sleep(1)
        voice.resume()
        await ctx.send(f"> Playing: {self.get_current_song(guild)['url']}")
    

    async def next_song(self, ctx, voice, guild):
        if len(self.get_queue(guild)) > 0:      
            self.set_next_song(guild)  
            voice.play(
                    nextcord.FFmpegPCMAudio(source=self.get_current_song(guild)['path']),
                    after=lambda e: self.next_song(ctx, voice, guild)
                )
    
            voice.pause()
            await asyncio.sleep(1)
            voice.resume()
            
            await ctx.send(f"> Playing: {self.get_current_song(guild)['url']}")     
        else: 
            self.set_status(guild, False)

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
        if len(self.get_queue(str(ctx.guild.id))) == 0:
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
        
        guild = str(ctx.guild.id)
        if len(self.get_queue(guild)) == 0 and self.get_current_song(guild) == {}:
            await ctx.send("> No hay canciones en la playlist")
            return
        
        temp = []
        temp.append(f'{self.get_current_song(guild)["title"]}')
        
        if not len(self.get_queue(guild)) == 0:
            for i, song in enumerate(self.get_queue(guild)):
                temp.append(f'{i+1}) {song["title"]}')
        await ctx.send("> Playlist:\n> Actual: " + "\n> ".join(temp))
  
      
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