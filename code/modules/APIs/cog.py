import nextcord
from nextcord.ext import commands

import asyncio
import requests

from datetime import datetime

import modules.APIs.requests as Request
class APIs(commands.Cog, name="APIs Requests"):
    
    def __init__(self, bot, CONFIGS, URLS,**kwargs):
        self.bot = bot
        self.URL = URLS
        self.poke_api = URLS.get("API","PokeAPI")
        self.weather_api = URLS.get("API","Gael Weather API")
        self.usd_api = URLS.get("API", "Gael Monedas API")
   
   
    #---------Weather---------# 
    @commands.command(aliases=["!clima"]) # Los Angeles Quitada
    async def __weather(self, ctx, city: str="Los Ángeles"):
        """!clima - Clima en Los Ángeles (se cae a cada rato)"""
        response = requests.get(self.weather_api)
        response = response.json()
        weather = list(filter(lambda x: x["Estacion"] == city, response))            
         
        if len(weather) != 0:
            weather = weather[0]       
        else: 
            print("!clima no disponible")
            return
        
        embed = nextcord.Embed(
            title=f'***Clima en {weather["Estacion"]}***', 
            description=f'Temperatura: {weather["Temp"]}°\n'
                        f'Humedad: {weather["Humedad"]}%\n'                    
                        f'**{weather["Estado"]}**',             
            timestamp=datetime.now(), 
            color=nextcord.Color.purple()
            )
        
        embed.set_thumbnail(url=self.URL.get("Icon", "weather_default"))
        if weather["Estado"] == "Despejado":
            embed.set_thumbnail(url=self.URL.get("Icon", "weather_clear"))
              
        await ctx.send(embed=embed)      

    #---------Money---------# 
    @commands.command(aliases=["!usd"]) 
    async def __clptousd(self, ctx, clp=None, usd="",currency="USD"):
        """!usd - Valor del dólar (se cae a cada rato)"""
        response = requests.get(self.usd_api)
        response = response.json()
        value = list(filter(lambda x: x["Codigo"] == currency, response)) 
        
        if len(value) != 1 or value[0]["Valor"] == "ND": return

        conv  = int(float((value[0]["Valor"]).replace(",", ".")))
        
        if not clp or not clp.isnumeric():
            t = '***Dolar***'
            d = f'**El dolar vale: ${conv}**'
        
        elif clp.isnumeric():  
            clp = int(clp)
                        
            if usd.lower() == "usd":
                dolar_to_clp = int(clp * conv)
                clp = '{:_}'.format(clp).replace("_",".")
                dolar_to_clp = '{:_}'.format(dolar_to_clp).replace("_",".")
                t = '***Dolar a CLP***'
                d = (f' **{clp}** {"dólar" if clp=="1" else "dólares"}\n'
                    f'  {"equivale" if clp=="1" else "equivalen"} a:\n'
                    f' **${dolar_to_clp}**\n')
            else:
                dolar_to_clp = int(clp/conv) 
                clp = '{:_}'.format(clp).replace("_",".")
                dolar_to_clp = '{:_}'.format(dolar_to_clp).replace("_",".")
                t = '***CLP a Dolar***'
                d = (f' **${clp}**   \n' 
                    f'  {"equivale" if clp=="1" else "equivalen"} a:\n'
                    f' **{dolar_to_clp}** {"dólar" if dolar_to_clp=="1" else "dólares"}\n')      
            
        embed = nextcord.Embed(
        title       = t, 
        description = d,
        timestamp   = datetime.now(), 
        color       = nextcord.Color.green()
        )
        embed.set_thumbnail(url=self.URL.get("Icon", "dolar"))
        
        await ctx.send(embed=embed)     
    
    #---------Safebooru---------# 
    @commands.command(aliases=["towa"])
    async def __towa(self, ctx):
        """towa - Towa Safebooru"""       
       
        source = self.URL.get("API", "Safebooru")        
        tags = ["tags=tokoyami_towa"]     
        cant = 10
        links = [ i for i in Request.booruImgs(source, tags=tags, limit=cant)                                          
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
    
    @commands.command(aliases=["-booru"])
    async def __booru(self, ctx, tag):
        """-booru - Safebooru search"""       
        print(f"Searching {tag}")
        source = self.URL.get("API", "Safebooru")             
        tags = [f"tags={tag}"]      
        cant = 15
        links = [i for i in Request.booruImgs(source, tags=tags, limit=cant)                                          
        ]
        embeds = []
        n = 1
        for i in links:
            embed = nextcord.Embed(
                    title=f"{n}/{len(links)}",
                    color=nextcord.Color.red())
            embed.set_image(i)   
            embeds.append(embed)
            n += 1
            
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
      
    @commands.command(aliases=["-booru100"])
    async def __booru100(self, ctx, tag):
        """-booru100 - Safebooru search x 100"""       
        print(f"Searching {tag}")
        source = self.URL.get("API", "Safebooru")        
        tags = [f"tags={tag}"]      
        cant = 100
        links = [i for i in Request.booruImgs(source, tags=tags, limit=cant)                                          
        ]
        embeds = []
        n = 1
        for i in links:
            embed = nextcord.Embed(
                    title=f"{n}/{len(links)}",
                    color=nextcord.Color.red())
            embed.set_image(i)   
            embeds.append(embed)
            n += 1
            
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
                    timeout=60.0 * 5                
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
      
    #---------Pokeapi---------#  
    @commands.command(aliases=["-pokerandom"])
    async def __pokemon(self, ctx):
        """Random Pokemon from PokeAPI"""
 
        pkmn = Request.pokeRandom(self.poke_api)
        print(pkmn["types"])
        types = [i["type"]["name"].capitalize() for i in pkmn["types"]]
        
        pokemon = nextcord.Embed(
            title=pkmn["name"].capitalize(),      
            description="["+"][".join(types)+"]",
            color=nextcord.Color.yellow()
        ) 
        pokemon.set_thumbnail(f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pkmn['id']}.png")
        await ctx.send(embed=pokemon)           

def setup(bot, **kwargs):
    bot.add_cog(APIs(bot, **kwargs))