import copy
import discord

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

async def init_draft(draft):
    tables = format_tables(draft.table)

    await draft.captain1.dm_channel.send(embed = tables[0])
    await draft.captain2.dm_channel.send(embed = tables[1])
