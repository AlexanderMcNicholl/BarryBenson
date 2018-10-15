from discord.ext.commands import Bot
from itertools import cycle
import random
import discord
from discord.utils import get
import numpy as np
import asyncio
import threading
import logging
import random
import time
from get_wow_data import get_data, get_json_info
from settings import WOW_API_KEY, TOKEN
import json
from constants import get_race, get_class, get_class_color
import os

song = 'songs.txt'
BOT_PREFIX = "$"
vote_count = 5
client = Bot(command_prefix=BOT_PREFIX)

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

@client.event
async def on_message(message):
	with open('members.json', 'r') as f:
		users = json.load(f)
	await update_json(users, message.author)
	await add_exp(users, message.author, 5)
	await update_level(users, message.author, message.channel)
	with open('members.json', 'w') as f:
		json.dump(users, f)
	client.process_commands(message)

async def get_logs_from(channel):
	f = open("tdata.txt", "a")
	async for m in client.logs_from(channel):
		f.write(m.clean_content + '\n')

@client.event
async def on_member_join(member):
	with open('members.json', 'r') as f:
		users = json.load(f)
	await update_json(users, member)
	with open('members.json', 'w') as f:
		json.dump(users, f)

async def update_json(users, user):
	if not user.id in users:
		users[user.id] = {}
		current_user = users[user.id]
		current_user['level'] = 1
		current_user['experience'] = 0

async def add_exp(users, user, exp):
	current_user = users[user.id]
	current_user['experience'] += exp

async def update_level(users, user, channel):
	current_user = users[user.id]
	experience = current_user['experience']
	level_start = current_user['level']
	end_level = int(experience ** (1/4))
	if level_start < end_level:
		current_user['level'] = end_level
		if end_level <= 2:
			await client.send_message(channel, 'O SHIT NIGGA, {} JUST BAMBOOZLED HIS WAY INTO {}.'.format(user.mention, end_level))
		elif end_level > 2 and end_level < 5:
			await client.send_message(channel, "Fuck, we got ourselfs a big boi here. Lil old dumb cunt {} has reached level {}. What a little bitch".format(user.mention, end_level))
		elif end_level >= 5:
			await client.send_message(channel, "Ok, the dumb cunt known as {} thinks its funny to send messages a bunch. Well WOOPTY DOO. NOBODY GIVES AN OUNCE OF A SHIT YOU WORTHLESS CUNT, BURN AND FUCK RIGHT OFF. {} isn't even that high anyway. pussy.".format(user.mention, end_level))


@client.event
async def on_reaction_add(reaction, user):
	message = reaction.message
	channel = message.channel
	if not user == client.user:
		if reaction.emoji == '✅':
			await client.send_message(channel, "{} Voted Yes".format(user.name))
		elif reaction.emoji == '❎':
			await client.send_message(channel, "{} Voted No".format(user.name))
		else:
			return

@client.command(pass_context=True, name='poll')
async def user_poll(ctx, *msg):
	message = " ".join(msg)
	embed = discord.Embed(title="Poll", description=message, color=0xc842f4)
	embed.add_field(name="Vote", value="Use Reactions to vote for: {}".format(message), inline=False)
	bot_message = await client.say(embed=embed)
	await client.add_reaction(bot_message, "✅")
	await client.add_reaction(bot_message, "❎")

@client.command(pass_context=True, name='stat')
async def get_character_info(ctx, *msg):
	await client.say("Fetching character information for {}".format(msg[0]))
	if len(msg) > 1:
		realm = msg[1]
	else:
		realm = "khazgoroth"
	data = get_data(msg[0], realm)
	if len(data) == 0:
		embed = discord.Embed(title="Error", description="O shit boi, aint no character wit dat name", color=0x00ff00)
		embed.add_field(name="Incorrect Player Name", value="Error 404: Bad URL, Character {} not found".format(msg[0]), inline=True)
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
		embed.add_field(name="Incorrect Player Name", value="Error 404: Bad URL, Character {} not found".format(msg[0]), inline=True)
		embed.set_thumbnail(url="https://i.pinimg.com/236x/b8/f6/77/b8f677570e6edb5aabd5d75ddf563e05--koala-bears-baby-koala.jpg")
		await client.say(embed=embed)
		return
	icon_image = "http://render-us.worldofwarcraft.com/character/{}".format(data['thumbnail'])
	professions = get_json_info("https://us.api.battle.net/wow/character/{}/{}?fields=professions&locale=en_US&apikey={}".format(realm, msg[0], WOW_API_KEY))
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

@client.command(pass_context=True, name='auc')
async def get_auction_house_data(ctx, *msg):
	item = msg[0]
	print("Searching for {}".format(int(item)))
	# if len(msg[1]) > 0:
	# 	realm = msg[1]
	# else:
	realm = "Khazgoroth"
	await client.say("Loading {} from {}...".format(item, realm))
	url = "https://us.api.battle.net/wow/auction/data/{}?locale=en_US&apikey={}".format(realm, WOW_API_KEY)
	return_data = get_json_info(url)
	auction_data = get_json_info(return_data["files"][0]["url"])
	test_item = None
	for i in auction_data['auctions']:
		if int(i['item']) == int(item):
			test_item = i
			await client.say("Item Found!")
			break
	if test_item == None:
		await client.say("Item Not Found on Auction House")
		return
	item_retrieval = get_json_info("https://us.api.battle.net/wow/item/{}?locale=en_US&apikey={}".format(test_item['item'], WOW_API_KEY))
	item_icon = "https://wow.zamimg.com/images/wow/icons/large/{}.jpg".format(item_retrieval['icon'])
	embed = discord.Embed(title="Auction Item", description=item_retrieval["name"], color=0x4259f4)
	embed.add_field(name="Owner", value=test_item['owner'], inline=False)
	if not item_retrieval['description'] == "":
		embed.add_field(name="Description", value=item_retrieval['description'], inline=False)
	embed.add_field(name="Price", value="{} Bid\n{} Buyout\nP.S. It obviously isn't a bizillion dollars for this trash but I cant figure what these numbers mean. It is a JSON element called 'bid' and 'buyout' so it has something to do with the price.".format(test_item["bid"], test_item["buyout"]), inline=False)
	embed.add_field(name="Amount", value=test_item['quantity'], inline=False)
	embed.add_field(name="Time Left", value=test_item["timeLeft"], inline=False)
	embed.set_thumbnail(url=item_icon)
	await client.say(embed=embed)

@client.command(pass_context=True, name='p')
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

@client.command(pass_context=True, name='pm')
async def change_playing_message(ctx, *msg):
	await client.change_presence(game=discord.Game(name=" ".join(msg)))

@client.event
async def on_ready():
	await client.change_presence(game=discord.Game(name='With My Large Wang.'))
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')

client.run(TOKEN)
# https://discordapp.com/oauth2/authorize?&client_id=486395215859679265&scope=bot&permissions=0
