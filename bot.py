import discord
import logging
import os
import re
from dotenv import load_dotenv #For hiding token
from discord.ext import commands
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer as sia

load_dotenv()
BOT_PREFIX = ("!")
TOKEN = os.getenv('DISCORD_TOKEN')
MSG_LIMIT = 100
bot = commands.Bot(BOT_PREFIX)

#Vibecheck Command implementation starts here
#Takes zero to one arguement
#    - "!vibecheck": Do an analysis of the first 100 messages
#    - "!vibecheck n": Do an analysis of the first n messages.
#       n must be an integer.
@bot.command(name = 'vibecheck', pass_context=True)
async def vibecheck(ctx, *arg):
	
	amt = MSG_LIMIT

	#Error checking
	#Probably should refactor to allow multiple arguments
	if len(arg) > 3:
		await ctx.send("Incorrect number of arguments: format is \"!vibecheck [NUMBER OF MESSAGES] [MENTION] [CHANNEL]\", 3 max arguments")
		return

	isMention = False
	isInteger = False
	isChannel = False
	manyInts = False
	intError = False

	mentions = ctx.message.mentions
	channel_mentions = ctx.message.channel_mentions

	#Check if mention exists and there is only 1
	if mentions:
		if len(mentions) > 1:
			await ctx.send("Incorrect number of mentions: 1 maximum")
			return
		print("Has a mention")
		isMention = True

	#Check if channel mention exists and there is only 1
	if channel_mentions:
		if len(channel_mentions) > 1:
			await ctx.send("Incorrect number of channel mentions: 1 maximum")
			return
		print("Has a channel mention")
		isChannel = True
	
	#Check if integer exists and there is only 1
	#Not working rn, trying to fix
	try:
		for a in arg:
			b = str(a)
			c = commands.MemberConverter.convert(ctx,b)
			print(c)
			amt = int(a)
			if isInteger:
				manyInts = True
				break
			isInteger = True
	except ValueError:
		pass
	if manyInts:
		print("Has too many integers")
		await ctx.send("Argument passed was not an integer, mention, or channel")
		return
	elif isInteger:
		print("Has an integer")

	# The bot needs to know which channel the author input
        # the command to in order to do the sentiment analysis
	current_channel_id = ctx.message.channel.id
	user_id = ctx.message.author.id

	if isChannel:
		channel = ctx.message.channel_mentions[0]
	else:
		channel = bot.get_channel(current_channel_id)

	history = channel.history(limit=amt)

	# need to fix this code block so it actually parses 
        # history for mentioned user's messages
	# or if not we can just remove the mention arg
	if isMention:
		for message in history:
			if message.author.id == ctx.message.mentions[0].id:
				history.append(message)
	
	messages = await history.flatten()

	# Grab all the sentences that does not 
    # contain the command and empty strings
	sentence = []
	for msg in messages:
		str_url_removed = re.sub('http[s]?://\S+', '', msg.content, flags=re.MULTILINE) #Remove urls
		str_mention_removed = re.sub('<@![0-9]+>', '', str_url_removed, flags=re.MULTILINE) #Remove mentions
		str_channel_removed = re.sub('<#[0-9]+>', '', str_mention_removed, flags=re.MULTILINE) #Remove channel
		if not '!vibecheck' in str_channel_removed and str_channel_removed != '':
			sentence.append(str_channel_removed)

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

	#compile weighted average or whatever
	#it looks like list_res prints from most to least recent

	#graph w/ whatever Dylan wants here idk

	#await ctx.send("Vibe Check")

@bot.event
async def on_ready():
	print('Logged in as')
	print(bot.user.name)
	print(bot.user.id)
	print('------')

bot.run(TOKEN)
