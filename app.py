import nextcord as discord
from nextcord.ext import commands, tasks

import json

from os import getenv
from dotenv.main import load_dotenv

import api


load_dotenv()

bot = commands.Bot(command_prefix="!", description="Receive a random word definition in your DM, everyday!")
api = api.Api(api_key=getenv('dicolink_apikey'))

@bot.event
async def on_ready():
	print(f"[ {bot.user.name}#{bot.user.discriminator} is ready ]")


@bot.event
async def on_message(msg):
	if msg.author.bot: return
	if msg.guild: return


	if msg.content in ["subscribe", "sub", "register", "start"]:
		#register msg.author
		with open('subscribers.list', 'r') as f:
			subs = json.load(f)
		
		if msg.author.id in subs:
			await msg.reply("> ❌ Unable to subscribe: You are already subscribed.")
			return

		subs.append(msg.author.id)

		with open('subscribers.list', 'w') as f:
			subs = json.dump(subs, f, indent=2)

		await msg.reply("> ✅ You successfully subscribed!")


	elif msg.content in ["unsubscribe", "unsub", "signout", "stop"]:
		#cancel msg.author
		with open('subscribers.list', 'r') as f:
			subs = json.load(f)
		
		if not msg.author.id in subs:
			await msg.reply("> ❌ Unable to unsubscribe: You are not subscribed.")
			return

		subs.remove(msg.author.id)

		with open('subscribers.list', 'w') as f:
			subs = json.dump(subs, f, indent=2)

		await msg.reply("> ✅ You successfully unsubscribed!")


	else:
		await msg.add_reaction("❔")


@bot.event
async def on_raw_reaction_add(payload):
	# Send help msg
	if payload.guild_id: return

	if payload.emoji.name == "❔":
		u = await bot.fetch_user(payload.user_id)
		await u.send("This bot let you subscribe to daily random word definitions.\nHere is how to subscribe/unsubscribe:\n\n\t- Send `subscribe` to the bot to subscribe\n\t- Send `unsubscribe` to the bot to unsubscribe\n\t- React with `❔` to a message to receive this message")


@bot.event
async def on_guild_join(guild):
	# Send a msg to everyone #ad (think to delay for big servers)
	pass


@tasks.loop(hours=24)
async def send_word_def():
	with open('subscribers.list', 'r') as f:
		subs = json.load(f)

	word = api.get_random_word()
	wdef = api.get_word_definition(word)

	for sub in subs:
		u = await bot.fetch_user(sub)
		await u.send(f"{word}:\n{wdef}")



@send_word_def.before_loop
async def before__send_word_def():
	await bot.wait_until_ready()

send_word_def.start()


bot.run(getenv('token'))