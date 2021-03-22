import discord
import logging
import os
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
BOT_PREFIX = ("!")
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(BOT_PREFIX)

@bot.command(name = 'vibecheck', pass_context=True)
async def vibecheck(ctx, *arg):
	current_channel_id = ctx.message.channel.id
	user_id = ctx.message.author.id
	print(user_id)
	channel = bot.get_channel(current_channel_id)
	messages = await ctx.channel.history(limit=200).flatten()

	for msg in messages:
		if msg.author.id == user_id:
			print(msg.content + " : " + msg.created_at.strftime("%d/%m/%Y, %H:%M:%S"))
	#await ctx.send("Vibe Check")

@bot.event
async def on_ready():
	print('Logged in as')
	print(bot.user.name)
	print(bot.user.id)
	print('------')

bot.run(TOKEN)