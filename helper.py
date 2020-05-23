import discord

DRAFT_CHANNEL_IDS = [
    709879064596447264,  # euil
    712809357988986980,  # nail
    709638103060447314,  # dev
    713178215321174057   # dio
]
BOT_ID = 709635454252613643

def format_tables(table):
    tables = [
        discord.Embed(color = table.color),
        discord.Embed(color = table.color)
    ]

    for i in range(len(table.fields)):
        for T in tables:
            T.add_field(
                name = table.fields[i].name,
                value = table.fields[i].value
            )

    # format table 1
    tables[0].set_field_at(
        index = 1,
        name = '**You**',
        value = table.fields[1].value
    )

    # format table 2
    tables[1].set_field_at(
        index = 1,
        name = '**You**',
        value = table.fields[2].value
    )
    tables[1].set_field_at(
        index = 2,
        name = table.fields[1].name,
        value = table.fields[1].value
    )

    return tables

async def init_draft(draft, client):
    tables = format_tables(draft.table)

    await draft.captain1.dm_channel.send(embed = tables[0])
    await draft.captain1.dm_channel.send(
        'Ban phase, please **ban** with `!ban [champ]`'
    )
    await draft.captain2.dm_channel.send(embed = tables[1])
    await draft.captain2.dm_channel.send(
        'Ban phase, please **ban** with `!ban [champ]`'
    )

    for channel in get_channels(client):
        draft.messages.append((await channel.send(embed = draft.table)).id)

def get_channels(client):
    channels = []

    for channel_id in DRAFT_CHANNEL_IDS:
        channels.append(client.get_channel(channel_id))

    return channels

async def update_draft_channel(draft, client):
    for channel_id in DRAFT_CHANNEL_IDS:
        async for message in client.get_channel(channel_id).history():
            if message.embeds:
                for message_id in draft.messages:
                    if message.id == message_id:
                        await message.edit(embed = draft.table)
                        break

async def clear_draft_channel(messages, client):
    for channel_id in DRAFT_CHANNEL_IDS:
        async for message in client.get_channel(channel_id).history():
            if message.embeds:
                for message_id in messages:
                    if message.id == message_id:
                        if message.embeds[0].color.value == 16753152:
                            await message.delete()
                        break

async def clear_dms(draft):
    count = 0
    if draft.captain1:
        async for message in draft.captain1.dm_channel.history():
            if count > 20:
                break
            count += 1

            if message.author.id == BOT_ID:
                if message.embeds:
                    if message.embeds[0].color.value == 16753152:
                        await message.delete()
                else:
                    await message.delete()

    count = 0
    if draft.captain2:
        async for message in draft.captain2.dm_channel.history():
            if count > 20:
                break
            count += 1

            if message.author.id == BOT_ID:
                if message.embeds:
                    if message.embeds[0].color.value == 16753152:
                        await message.delete()
                else:
                    await message.delete()

async def clear_dm(dm_channel):
    count = 0

    async for message in dm_channel.history():
        if count > 6:
            break
        count += 1

        if message.author.id == BOT_ID:
            if message.embeds:
                if message.embeds[0].color.value == 16753152:
                    await message.delete()
            else:
                await message.delete()
