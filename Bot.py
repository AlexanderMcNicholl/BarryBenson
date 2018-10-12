from discord.ext.commands import Bot
from itertools import cycle
import random
import discord
import numpy as np
import asyncio
import threading
import logging
import random
import time
from get_wow_data import get_data, get_json_info
from settings import WOW_API_KEY
import json
from constants import get_race, get_class, get_class_color

filename = 'quotes.txt'
song = 'songs.txt'

BOT_PREFIX = "$"

selections = [
	'No', 'All of the time',
	'Maybe next time', 'VenOMMMMMMM',
	'I don\'t know', 'Definitely',
	'As sure as an unplugged toaster',
	'FUCK YEAH!',
	'Damn straight cunt',
	'Not in six million Jews',
	'Highly disagree',
	'I really couldn\'t give a fuck',
	'maybe I don\'t care'
]

blacklist = "blacklist.txt"

client = Bot(command_prefix=BOT_PREFIX)

TOKEN = 'NDg2Mzk1MjE1ODU5Njc5MjY1.DpYMDA.yNi3WCOTofVzbQbHCxSS6lvZYbk'

async def get_logs_from(channel):
	f = open("tdata.txt", "a")
	async for m in client.logs_from(channel):
		f.write(m.clean_content + '\n')

@client.command(pass_context=True, name='stat')
async def get_character_info(ctx, *msg):
	await client.say("Fetching character information for {}".format(msg[0]))
	if len(msg) > 1:
		realm = msg[1]
	else:
		realm = "khazgoroth"
	data = get_data(msg[0], realm)
	if len(data) == 0:
		embed.set_thumbnail(url="https://i.pinimg.com/236x/b8/f6/77/b8f677570e6edb5aabd5d75ddf563e05--koala-bears-baby-koala.jpg")
		await client.say(embed=embed)
		return
	icon_image = "http://render-us.worldofwarcraft.com/character/{}".format(data['thumbnail'].replace('avatar', 'main'))
	color = get_class_color(data['class'])
	embed = discord.Embed(title="Name", description=data['name'], color=color)
	embed.add_field(name="Level", value=data['level'], inline=True)
	embed.add_field(name="Realm", value=data['realm'], inline=True)
	embed.add_field(name="Race", value=get_race(data['race']), inline=True)
	embed.add_field(name="Class", value=get_class(data['class']), inline=True)
	embed.add_field(name="Honorable Kills", value=data['totalHonorableKills'], inline=True)
	embed.add_field(name="Achievement Points", value=data['achievementPoints'], inline=True)
	if data['faction'] == 0:
		embed.set_thumbnail(url="https://cdn0.iconfinder.com/data/icons/world-of-warcraft-wow-faction-and-class/199/Alliance-512.png")
	elif data['faction'] == 1:
		embed.set_thumbnail(url="https://cdn4.iconfinder.com/data/icons/smashicons-game-flat/60/41_-_For_the_Horde_Flat-512.png")
	embed.set_image(url=icon_image)
	await client.say(embed=embed)

@client.command(pass_context=True, name='prof')
async def get_character_professions(ctx, *msg):
	await client.say("Fetching profession information for {}".format(msg[0]))
	if len(msg) > 1:
		realm = msg[1]
	else:
		realm = "khazgoroth"
	data = get_data(msg[0], realm)
	if len(data) == 0:
		embed = discord.Embed(title="Error", description="O shit boi, aint no character wit dat name", color=0x00ff00)
		embed.add_field(name="Incorrect Player Name", value="Error 404: Bad URL, Character {} not found".format(msg), inline=True)
		embed.set_thumbnail(url="https://i.pinimg.com/236x/b8/f6/77/b8f677570e6edb5aabd5d75ddf563e05--koala-bears-baby-koala.jpg")
		await client.say(embed=embed)
		return
	icon_image = "http://render-us.worldofwarcraft.com/character/{}".format(data['thumbnail'])
	professions = get_json_info("https://us.api.battle.net/wow/character/{}/{}?fields=professions&locale=en_US&apikey=7q2yab7gha6jfdzj7tca472bnyvs3x9h".format(realm, msg))
	primary = professions["professions"]["primary"]
	secondary = professions["professions"]["secondary"]
	color = get_class_color(data['class'])
	embed = discord.Embed(title="Professions", description=professions['name'], color=color)
	prof_sec = []
	if len(primary) == 0:
		embed.add_field(name="Primary Professions", value="None", inline=False)
	else:
		for x in primary:
			n = x['name']
			txt = '{}/{} - {}\n'.format(x['rank'], x['max'], x['name'])
			prof_sec.append(txt)
		embed.add_field(name="Primary Professions", value=(''.join(prof_sec)), inline=False)
	prof_sec = []
	if len(secondary) == 0:
		embed.add_field(name="Secondary Professions", value="None", inline=False)
	else:
		for x in secondary:
			n = x['name']
			txt = '{}/{} - {}\n'.format(x['rank'], x['max'], x['name'])
			prof_sec.append(txt)
		embed.add_field(name="Secondary Professions", value=(''.join(prof_sec)), inline=False)
	embed.set_thumbnail(url=icon_image)
	await client.say(embed=embed)

@client.command(pass_context=True, name='newquote')
async def add_quote(ctx, msg):
	txt = ctx.message.content.replace('$newquote ', '')
	f = open(filename, "a")
	f.write(txt)
	f.write("\n")
	await client.say('quote saved.')
	f.close()

@client.command(pass_context=True, name='addsong')
async def add_song(ctx, msg):
	txt = ctx.message.content.replace('$addsong ', '')
	f = open(song, "a")
	f.write(txt)
	f.write("\n")
	await client.say('song saved.')
	f.close()

@client.command(pass_context=True, name='quote')
async def choose_quote(ctx):
	quotes = []
	fh = open(filename)
	while True:
	    line = fh.readline()
	    if not line or line == '':
	        break
	    quotes.append(line)
	fh.close()
	quote = random.choice(quotes)
	await client.send_message(ctx.message.channel, quote, tts=True)

@client.command(pass_context=True, name='playsong')
async def play_song(ctx):
	songs = []
	fh = open(song)
	while True:
	    line = fh.readline()
	    if not line or line == '':
	        break
	    songs.append(line)
	fh.close()
	chosen_song = random.choice(songs)
	author = ctx.message.author
	voice_channel = author.voice_channel
	vc = await client.join_voice_channel(voice_channel)
	player = await vc.create_ytdl_player(chosen_song)
	player.start()
	await client.say("Song played.")

@client.command(pass_context=True, name='8ball')
async def magic_eight_ball(ctx, msg):
	await client.send_message(ctx.message.channel, random.choice(selections), tts=True)

@client.event
async def on_ready():
	await client.change_presence(game=discord.Game(name='With My Large Wang.'))
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')

client.run(TOKEN)
