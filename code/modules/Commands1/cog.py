import nextcord
from nextcord.ext import commands
from nextcord.utils import get

import modules.Commands1.simple_commands as simple
import random

class Commands1(commands.Cog, name="General Commands"):
    
    def __init__(self, bot):
        self.bot = bot


    #---------Text---------# 
    @commands.command(aliases=simple.Memes.commands())
    async def __plainTextResponse(self, ctx):
        await ctx.send(simple.plainText(ctx.message.content))
             

    @commands.command()
    async def mona(ctx):
        i = random.choice((1,2,3,4,5))
        await ctx.send(file=nextcord.File(f"../files/monas/{i}.png"))
        

    @commands.command(aliases = ["-ping"])
    async def ping_bot(self, ctx): 
        await ctx.send(f"Tengo {round(self.bot.latency * 1000)}ms")
        

    @commands.command(aliases = ["-clear"])
    async def clear_command(self, ctx, amount = 1):
        await ctx.channel.purge(limit = amount + 1) if amount < 6 else False
        
    
    #---------Voice---------#  
    @commands.command()
    async def venbot(self, ctx):
        channel = ctx.message.author.voice.channel
        if not channel:
            await ctx.send("No estas en un canal de voz ~")
            return
        voice = get(self.bot.voice_clients, guild = ctx.guild)

        if voice: await voice.move_to(channel)           
        else: await channel.connect()           

    @commands.command()
    async def salbot(self, ctx):
        voice = get(self.bot.voice_clients, guild = ctx.guild)
        await voice.disconnect() 



def setup(bot: commands.Bot):
    bot.add_cog(Commands1(bot))