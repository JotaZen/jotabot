from nextcord.ext import commands
from modules.Help.cog import HelpCommands
from modules.Math import f_table_1, binary

import csv
import requests

class Math(commands.Cog, name="Math"):
    
    def __init__(self, bot):
        self.bot = bot
        HelpCommands.AddCommands(self.get_commands())
        

    @commands.command(aliases=["-data"])
    async def __data(self, ctx, *, DATA):
        """-data - Tabla de Frecuencia a partir de una serie de datos"""
        DATA = DATA.split(sep=" ")
        await ctx.send(f_table_1.tablaFrecuencia(DATA))
        
    
    @commands.command(aliases=["-binary"])
    async def __binary(self, ctx, number):
        """-binary - Transformador de numeros entero a su representación binaria"""
        number = int(number)
        await ctx.send(f'{number} a binario: {binary.decimalToBinary(number)}')
        
    
        
    @commands.command(aliases=["!!test"])
    async def __testsaasdasd(self, ctx):
        files = ctx.message.attachments.copy()
        
        if len(files) != 1:
            await ctx.send(f'> **Comando solo diponible con 1 archivo CSV o JSON**')
        
        files = files[0].url     
        DATA = requests.get(files).content.decode('utf-8')
        DATA = list(csv.reader(DATA.splitlines(), delimiter=','))[0]
        await ctx.send(f_table_1.tablaFrecuencia(DATA))
        

def setup(bot, **kwargs):
    bot.add_cog(Math(bot))