#from dotenv import load_dotenv # FOR LOCAL USE
import os
import requests
import random
import discord
from discord.ext import commands

#load_dotenv() # FOR LOCAL USE
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='&', intents=intents)
bot.remove_command("help")

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Element Bot Help", colour=discord.Color.from_rgb(125, 69, 255), description="This offers a basic explanation of all the commands that can be understood by Element Bot.")
    prefix = await bot.get_prefix(ctx.message)
    for bot_command in bot.commands:
        if (bot_command.name != 'help'):
            embed.add_field(name=prefix + bot_command.name, value=bot_command.help, inline=False)
    await ctx.send(embed=embed)

@bot.command(name="hi", help="Responds with the fingerguns emoji.")
async def fingerguns_hello(ctx):
    guild = discord.utils.get(bot.guilds, name=GUILD)
    fingerguns = discord.utils.get(guild.emojis, name="fingerguns")
    await ctx.send(f"<:{fingerguns.name}:{fingerguns.id}>")

@bot.command(name="F", help="Responds with \"F's in the chat :(\"")
async def f_method(ctx):
    await ctx.send("F's in the chat :(")

@bot.command(name="motivate", help="Responds with a motivational quote.")
async def motivate(ctx):
    message = ""
    response = requests.get("https://zenquotes.io/api/random")
    if response.status_code == 200:
        quote = response.json()
        message = quote[0]['q']
        author = quote[0]['a']
        if message.startswith("Too many requests."):
            await ctx.send("The ZenQuotes API is overloaded. Please wait 30 seconds before trying again.")
        else:
            embed_quote = discord.Embed(title="Motivational Quotes", type="rich", url="https://zenquotes.io/")
            embed_quote.color = discord.Color.from_rgb(125, 69, 255)
            embed_quote.set_thumbnail(url="https://user-images.githubusercontent.com/42954045/102170926-49b47f80-3e4a-11eb-929b-eed606a70399.png") \
                      .add_field(name='Quote:',value="_" + message + "_", inline=False) \
                      .add_field(name='Author:', value=author, inline=False) \
                      .set_footer(text="Quotes provided by ZenQuotes", icon_url=bot.user.avatar_url)
            await ctx.send(embed=embed_quote)
    else:
        await ctx.send("An unknown error occurred. Please try again later.")

@bot.command(name="compliment", help="Compliments a user, or yourself\nif no user is provided.")
async def compliment(ctx, user: discord.Member=None):
    mentioned_user = user if user is not None else ctx.message.author
    quotes = [
        "{}, I appreciate you a lot!",
        "Thanks for being so awesome {}!",
        "Who's got two thumbs and a lovely personality? It's {} of course!",
        "You are an excellent friend {}!",
        "I am glad that we met {}!",
        "You got this {}!",
        "{}, I believe in you!",
        "I hope you are proud of yourself {}, because I am!",
        "{}, you're a smart cookie!",
        "{}, you deserve a hug right now (if you want one of course)!",
        "How are you so cool {}?",
        "Hey {}, you're a wonderful person!",
        "I'm lucky to have you in my life {}!",
        "Never stop being you {}!",
        "Who's a Kool Kat? You are {}!",
        "It's a great day because you're here {}!",
        "{}, you are a strong and resilient person who has fought many hard battles!"
    ]
    await ctx.send(f"**{ctx.message.author.mention} says:**  " + random.choice(quotes).format(mentioned_user.mention))

bot.run(TOKEN)