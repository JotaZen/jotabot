from nextcord.ext import commands
import modules.yTube.yTube as yt
import os
from nextcord.utils import get
import nextcord as discord

import asyncio

class MusicPlayer(commands.Cog, name="Music Player"):
    """Music"""
    
    def __init__(self, bot):
        self.bot = bot
        self.song_queue = []       
        self.dir = "./modules/MusicPlayer/temp"
        
    @commands.command(aliases=["-p"])
    async def __play(self, ctx, *, search): 
                
        song_yt_link = yt.search(search)
        yt.download(source=song_yt_link, dir=self.dir)
        
        video_title = yt.source(song_yt_link).title      
        for i in '!<>/\\:?|*"':
            video_title = video_title.replace(i,"")
        
        self.song_queue.append(video_title)

        voice = get(self.bot.voice_clients, guild = ctx.guild)
        
        if not voice.is_playing():
            
            song = f"{dir}/{self.song_queue[0]}.mp4"
                        
            voice.play(discord.FFmpegPCMAudio(source=song))
            voice.pause()
            await asyncio.sleep(1)
            voice.resume()
            
            print(self.song_queue.pop(0))          
            await ctx.send(f"> Playing: {song_yt_link}")
        else:
            await ctx.send('Song queued')    

    

    @commands.command(aliases=["-pause", "-play"])
    async def __pause(self, ctx): 
        
        voice = get(self.bot.voice_clients, guild = ctx.guild)
        
        if voice.is_playing():
            voice.pause()
        else:
            voice.resume()

    
    @commands.command(aliases=["-stop"])
    async def __stop(self, ctx): 
        
        voice = get(self.bot.voice_clients, guild = ctx.guild)
        voice.stop()

    @commands.command(aliases=["-playlist"])
    async def __playlist(self, ctx): 
        
        if self.song_queue == []: 
            await ctx.send("> No hay canciones en la playlist")
            return
        
        temp = []
        for song in self.song_queue:
            temp.append(song)
        await ctx.send("> Playlist:\n> " + "\n> ".join(temp))
    
     
            
        
def setup(bot: commands.Bot):
    bot.add_cog(MusicPlayer(bot))