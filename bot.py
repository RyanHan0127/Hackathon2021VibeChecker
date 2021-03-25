import discord
import logging
import os
from dotenv import load_dotenv
from discord.ext import commands
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer as sia

load_dotenv()
BOT_PREFIX = ("!")
TOKEN = os.getenv('DISCORD_TOKEN')
MSG_LIMIT = 100
bot = commands.Bot(BOT_PREFIX)

@bot.command(name = 'vibecheck', pass_context=True)
async def vibecheck(ctx, *arg):
	amt = MSG_LIMIT
	if len(arg) == 1:
		amt = arg[0]
	current_channel_id = ctx.message.channel.id
	user_id = ctx.message.author.id
	channel = bot.get_channel(current_channel_id)
	messages = await ctx.channel.history(limit=amt).flatten()

	sentence = []
	for msg in messages:
		if msg.content != '!vibecheck' and msg.content != '':
			sentence.append(msg.content)
	#print(sentence)
	analyzer = sia()
	list_res = []
	for sen in sentence:
		vs = analyzer.polarity_scores(sen)
		sen_tuple = (sen, vs['compound'])
		list_res.append(sen_tuple)
	for i in list_res:
		print(i)
	#print(list_res)
	#await ctx.send("Vibe Check")

@bot.event
async def on_ready():
	print('Logged in as')
	print(bot.user.name)
	print(bot.user.id)
	print('------')

bot.run(TOKEN)