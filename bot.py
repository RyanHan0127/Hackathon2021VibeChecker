import discord
import logging
from discord.ext import commands

TOKEN = "秘密です( ͡❛ ω ͡❛)"
BOT_PREFIX = ("!")

bot = commands.Bot(BOT_PREFIX)

@bot.command()
async def vibecheck(ctx, arg):
    pass
