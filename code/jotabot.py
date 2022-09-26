import nextcord as discord
from nextcord.ext import commands

from datetime import datetime
import os

from urls.urls import URLManager
from utilities.configs import JotabotConfig


def jotabot():

    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix="", intents=intents)
    CONFIGS = JotabotConfig('config.ini', './utilities/saves/default_configs.ini')
    URLS = URLManager('./urls')
    extra_kwargs = {
        'CONFIGS':CONFIGS,
        'URLS':URLS
    }
    Cogs = []
 
    with open("../botToken.txt", "r") as file:
        token = file.read()
        print(f'Token = "{token[0:10]}..."')  
         
    @bot.event
    async def on_message(message):
        if message.author == bot.user: return
        elif "silksong" in message.content.split():
            embed = discord.Embed(title="¿Silksong?", description="Todavia no sale Silksong.",
                timestamp=datetime.now(), color=discord.Color.red())
            embed.set_thumbnail(url=URL.get("Img", "hornet_miniature"))
            await message.channel.send(embed=embed)
        await bot.process_commands(message)
        
    @bot.event
    async def on_ready():
        await bot.change_presence(activity=discord.Game(name="Among Us"))
        print(f'Módulos Cargados: ', end='')
        for i in Cogs[0:-1]:
            print(f'{i}, ', end='')
        print(Cogs[-1]+'.')
        print("My boty is ready")
    
    @bot.command(aliases=["-reload"])
    async def __reloadExtensions(ctx):
        """-reload - Recarga al bot"""
             
        bot.reload_extension("modules.Help.cog")
        for folder in os.listdir("modules"):
            if not (os.path.exists(os.path.join("modules", folder, "cog.py")) and folder != "Help"):
                continue
            if folder in Cogs:
                bot.unload_extension(f"modules.{folder}.cog")
                Cogs.remove(folder)         
            try:                     
                bot.load_extension(f"modules.{folder}.cog", extras=extra_kwargs)
                Cogs.append(folder)
            except:
                print(f'[ERROR] Cog "{folder}" not Loaded')                
        else:
            print("[INFO] Cogs Recargados")
            await ctx.send("> Se han actualizado los comandos")

    bot.load_extension("modules.Help.cog")
    for folder in os.listdir("modules"):
        if os.path.exists(os.path.join("modules", folder, "cog.py")) and folder != "Help":  
            try:
                bot.load_extension(f"modules.{folder}.cog", extras=extra_kwargs)
                Cogs.append(folder)
            except:
                 print(f'[ERROR] Cog "{folder}" not Loaded')                  
    
    bot.run(token)



def extensionsLoad(bot: commands.Bot, folder: str, loaded_extensions: list, CONFIGS: dict):
    if not (os.path.exists(os.path.join("modules", folder, "cog.py")) and folder != "Help"):
        return
    file = f"modules.{folder}.cog"
    
    if folder in loaded_extensions:
        bot.unload_extension(file)
        loaded_extensions.remove(folder)         
    try:                     
        bot.load_extension(file, extras={'CONFIGS':CONFIGS})
        loaded_extensions.append(folder)
    except:
        print(f'[ERROR] Cog "{folder}" not Loaded')   
    
        
if __name__ == "__main__":
    print("Running Jotabot ...")
    jotabot()

