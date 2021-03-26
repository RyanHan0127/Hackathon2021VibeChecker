import discord 
import logging
import os
from dotenv import load_dotenv #For hiding token
from discord.ext import commands
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer as sia #Sentiment API

load_dotenv()
BOT_PREFIX = ("!") 
TOKEN = os.getenv('DISCORD_TOKEN')
MSG_LIMIT = 100
bot = commands.Bot(BOT_PREFIX) #Creating the bot with the prefix

#Vibecheck Command implementation starts here
#Takes zero to one arguement
#    - "!vibecheck": Do an analysis of the first 100 messages
#    - "!vibecheck n": Do an analysis of the first n messages. n must be an integer.
@bot.command(name = 'vibecheck', pass_context=True) 
async def vibecheck(ctx, *arg):
	amt = MSG_LIMIT
	if len(arg) > 1: #Checking the number of arguments
		await ctx.send("Incorrect number of arguments: 0 or 1")
		return

	#Argument handling checker. Needs to be an integer, and not mentions, channel, or any other string
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

	#The bot needs to look at which channel did the author inputted the command
	#to do the sentiment analysis
	current_channel_id = ctx.message.channel.id
	user_id = ctx.message.author.id
	if isChannel:
		channel = ctx.message.channel_mentions[0]
	else:
		channel = bot.get_channel(current_channel_id)
	messages = await channel.history(limit=amt).flatten() #Grabbing the first (amt) messages

	#Grab all the sentences that does not contain the command and empty strings
	sentence = []
	for msg in messages:
		if not '!vibecheck' in msg.content and msg.content != '':
			sentence.append(msg.content)

	#Analysis starts here
	analyzer = sia()
	list_res = []
	#Only one sentence at a time can do the analysis
	for sen in sentence:
		vs = analyzer.polarity_scores(sen)
		sen_tuple = (sen, vs['compound'])
		list_res.append(sen_tuple)
	#Printing the result of the analysis. We care about the compound score.
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