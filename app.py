import nextcord as discord
from nextcord.ext import commands, tasks

from os import getenv
from dotenv.main import load_dotenv

load_dotenv()

bot = commands.Bot(command_prefix="!", description="Receive a random word definition in your DM, everyday!")


@bot.event
async def on_ready():
	print(f"[ {bot.user.name}#{bot.user.discriminator} is ready ]")


@bot.event
async def on_message(msg):
	if msg.author.bot: return
	if msg.guild: return

	if msg.content in ["subscribe", "sub", "register", "start"]:
		#register msg.author
		pass

	elif msg.content in ["unsubscribe", "unsub", "signout", "stop"]:
		#cancel msg.author
		pass

	else:
		await msg.add_reaction("❔")


@bot.event
async def on_raw_reaction_add(payload):
	# Send help msg
	pass


@bot.event
async def on_guild_join(guild):
	# Send a msg to everyone (think to delay for big servers)
	pass


@tasks.loop(hours=24)
async def send_word_def():
	with open('subscribers.list', 'r') as f:
		subs = json.load(f)

	for sub in subs:
		u = await bot.fetch_user(sub)
		await u.send("hi")



@send_word_def.before_loop
async def before__send_word_def():
	await bot.wait_until_ready()

send_word_def.start()


bot.run(getenv('token'))