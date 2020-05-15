import discord

from draft import Draft, DraftState
from helper import init_draft, format_tables, clear_dms, update_draft_channel

# Global Variables
SESSIONS = {}
CAPTAINS = {}

DRAFT_GUILD_ID = [709638020525064252]

async def help_msg(args, author, client):
    await author.dm_channel.send(
        "`!help` : pull up this very dialog\n" \
        "`!draft` : start a draft\n" \
        "`!join [draft id]` : join a draft\n" \
        "`!ban [champ]` : during ban phase used to ban a champion\n" \
        "`!pick [champ]` : during pick phase used to pick a champion\n" \
        "`!exit` : exit the current draft you are in"
    )

async def start_draft(args, author, client):
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

async def join_draft(args, author, client):
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

    await init_draft(draft, client)

async def pick_champ(args, author, client):
    channel = author.dm_channel

    if author.id not in CAPTAINS:
        await channel.send(
            'You are not in a draft, start a draft with `!draft`'
        )
        return

    draft = SESSIONS[CAPTAINS[author.id]]

    if not draft.captain2:
        await channel.send(
            'Another captain needs to join the draft, send them the draft id\t>>>\t`'
            + draft.id + '`'
        )
        return

    if not args:
        await channel.send(
            'You did not specify a champ, try `!pick [champ]`'
        )
        return

    if draft.state != DraftState.FIRST_PICK and \
       draft.state != DraftState.SECOND_PICK and \
       draft.state != DraftState.THIRD_PICK:
        await channel.send(
            'You are not currently picking, try `!ban [champ]`'
        )
        return

    if not await draft.pick(author, ' '.join(args)):
        return

    if draft.state == DraftState.COMPLETE:
        draft.table.color = 3210243

    tables = format_tables(draft.table)
    await clear_dms(draft)

    await draft.captain1.dm_channel.send(
        embed = tables[0]
    )
    await draft.captain2.dm_channel.send(
        embed = tables[1]
    )

    await update_draft_channel(draft, client)

    if draft.state == DraftState.COMPLETE:
        await exit_draft([], author, client)
    else:
        if draft.state == DraftState.SECOND_PICK:
            await draft.captain1.dm_channel.send(
                'Pick phase, please **pick** with `!pick [champ]`'
            )
            await draft.captain2.dm_channel.send(
                'Pick phase, please **pick** with `!pick [champ]`'
            )
        else:
            await draft.captain1.dm_channel.send(
                'Ban phase, please **ban** with `!ban [champ]`'
            )
            await draft.captain2.dm_channel.send(
                'Ban phase, please **ban** with `!ban [champ]`'
            )

async def ban_champ(args, author, client):
    channel = author.dm_channel

    if author.id not in CAPTAINS:
        await channel.send(
            'You are not in a draft, start a draft with `!draft`'
        )
        return

    draft = SESSIONS[CAPTAINS[author.id]]

    if not draft.captain2:
        await channel.send(
            'Another captain needs to join the draft, send them the draft id\t>>>\t`'
            + draft.id + '`'
        )
        return

    if not args:
        await channel.send(
            'You did not specify a champ, try `!ban [champ]`'
        )
        return

    if draft.state != DraftState.FIRST_BAN and \
       draft.state != DraftState.SECOND_BAN:
        await channel.send(
            'You are not currently banning, try `!pick [champ]`'
        )
        return

    if not await draft.ban(author, ' '.join(args)):
        return

    tables = format_tables(draft.table)
    await clear_dms(draft)

    await draft.captain1.dm_channel.send(
        embed = tables[0]
    )
    await draft.captain2.dm_channel.send(
        embed = tables[1]
    )

    await update_draft_channel(draft, client)

    await draft.captain1.dm_channel.send(
        'Pick phase, please **pick** with `!pick [champ]`'
    )
    await draft.captain2.dm_channel.send(
        'Pick phase, please **pick** with `!pick [champ]`'
    )

async def exit_draft(args, author, client):
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
