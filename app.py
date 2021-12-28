import nextcord as discord
from nextcord.ext import commands

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


bot.run(getenv('token'))