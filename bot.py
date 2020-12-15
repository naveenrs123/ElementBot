#from dotenv import load_dotenv # FOR LOCAL USE
import os
import requests
import discord
from discord.ext import commands

#load_dotenv() # FOR LOCAL USE
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name="hi", help=f"Responds with the fingerguns emoji.")
async def fingerguns_hello(ctx):
    guild = discord.utils.get(bot.guilds, name=GUILD)
    fingerguns = discord.utils.get(guild.emojis, name="fingerguns")
    await ctx.send(f"<:{fingerguns.name}:{fingerguns.id}>")

@bot.command(name="motivate", help="Responds with a motivational quote.")
async def motivate(ctx):
    message = ""
    response = requests.get("https://zenquotes.io/api/random")
    if response.status_code == 200:
        quote = response.json()
        message =quote[0]['q']
        author = quote[0]['a']
        if message.startswith("Too many requests."):
            await ctx.send("The Zenquotes API is overloaded. Please wait 30 seconds before trying again.")
        else:
            embedQuote = discord.Embed(title="Motivational Quotes", type="rich", url="https://zenquotes.io/")
            embedQuote.color = discord.Color.from_rgb(52, 29, 105)
            embedQuote.set_thumbnail(url="https://user-images.githubusercontent.com/42954045/102170926-49b47f80-3e4a-11eb-929b-eed606a70399.png") \
                      .add_field(name='Quote:',value="_" + message + "_", inline=False) \
                      .add_field(name='Author:', value=author, inline=False) \
                      .set_footer(text="Quotes provided by ZenQuotes", icon_url=bot.user.avatar_url)
            await ctx.send(embed=embedQuote)
    else:
        await ctx.send("An unknown error occurred. Please try again later.")

bot.run(TOKEN)