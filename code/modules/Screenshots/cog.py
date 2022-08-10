from nextcord.ext import commands

import modules.Screenshots.screenshots as ss
import nextcord as discord


class Screenshot(commands.Cog, name="Screenshots"):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def scramshot(self, ctx):
        if ss.screenshotLimit(): 
            await ctx.send(ss.limitData("message"))   
        else: 
            await ctx.send(file = discord.File(ss.screenshot()))

    @commands.command()
    async def scramshow(self, ctx):         
        await ctx.send(ss.screenshotList())

def setup(bot: commands.Bot):
    bot.add_cog(Screenshot(bot))