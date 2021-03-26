import discord
import logging
import os
import re
import plot
import numpy as np
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
#    - "!vibecheck [NUMBER OF MESSAGES] [MENTION] [CHANNEL]"
@bot.command(name = 'vibecheck', pass_context=True)
async def vibecheck(ctx, *arg):
	
	amt = MSG_LIMIT

	#Error checking
	#Probably should refactor to allow multiple arguments

	hasMention = False
	hasInteger = False
	hasChannel = False
	manyInts = False

	mentions = ctx.message.mentions
	channel_mentions = ctx.message.channel_mentions

	#Check if mention exists and there is only 1
	if mentions:
		if len(mentions) > 1:
			await ctx.send("Incorrect number of mentions: 1 maximum")
			return
		print("Has a mention")
		hasMention = True

	#Check if channel mention exists and there is only 1
	if channel_mentions:
		if len(channel_mentions) > 1:
			await ctx.send("Incorrect number of channel mentions: 1 maximum")
			return
		print("Has a channel mention")
		hasChannel = True
	
	#Check if integer exists and there is only 1
	#Not working rn, trying to fix
	for a in arg:
		try:
			amt = int(a)
			if hasInteger:
				manyInts = True
				break
			hasInteger = True
		except ValueError:
			pass
	if manyInts:
		print("Has too many integers")
		await ctx.send("Incorrect number of integers: 1 maximum")
		return
	elif hasInteger:
		print("Has an integer")

	# The bot needs to know which channel the author input
        # the command to in order to do the sentiment analysis
	current_channel_id = ctx.message.channel.id
	user_id = ctx.message.author.id

	if hasChannel:
		channel = ctx.message.channel_mentions[0]
	else:
		channel = bot.get_channel(current_channel_id)

	history = channel.history()

	# need to fix this code block so it actually parses 
        # history for mentioned user's messages
	# or if not we can just remove the mention arg
	if hasMention:
		for message in history:
			if message.author.id == ctx.message.mentions[0].id:
				history.append(message)
	
	messages = await history.flatten()

	# Grab all the sentences that does not 
    # contain the command and empty strings
	sentence = []
	count_sen = 0
	for msg in messages:
		str_url_removed = re.sub('http[s]?://\S+', '', msg.content, flags=re.MULTILINE) #Remove urls
		str_mention_removed = re.sub('<@![0-9]+>', '', str_url_removed, flags=re.MULTILINE) #Remove mentions
		str_channel_removed = re.sub('<#[0-9]+>', '', str_mention_removed, flags=re.MULTILINE) #Remove channel
		if not '!vibecheck' in str_channel_removed and str_channel_removed != '':
			sentence.append(str_channel_removed)
			count_sen += 1
		if count_sen == amt:
			break
	print(sentence)

	#Analysis starts here
	analyzer = sia()
	list_res = []
	#Only one sentence at a time can do the analysis
	for sen in sentence:
		vs = analyzer.polarity_scores(sen)
		list_res.append(vs['compound'])
	#Getting the average of compound scores and plotting with our created plot.py
	mean = float(np.mean(np.array(list_res)))
	png = plot.plot(mean)
	pct = (mean + 1) / 2 * 100
	contentstr = "The last " + str(amt) + " messages had " + str(round(pct,2)) + "% good vibes, here's the graph:"
	await ctx.send(content=contentstr, file=discord.File(png))
	os.remove(png)

@bot.event
async def on_ready():
	print('Logged in as')
	print(bot.user.name)
	print(bot.user.id)
	print('------')

bot.run(TOKEN)