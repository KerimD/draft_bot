import copy
import discord

DRAFT_CHANNEL_IDS = [709638103060447314, 710076783227174973]

def format_tables(table):
    tables = [copy.deepcopy(table), copy.deepcopy(table)]

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
    await draft.captain2.dm_channel.send(embed = tables[1])

    for channel in get_channels(client):
        draft.message = await channel.send(embed = draft.table)

def get_channels(client):
    channels = []

    for channel_id in DRAFT_CHANNEL_IDS:
        channels.append(client.get_channel(channel_id))

    return channels
