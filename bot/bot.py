# bot.py
import os
import random
from dotenv import load_dotenv

# 1
import discord
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.default()
intents.members = True

# 2
bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name="hi", help="Responds with a fingerguns emoji.")
async def fingerguns_hello(ctx):
    guild = discord.utils.get(bot.guilds, name=GUILD)
    fingerguns = discord.utils.get(guild.emojis, name="fingerguns")
    await ctx.send(f"<:{fingerguns.name}:{fingerguns.id}>")

bot.run(TOKEN)