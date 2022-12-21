import os

from helpers import get_time
from pokemon_data import get_pmu_pokemon_data, get_recruitable_data, get_ability_data
from pokemon_api import pokemon, ability
import discord
from discord.ext import commands
from pytz import timezone
from dotenv import load_dotenv
from webserver import keep_alive

from datetime import datetime, timedelta

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


@bot.command(name='broken', help='Mock the best PMU bot in the world.')
async def bully(ctx):
	id = '<@' + str(ctx.message.author.id) + '>'
	gif = "https://c.tenor.com/vteeAE47mHgAAAAd/mihoyo-genshin.gif"
	response = "Stop it!" + id + " is broken!"
	await ctx.send(response)
	await ctx.send(gif)


@bot.command(name='hey', help='Say hi to the bot.')
async def hey(ctx):
	id = '<@' + str(ctx.message.author.id) + '>'
	response = "Hey " + id + ", did you know that in terms of male human and female Pokémon breeding, Vaporeon is the most compatible Pokémon for humans? Not only are they in the field egg group, which is mostly comprised of mammals, Vaporeon are an average of 3\"03' tall and 63.9 pounds. this means they're large enough to be able to handle human dicks, and with their impressive Base Stats for HP and access to Acid Armor, you can be rough with one. Due to their mostly water based biology, there's no doubt in my mind that an aroused Vaporeon would be incredibly wet, so wet that you could easily have sex with one for hours without getting sore. They can also learn the moves Attract, Baby-Doll Eyes, Captivate, Charm, and Tail Whip, along with not having fur to hide nipples, so it'd be incredibly easy for one to get you in the mood. With their abilities Water Absorb and Hydration, they can easily recover from fatigue with enough water. No other Pokémon comes close to this level of compatibility. Also, fun fact, if you pull out enough, you can make your Vaporeon turn white."
	gif = "https://i.kym-cdn.com/photos/images/newsfeed/001/017/359/6d2.gif"
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
async def timeshift(ctx, args=None, time="0"):
	if args == "-h":
		os.environ['TIMESHIFTED_H'] = time
	elif args == "-m":
		os.environ['TIMESHIFTED_M'] = time
	elif args == "-s":
		os.environ['TIMESHIFTED_S'] = time
	elif args == "clear":
		os.environ['TIMESHIFTED_H'] = "0"
		os.environ['TIMESHIFTED_M'] = "0"
		os.environ['TIMESHIFTED_S'] = "0"
		
	response = "The timeshift is " + os.getenv('TIMESHIFTED_H') + " hours, " + os.getenv('TIMESHIFTED_M') + " minutes and " + os.getenv('TIMESHIFTED_S') + " seconds."
	await ctx.send(response)


@bot.command(name='pmu', aliases=['get'], help='Where to get pokemon in PMU game.')
async def pmu(ctx, *argv):
	res = get_pmu_pokemon_data(" ".join(argv))
	response = str(res)
	await ctx.send(response)


@bot.command(name='pokemon', aliases=['pkm', 'p'], help='Show information about pokemon.')
async def get_pokemon(ctx, *argv):
	res = pokemon(" ".join(argv))
	response = str(res)
	await ctx.send(response)


@bot.command(name='ability', aliases=['abi', 'ab'], help='Show information about ability.')
async def get_ability(ctx, *argv):
	status, res = ability(" ".join(argv))
	response = res if status == 0 else res['effect']
	status, abi_pmu = get_ability_data(" ".join(argv))
	response = response + '\n\n*In PMU Game*: ' + (abi_pmu["Description"] if status == 1 else abi_pmu).replace("Ã©", "é")
	await ctx.send(response)


@bot.command(name='recruit', aliases=['rr'], help='Where to recruit pokemon in PMU game.')
async def get_retcruit(ctx, *argv):
	res = get_recruitable_data(" ".join(argv))
	response = str(res)
	await ctx.send(response)


@bot.command(name='map', help='Show PMU World Map.')
async def map(ctx, area=None):
	picture = discord.File("Data/Map/WorldMap.png")
	if area.lower() == "exbel":
		picture = discord.File("Data/Map/ExbelMap.png")
	elif area.lower() == "archford":
		picture = discord.File("Data/Map/ArchfordMap.png")
	elif area.lower() == "tanren":
		picture = discord.File("Data/Map/TanrenMap.png")
	elif area.lower() == "winden":
		picture = discord.File("Data/Map/WindenMap.png")
	elif area.lower() == "help":
		picture = discord.File("Data/Map/ReferenceMap.png")
	await ctx.send(file=picture)

	
@bot.event
async def on_ready():
	activity = discord.Game(name="Pokemon Mystery Universe", type=4)
	await bot.change_presence(status=discord.Status.online, activity=activity)

	print(f'{bot.user.name} has connected to Discord!')
	print(f'selfbot is ready!')

bot.run(TOKEN)
