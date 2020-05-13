import copy
import discord

from draft import Draft

# Global Variables
SESSIONS = {}
CAPTAINS = {}

BOT_ID = 709635454252613643
DRAFT_GUILD_ID = 709638020525064252
DRAFT_CHANNEL_ID = 709638103060447314

async def help_msg(args, author):
    await author.dm_channel.send(
        "`!help` : pull up this very dialog\n" \
        "`!draft` : start a draft\n" \
        "`!join [draft id]` : join a draft\n" \
        "`!ban [champ]` : during ban phase used to ban a champion\n" \
        "`!pick [champ]` : during pick phase used to pick a champion\n" \
        "`!exit` : exit the current draft you are in"
    )

async def start_draft(args, author):
    channel = author.dm_channel

    if args:
        await channel.send(
            'Too many arguments provided, try **just** `!draft`'
        )
        return

    if author.id in CAPTAINS:
        await channel.send(
            'You are already in a draft, exit with `!exit`'
        )
        return

    draft = Draft(author)
    CAPTAINS[author.id] = draft.id
    SESSIONS[draft.id] = draft

    await channel.send(
        'Share **Draft ID** with Opposing Captain\t>>>\t`' + draft.id + '`'
    )

async def join_draft(args, author):
    channel = author.dm_channel

    # if author.id in CAPTAINS:
    #     await channel.send(
    #         'You are already in a draft, exit with `!exit`'
    #     )
    #     return

    if len(args) < 1:
        await channel.send(
            'No draft id provided, try `!join [draft id]`'
        )
        return
    elif len(args) > 1:
        await channel.send(
            'Too many arguments provided, try `!join [draft id]`'
        )
        return

    if args[0] not in SESSIONS:
        await channel.send(
            args[0] + ' is not a valid draft id.'
        )
        return
    
    draft = SESSIONS[args[0]]

    if draft.captain2:
        await channel.send(
            'This draft already has two captains.'
        )
        return

    CAPTAINS[author.id] = draft.id
    draft.add_captain(author)

    tables = format_tables(draft.table)

    await draft.captain1.dm_channel.send(embed = tables[0])
    await draft.captain2.dm_channel.send(embed = tables[1])

async def pick_champ(args, author):
    print(args, author)
    pass

async def ban_champ(args, author):
    print(args, author)
    pass

async def exit_draft(args, author):
    channel = author.dm_channel

    if args:
        await channel.send(
            'Too many arguments provided, try **just** `!exit`'
        )
        return

    if author.id not in CAPTAINS:
        await channel.send(
            'You are not in a draft, start a draft with `!draft`'
        )
        return

    draft = SESSIONS[CAPTAINS[author.id]]
    draft_id = SESSIONS[CAPTAINS[author.id]].id

    await clear_dms(draft)

    if draft.captain1:
        await draft.captain1.dm_channel.send(
            'Exiting draft.'
        )
        del CAPTAINS[draft.captain1.id]
    if draft.captain2:
        await draft.captain2.dm_channel.send(
            'Exiting draft.'
        )
        del CAPTAINS[draft.captain2.id]

    del SESSIONS[draft_id]

async def clear_dms(draft):
    async for message in draft.captain1.dm_channel.history():
        if message.author.id == BOT_ID:
            if message.embeds:
                if message.embeds[0].color.value == 16753152:
                    await message.delete()
            else:
                await message.delete()

    if draft.captain2:
        async for message in draft.captain2.dm_channel.history():
            if message.author.id == BOT_ID:
                if message.embeds:
                    if message.embeds[0].color.value == 16753152:
                        await message.delete()
            else:
                await message.delete()

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