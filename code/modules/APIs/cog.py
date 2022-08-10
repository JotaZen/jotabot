import nextcord
from nextcord.ext import commands

import requests
from datetime import datetime
from urls.icons_url import Icon
from urls.api_urls import API

class APIs(commands.Cog, name="APIs Requests"):
    
    def __init__(self, bot):
        self.bot = bot

    
    #---------Weather---------# 
    @commands.command(aliases=["!clima"]) # Los Angeles Quitada
    async def __weather(self, ctx, city: str="Los Ángeles"):
        response = requests.get(API.get("Gael Weather API"))
        response = response.json()

        weather = list(filter(lambda x: x["Estacion"] == city, response))            
         
        if len(weather) != 0:
            weather = weather[0]       
        else: return
        
        embed = nextcord.Embed(
            title=f'***Clima en {weather["Estacion"]}***', 
            description=f'Temperatura: {weather["Temp"]}°\n'
                        f'Humedad: {weather["Humedad"]}%\n'                    
                        f'**{weather["Estado"]}**',             
            timestamp=datetime.utcnow(), 
            color=nextcord.Color.purple()
            )
        
        embed.set_thumbnail(url=Icon.get("weather_default"))
        if weather["Estado"] == "Despejado":
            embed.set_thumbnail(url=Icon.get("weather_clear"))
              
        await ctx.send(embed=embed)      


    #---------Money---------# 
    @commands.command(aliases=["!usd"]) 
    async def __clptousd(self, ctx, clp=None, usd=None,currency="USD"):
        response = requests.get(API.get("Gael Monedas API"))
        response = response.json()
        value = list(filter(lambda x: x["Codigo"] == currency, response)) 
        
        if len(value) != 1: return
        
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
        embed.set_thumbnail(url=Icon.get("dolar"))
        
        await ctx.send(embed=embed)
        

        
         


def setup(bot: commands.Bot):
    bot.add_cog(APIs(bot))