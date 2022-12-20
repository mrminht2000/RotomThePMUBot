import os

from helpers import get_time
from pokemon_data import get_pokemon_data
import discord
from discord.ext import commands
from pytz import timezone
from dotenv import load_dotenv
from webserver import keep_alive

from datetime import datetime, timedelta

keep_alive()

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

TIMEZONE_VN = timezone('Asia/Ho_Chi_Minh')
TIMEZONE_UTC = timezone("UTC")
os.environ['TIMESHIFTED_H'] = '0' if os.getenv('TIMESHIFTED_H') is None else os.getenv('TIMESHIFTED_H')
os.environ['TIMESHIFTED_M'] = '0' if os.getenv('TIMESHIFTED_M') is None else os.getenv('TIMESHIFTED_M')
os.environ['TIMESHIFTED_S'] = '0' if os.getenv('TIMESHIFTED_S') is None else os.getenv('TIMESHIFTED_S')

@bot.command(name='introduce', help='Rotom introduce himself')
async def introduce(ctx):
	response = "I am the best Pokemon Mystery Universe bot in the world uwu"
	await ctx.send(response)


@bot.command(name='ehe', help='What do you mean EHE?!?')
async def ehe(ctx):
	ehe_gif = "https://c.tenor.com/cZHoFqQEgwkAAAAM/paimon.gif"
	response = "EHE TE NANDAYO?!?"
	await ctx.send(response)
	await ctx.send(ehe_gif)


@bot.command(name='broken', help='Mock the best PMU bot in the world')
async def bully(ctx):
	id = '<@' + str(ctx.message.author.id) + '>'
	gif = "https://c.tenor.com/vteeAE47mHgAAAAd/mihoyo-genshin.gif"
	response = "Stop it!" + id + " is broken!"
	await ctx.send(response)
	await ctx.send(gif)


@bot.command(name='time', help='Check the time in PMU game')
async def time(ctx):
	current_time = datetime.now(TIMEZONE_UTC)
	ts_h = int(os.getenv('TIMESHIFTED_H'))
	ts_m = int(os.getenv('TIMESHIFTED_M'))
	ts_s = int(os.getenv('TIMESHIFTED_S'))
	time, td, next_time = get_time(current_time + timedelta(hours = ts_h, minutes = ts_m, seconds = ts_s))
	hours, minutes = td.seconds // 3600, td.seconds // 60 % 60
	seconds = td.seconds - hours*3600 - minutes*60
	response = "It is now " + time + ". It will be " + next_time + " in " + str(hours) + " hours, " + str(minutes) + " minutes and " + str(seconds) + " seconds."
	await ctx.send(response)


@bot.command(name='timeshift', help='Manually set the timeshift by choice. Use -h -m -s to choose type of time. Use <timeshift clear> to reset the timeshift.')
async def timeshift(ctx, command):
	commands = command.split()
	if commands[0] == "-h":
		os.environ['TIMESHIFTED_H'] = commands[1]
	elif commands[0] == "-m":
		os.environ['TIMESHIFTED_M'] = commands[1]
	elif commands[0] == "-s":
		os.environ['TIMESHIFTED_S'] = commands[1]
	elif commands[0] == "clear":
		os.environ['TIMESHIFTED_H'] = "0"
		os.environ['TIMESHIFTED_M'] = "0"
		os.environ['TIMESHIFTED_S'] = "0"
		
	response = "The timeshift is " + os.getenv('TIMESHIFTED_H') + " hours, " + os.getenv('TIMESHIFTED_M') + " minutes and " + os.getenv('TIMESHIFTED_S') + "seconds."
	await ctx.send(response)


@bot.command(name='pokemon', help='Where to get pokemon in PMU game.')
async def pokemon(ctx, name):
	res = get_pokemon_data(name)
	response = str(res)
	await ctx.send(response)

	
@bot.event
async def on_ready():
	activity = discord.Game(name="Pokemon Mystery Universe", type=4)
	await bot.change_presence(status=discord.Status.online, activity=activity)

	print(f'{bot.user.name} has connected to Discord!')
	print(f'selfbot is ready!')


keep_alive()
bot.run(TOKEN)
