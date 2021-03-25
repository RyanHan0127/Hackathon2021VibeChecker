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
	if len(arg) > 1:
		await ctx.send("Incorrect number of arguments: 0 or 1")
		return

	isMention = False
	isInteger = False
	isChannel = False
	if len(arg) == 0:
		pass
	elif ctx.message.mentions:
		print("Is a mention")
		isMention = True
	elif ctx.message.channel_mentions:
		print("Is a channel mention")
		isChannel = True
	else:
		try:
			amt = int(arg[0])
			isInteger = True
		except ValueError:
			isInteger = False
		if isInteger:
			print("Is an integer")
		else:
			print("Not an integer")
			await ctx.send("Argument passed was not an integer, mention, or channel")
			return

	current_channel_id = ctx.message.channel.id
	user_id = ctx.message.author.id
	if isChannel:
		channel = bot.get_channel(ctx.message.channel_mentions[0])
	else:
		channel = bot.get_channel(current_channel_id)
	messages = await channel.history(limit=amt).flatten()

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