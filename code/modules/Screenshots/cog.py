from nextcord.ext import commands

from modules.Help.cog import HelpCommands

import modules.Screenshots.screenshots as ss
import nextcord as discord


class Screenshot(commands.Cog, name="Screenshots"):
    
    def __init__(self, bot, CONFIGS, **kwargs):
        self.bot = bot
        self.directory = CONFIGS.get(self.__cog_name__, 'directory')
        HelpCommands.AddCommands(self.get_commands())
        
    @commands.command(aliases=["-ss"])
    async def __scramshot(self, ctx):
        """-ss - Toma una screenshot"""
        if ss.screenshotLimit(): 
            await ctx.send(ss.limitData("message"))   
        else: 
            await ctx.send(file = discord.File(ss.screenshot()))

    @commands.command(aliases=["-show"])
    async def __scramshow(self, ctx):  
        """-show - Lista de screenshots"""       
        await ctx.send(ss.screenshotList())

def setup(bot, **kwargs):
    bot.add_cog(Screenshot(bot, **kwargs))