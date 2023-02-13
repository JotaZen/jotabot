import nextcord as discord
from nextcord.ext import commands

from datetime import datetime
import os

from urls.urls import URLManager
from utilities.configs import JotabotConfig

def jotabot():
    CONFIGS = JotabotConfig(config_file='config.ini', default_configs='./utilities/saves/default_configs.ini')
    URLS = URLManager(CONFIGS.get('URLS', 'directory'))
    extra_kwargs = {
        'CONFIGS':CONFIGS,
        'URLS':URLS
    }
    bot = commands.Bot(command_prefix=CONFIGS.get('Jotabot', 'command_prefix'), intents=discord.Intents.all())
    Cogs = []
    
    try:
        with open(CONFIGS.get('Jotabot', 'TOKEN'), "r") as f:
            TOKEN = f.read()     
    except KeyError:
        TOKEN = input("DISCORD TOKEN: ")
        with open(CONFIGS.get('Jotabot', 'TOKEN'), "w") as f:
            f.write(TOKEN)
    finally:
        print(f'TOKEN = "{TOKEN[0:10]}..."')  

    @bot.event
    async def on_message(message):
        if message.author == bot.user: return
        elif "silksong" in message.content.split():
            embed = discord.Embed(title="¿Silksong?", description="Todavia no sale Silksong.",
                timestamp=datetime.now(), color=discord.Color.red())
            embed.set_thumbnail(url=URLS.get("Img", "hornet_miniature"))
            await message.channel.send(embed=embed)
        await bot.process_commands(message)
        
    @bot.event
    async def on_ready():
        await bot.change_presence(activity=discord.Game(name=CONFIGS.get('Jotabot', 'activity')))
        print(f'Módulos Cargados: ', end='')
        for i in Cogs[0:-1]:
            print(f'{i}, ', end='')
        print(Cogs[-1]+'.')
        print("My boty is ready")
    
    @bot.command(aliases=["-reload"])
    async def __reloadExtensions(ctx):
        """-reload - Recarga al bot"""
        
        CONFIGS = JotabotConfig(config_file='config.ini', default_configs='./utilities/saves/default_configs.ini')
        URLS = URLManager(CONFIGS.get('URLS', 'directory'))
        extra_kwargs = {
            'CONFIGS':CONFIGS,
            'URLS':URLS
        } 
        
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
            bot.load_extension(f"modules.{folder}.cog", extras=extra_kwargs)
            try:
                
                Cogs.append(folder)
            except:
                 print(f'[ERROR] Cog "{folder}" not Loaded')                  
    
    bot.run(TOKEN)   
        
if __name__ == "__main__":
    print("\nRunning Jotabot ...")
    jotabot()

