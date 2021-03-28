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

# Vibecheck Command implementation starts here
# Takes one argument per field
# Non-integer, mention, or channel mention arguments are ignored
#    - "!vibecheck [NUMBER OF MESSAGES] [MENTION] [CHANNEL]"
#    - "!vibecheck": default options are 100 messages, all users, current channel
@bot.command(name = 'vibecheck', pass_context=True)
async def vibecheck(ctx, *arg):
	
	amt = MSG_LIMIT

	# Error checking
	# Refactored to allow multiple arguments

	has_mention = False
	has_integer = False
	has_channel = False
	many_ints = False

	mentions = ctx.message.mentions
	channel_mentions = ctx.message.channel_mentions

	# Check if mention exists and there is only 1
	if mentions:
		if len(mentions) > 1:
			await ctx.send("Incorrect number of mentions: 1 maximum")
			return
		print("Has a mention")
		has_mention = True

	# Check if channel mention exists and there is only 1
	if channel_mentions:
		if len(channel_mentions) > 1:
			await ctx.send("Incorrect number of channel mentions: 1 maximum")
			return
		print("Has a channel mention")
		has_channel = True
	
	# Check if integer exists and there is only 1
	for a in arg:
		try:
			amt = int(a)
			if has_integer:
				many_ints = True
				break
			has_integer = True
		except ValueError:
			pass
	if many_ints:
		print("Has too many integers")
		await ctx.send("Incorrect number of integers: 1 maximum")
		return
	elif has_integer:
		print("Has an integer")

	# The bot needs to know which channel the author input
    # the command to in order to do the sentiment analysis
	current_channel_id = ctx.message.channel.id

	# Change channel to analyze if option exists
	if has_channel:
		channel = ctx.message.channel_mentions[0]
	else:
		channel = bot.get_channel(current_channel_id)

	messages = await channel.history().flatten()

	# Grab all the sentences that do not
    # contain the command and empty strings
	# Check for mentioned user if needed as well
	sentence = []
	count_sen = 0
	for msg in messages:
		str_url_removed = re.sub('http[s]?://\S+', '', msg.content, flags=re.MULTILINE) # Remove urls
		str_mention_removed = re.sub('<@![0-9]+>', '', str_url_removed, flags=re.MULTILINE) # Remove mentions
		str_channel_removed = re.sub('<#[0-9]+>', '', str_mention_removed, flags=re.MULTILINE) # Remove channel
		if msg.author.id != bot.user.id and not '!vibecheck' in str_channel_removed and str_channel_removed != '':
			sentence.append(str_channel_removed)
			count_sen += 1
		if has_mention and mentions[0].id == msg.author.id:
			sentence.append(str_channel_removed)
			count_sen += 1
		if count_sen == amt:
			break
	# Analysis starts here
	analyzer = sia()
	list_res = []
	# Only can analyze one sentence at a time
	# list_res gives messages from most to least recent
	for sen in sentence:
		vs = analyzer.polarity_scores(sen)
		list_res.append(vs['compound'])
	# Getting the weighted average of compound scores and plotting with our created plot.py
	list_arr = np.array(list_res)
	reg_mean = mean = float(np.mean(list_arr))
	for spot,value in enumerate(list_arr):
		if list_arr[spot] < -0.1:
			list_arr[spot] = -1
		elif list_arr[spot] > 0.1:
			list_arr[spot] = 1
		else:
			list_arr[spot] = 0
	list_arr[spot] = value*((amt-spot)/amt)
	mean = float(np.mean(list_arr))
	png = plot.plot(mean)

	reg_pct = (reg_mean + 1) / 2 * 100
	pct = (mean + 1) / 2 * 100

	# Compare regular mean with weighted mean
	print(reg_pct)
	print(pct)

	# Create return string, send it and the plot
	content_str = "The last " + str(amt) + " messages in " + channel.mention
	if has_mention:
		content_str += " from " + mentions[0].mention
	content_str += " had " + str(round(pct,2)) + "% good vibes, here's the graph:"
	await ctx.send(content=content_str, file=discord.File(png))
	os.remove(png)

@bot.event
async def on_ready():
	print('Logged in as')
	print(bot.user.name)
	print(bot.user.id)
	print('------')

bot.run(TOKEN)
