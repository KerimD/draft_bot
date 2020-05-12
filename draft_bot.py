import discord

client = discord.Client()

@client.event
async def on_ready():
	print('Bot Online')

@client.event
async def on_message(message):
	if message.author == client.user:
		return

	await message.channel.send('Potato')

with open("token.secret", "r") as f:
	token = f.read()

client.run(token)
