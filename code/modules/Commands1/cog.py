
import nextcord
from nextcord.ext import commands
from nextcord.utils import get

import random
import asyncio
import datetime as dt
from datetime import datetime

from modules.Help.cog import HelpCommands
from urls.urls import URL

import modules.APIs.requests as Request
import modules.Commands1.simple_commands as simple
import modules.Commands1.scrapper_horosc as horoscope

class Commands1(commands.Cog, name="General Commands"):
    
    def __init__(self, bot):
        self.bot = bot
        self.API = URL.getAllFromType("API")
        self.Img = URL.getAllFromType("Icon")
        self.Icon = URL.getAllFromType("Img")
        HelpCommands.AddCommands(self.get_commands())

    #---------Text---------# 
    @commands.command(aliases=simple.Memes.commands())
    async def __plainTextResponse(self, ctx):
        await ctx.send(simple.plainText(ctx.message.content))
             

    @commands.command(aliases=["mona"])
    async def __mona(self, ctx):
        """mona - Mona china aleatoria"""
        i = random.choice((1,2,3,4,5))
        await ctx.send(file=nextcord.File(f"../files/monas/{i}.png"))
        

    @commands.command(aliases = ["-ping"])
    async def __ping_bot(self, ctx): 
        """-ping - Ping del bot"""
        await ctx.send(f"Tengo {round(self.bot.latency * 1000)}ms")
        

    @commands.command(aliases = ["-clear"])
    async def __clear_command(self, ctx, amount = 1):
        """-clear - Borra hasta 6 mensajes"""
        await ctx.channel.purge(limit = amount + 1) if amount < 6 else False
        
                
    #---------Embeds--------#
    
    @commands.command(aliases=["towastc"])
    async def __towastatic(self, ctx):
        """towastc - Towa static"""    
        
        links = [
            "https://safebooru.org//samples/3828/sample_0ce103530ab2d500fcbc8589babe28233b833b32.jpg?3999183",
            "https://safebooru.org//samples/3868/sample_3d8d307be6c8d6f49a9bfd66f8be55b7c26b863e.jpg?4042524",
            "https://safebooru.org//samples/3899/sample_d93f1ae64123c356db41b2c29e716235c6b8d04b.jpg?4075801",
            "https://safebooru.org//samples/3926/sample_4e4450bc534f78aafd1513a1d606b1fc65fbd8fa.jpg?4103635"                                     
        ]
        embeds = []
        
        for i in links:
            embed = nextcord.Embed(
                    color=nextcord.Color.dark_purple())
            embed.set_image(i)        
            embeds.append(embed)
            
        self.bot.help_pages = embeds       
        buttons = [u"\u23EA",u"\u25C0",u"\u25B6",u"\u23E9"]
        c = 0
        msg = await ctx.send(embed=embeds[c])
        
        for button in buttons:
            await msg.add_reaction(button)

        while True:
            try:
                reaction, user = await self.bot.wait_for(
                    "reaction_add", 
                    check=lambda reaction, user: user != self.bot.user and reaction.message == msg and reaction.emoji in buttons, 
                    timeout=60.0                
                )
            except asyncio.TimeoutError:
                embed = self.bot.help_pages[c]
                embed.set_footer(text="Timed Out.")
                await msg.clear_reactions()
            
            else:
                previous = c              
                if reaction.emoji == buttons[0]:  
                    c = 0
                elif reaction.emoji == buttons[1]:  
                    if c>0: 
                        c -= 1   
                elif reaction.emoji == buttons[2]:  
                    if c < len(embeds)-1: 
                        c += 1 
                elif reaction.emoji == buttons[3]:  
                    c = len(embeds)-1 
                
                for button in buttons:
                    await msg.remove_reaction(button, ctx.author)
                
                if c != previous:
                    await msg.edit(embed=embeds[c])
    
        
    #---------Voice---------#  
    @commands.command(aliases=["venbot"])
    async def __venbot(self, ctx):
        """venbot - Bot a Voz"""
        channel = ctx.message.author.voice.channel
        if not channel:
            await ctx.send("No estas en un canal de voz ~")
            return
        voice = get(self.bot.voice_clients, guild = ctx.guild)

        if voice: await voice.move_to(channel)           
        else: await channel.connect()           


    @commands.command(aliases=["salbot"])
    async def __salbot(self, ctx):
        """salbot - Saca al Bot"""
        voice = get(self.bot.voice_clients, guild = ctx.guild)
        await voice.disconnect() 


    #---------Horoscope---------# 
    @commands.command(aliases=["horoscopo", "horóscopo", "-horo"])
    async def __horoscope(self, ctx, sign):
        if horoscope.symbol(sign) == "":
            return
        
        horoscope_today = horoscope.parseHome(sign)
        text = "***" + "***\n ".join(horoscope_today["horoscope"]) + ""
        
        embed = nextcord.Embed(
            title=horoscope.symbol(sign),
            description=text,
            timestamp=datetime.today(),
            color=nextcord.Color.blue()
        )
        
        await ctx.send(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(Commands1(bot))