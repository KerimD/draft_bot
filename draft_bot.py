import discord

from commands import *

client = discord.Client()

# Global Variables
COMMAND_PREFIX = '!'
DRAFT_CHANNEL_IDS = [709879064596447264, 709638103060447314, 698678134085779466]
IHL_BOT_IDS = [709917629669965876, 704663040682885134]
COMMANDS = {
    "!help": help_msg,
    "!draft": start_draft,
    "!join": join_draft,
    "!pick": pick_champ,
    "!ban": ban_champ,
    "!exit": exit_draft
}

@client.event
async def on_ready():
    # clean up draft channels
    messages = []

    for channel_id in DRAFT_CHANNEL_IDS:
        channel = client.get_channel(channel_id)

        async for message in channel.history():
            if message.author.id == client.user.id:
                if message.embeds:
                    if message.embeds[0].color.value == 16753152:
                        messages.append(message)
            else:
                messages.append(message)

        await channel.delete_messages(messages)

    print('Bot Online')

@client.event
async def on_message(message):
    if message.author.id in IHL_BOT_IDS:
        await init_ihl_draft(message, client)
        return

    if not await is_valid_message(message):
        return

    print(message.author, message.content)

    if not message.author.dm_channel:
        await message.author.create_dm()

    content = (message.content.strip().lower()).split()

    if content[0] in COMMANDS:
        await COMMANDS[content[0]](content[1:], message.author, client)
    else:
        await message.author.dm_channel.send(
            content[0] + ' is not recognized as a command, try `!help`.'
        )

@client.event
async def on_member_join(member):
    if member.dm_channel:
        return

    await member.create_dm()
    await member.dm_channel.send(
        'Welcome, to learn how to use this bot try `!help`'
    )

async def is_valid_message(message) -> bool:
    if message.author.bot:
        return False

    if not message.content:
        return False

    if type(message.channel) is discord.DMChannel:
        return True

    if message.channel.id in DRAFT_CHANNEL_IDS:
        await message.delete()
        return True
    else:
        return False

with open("token.secret", "r") as f:
    token = f.read()

client.run(token)
