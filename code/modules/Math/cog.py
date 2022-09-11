from os import sep
from nextcord.ext import commands
from modules.Help.cog import HelpCommands
from modules.Math import f_table_1
from modules.Math import binary

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


def setup(bot: commands.Bot):
    bot.add_cog(Math(bot))