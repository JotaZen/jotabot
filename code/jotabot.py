import discord
from discord.ext import commands as d_commands
from discord.utils import get
from discord_components import Button, DiscordComponents

from datetime import datetime
import random
import os
import simple_utilities as Sp
import pyautogui

from commands import help_commands as hc, yTube, simple_commands as simple


bot = d_commands.Bot(command_prefix="")
DiscordComponents(bot) 
            
#---------Events---------#
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="Hollow Knight: Silksong"))
    print("My boty is ready")

@bot.event
async def on_message(message):
    if message.author == bot.user:return 
    if message.content == "xd": 
        answersFaces = ["AwA", "Owo", "Uwu", "uwu", "(๑╹ᆺ╹)"]  
        await message.channel.send(random.choice(answersFaces))
    elif "silksong" in message.content.split():
        embed = discord.Embed(title="¿Silksong?", description="Todavia no sale Silksong.", 
            timestamp=datetime.utcnow(), color=discord.Color.red())
        embed.set_thumbnail(url="https://static.wikia.nocookie.net/hollowknight/images/1/16/Hornet_Idle.png/revision/latest?cb=20181124144744")
        await message.channel.send(embed=embed)
    await bot.process_commands(message)   

#---------Test---------#
    
@bot.command()
async def test(ctx):
    await ctx.send("aaaaaa",       
        components = [Button(label = "papa", custom_id = "papa")])
    interaction = await bot.wait_for("button_click", check = lambda x: x.custom_id == "papa")
    await interaction.send("xd")


@bot.command()
async def scramshot(ctx):
    myScreenshot = pyautogui.screenshot()
    i_ss = len(os.listdir("../files/ss/")) +1
    myScreenshot.save(f"../files/ss/{i_ss}.png")
    await ctx.send(file=discord.File(f"../files/ss/{i_ss}.png"))  

@bot.command()
async def scramshow(ctx):
    sss = os.listdir("../files/ss")
    sss = "> " + "\n- ".join(sss)            
    await ctx.send(sss)

@bot.command()
async def scram(ctx, index):
    await ctx.send(file=discord.File(f"../files/ss/{index}.png")) 

#---------YouTube---------#

@bot.command()
async def yt(ctx,*, search): await ctx.send(yTube.ytSearch(search))

@bot.command()
async def ytlist(ctx): await ctx.send(yTube.dwList(separator = ">"))  

@bot.command()
async def ytdwl(ctx, *, search): 
    yTube.ytDownload(search)
    await ctx.send(yTube.ytSearch(search))            
    
#---------Commands---------#

@bot.command(aliases = simple.Memes.commands())
async def plainTextResponse(ctx):
    await ctx.send(simple.plainText(ctx.message.content))

@bot.command()
async def mona(ctx):
    i = random.choice((1,2,3,4,5))
    await ctx.send(file=discord.File(f"../files/monas/{i}.png"))

@bot.command(aliases = ["-ping"])
async def ping_bot(ctx): await ctx.send(f"Tengo {round(bot.latency * 1000)}ms")

@bot.command(aliases = ["-clear"])
async def clear_command(ctx, amount = 1):
        await ctx.channel.purge(limit = amount + 1) if amount < 6 else False

#---------Voice---------#  
@bot.command()
async def venbot(ctx):
    channel = ctx.message.author.voice.channel
    if not channel:
        await ctx.send("No estas en un canal de voz ~")
        return
    voice = get(bot.voice_clients, guild = ctx.guild)

    if voice: await voice.move_to(channel)           
    else: await channel.connect()       

@bot.command()
async def salbot(ctx):
    voice = get(bot.voice_clients, guild = ctx.guild)
    await voice.disconnect()

#--------HELP--------#
@bot.command(aliases = ["-help","-?","-ayuda","-h", "-db"])
async def help_command(ctx): 
    if ctx.message.content == "-db": 
        await ctx.send(hc.datab_commands.get())  
    else: 
        await ctx.send(hc.help_commands.get()) 

#---------Run---------#  

with open("../botToken.txt", "r") as file:
    token = file.read()
    print(f'Token = "{token}"')

bot.run(token)
