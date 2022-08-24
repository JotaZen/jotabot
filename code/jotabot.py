import nextcord as discord
from nextcord.ext import commands

from datetime import datetime
import os

from urls.urls import URL
      
def jotabot():
    
    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix="", intents=intents)
 
    @bot.event
    async def on_message(message):
        if message.author == bot.user: return 
        elif "silksong" in message.content.split():
            embed = discord.Embed(title="¿Silksong?", description="Todavia no sale Silksong.", 
                timestamp=datetime.now(), color=discord.Color.red())
            embed.set_thumbnail(url=URL.get("Img", "hornet_miniature"))
            await message.channel.send(embed=embed)
        await bot.process_commands(message)   
    
            
    @bot.command(aliases=["-reload"])
    async def __reload(ctx):
        """-reload - Recarga al bot"""   
        bot.reload_extension("modules.Help.cog")
        for folder in os.listdir("modules"):
            if os.path.exists(os.path.join("modules", folder, "cog.py")) and folder != "Help":
                bot.reload_extension(f"modules.{folder}.cog")
        else:        
            print("Cogs Recargados")        
            await ctx.send("Se han actualizado los comandos")
            
    
    bot.load_extension("modules.Help.cog")  
    for folder in os.listdir("modules"):
        
        if os.path.exists(os.path.join("modules", folder, "cog.py")) and folder != "Help":
            bot.load_extension(f"modules.{folder}.cog")
                    
            
    with open("../botToken.txt", "r") as file:
        token = file.read()
        print(f'Token = "{token[0:10]}..."')
    
    @bot.event
    async def on_ready():
        await bot.change_presence(activity=discord.Game(name="Hollow Knight: Silksong"))
        #All OK#
        print("My boty is ready")  
        
    bot.run(token)
    

if __name__ ==  "__main__":
    print("Running Jotabot ...")
    jotabot()

