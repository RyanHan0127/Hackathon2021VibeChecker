import discord
import logging
import os
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
BOT_PREFIX = ("!")
TOKEN = os.getenv('DISCORD_TOKEN')
MSG_LIMIT = 100
bot = commands.Bot(BOT_PREFIX)

@bot.command(name = 'vibecheck', pass_context=True)
async def vibecheck(ctx, arg):

    amt = 100      #Default/placeholder, idk if we want to do a mention-based one as well but w/e I added error checking for it anyway
    isValid = true
    if not ctx.message.mentions:
        print("Is not a mention")
        try:
            amt = int(arg)
        except ValueError:
            isValid = False
        if not isValid:
            print("Not an integer")
            await ctx.send("Argument passed was not an integer or a mention")
            return
        else:
            print("Is an integer")
    else:
        #Check for the first message sent by mentioned user in an arbitrary time period and adjust amt accordingly
        #or something idk
        print("Is a mention")


	current_channel_id = ctx.message.channel.id
	user_id = ctx.message.author.id
	print(user_id)
	channel = bot.get_channel(current_channel_id)
	messages = await ctx.channel.history(limit=arg).flatten()

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