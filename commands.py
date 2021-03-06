import discord

from draft import Draft, DraftState
from helper import init_draft, format_tables, clear_dms, update_draft_channel, clear_draft_channel

# Global Variables
SESSIONS = {}
CAPTAINS = {}

NAIL_CHANNEL_ID = 712809437034709133
DRAFT_TO_MISC = {
    709879064596447264: 709879167419678730,  # euil
    712809357988986980: 712809437034709133,  # nail
    709638103060447314: 710901389232046080   # dev
}

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

    if author.id in CAPTAINS:
        await channel.send(
            'You are already in a draft, exit with `!exit`'
        )
        return

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
        await msg_ihl_bot(draft, client)
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
    draft_id = draft.id

    await clear_dms(draft)
    await clear_draft_channel(draft.messages, client)

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

async def init_ihl_draft(message, client):
    if message.channel.id not in DRAFT_TO_MISC:
        return

    await message.delete()

    content = message.content.split(',')
    guild = message.guild

    captain1 = guild.get_member(int(content[1]))
    captain2 = guild.get_member(int(content[2]))

    if not captain1.dm_channel:
        await captain1.create_dm()
    if not captain2.dm_channel:
        await captain2.create_dm()

    # check if already in a draft
    if captain1.id in CAPTAINS or captain2.id in CAPTAINS:
        await captain1.dm_channel.send(
            'Unable to create draft because one of the captains is already in a draft, exit with `!exit`'
        )
        await captain2.dm_channel.send(
            'Unable to create draft because one of the captains is already in a draft, exit with `!exit`'
        )
        return

    draft = Draft(captain1, captain2)
    draft.id = content[0]
    draft.ihl = True
    draft.ihl_channel_id = DRAFT_TO_MISC[message.channel.id]
    for champ in content[3:]:
        draft.banned_champs.append(champ.lower())

    CAPTAINS[int(content[1])] = draft.id
    CAPTAINS[int(content[2])] = draft.id
    SESSIONS[draft.id] = draft

    await init_draft(draft, client)

async def msg_ihl_bot(draft, client):
    if draft.ihl:
        channel = client.get_channel(draft.ihl_channel_id)
        draft_id = draft.id
    else:
        channel = client.get_channel(NAIL_CHANNEL_ID)
        draft_id = '0'

    message = [draft_id] + \
        draft.captain1.bans + \
        draft.captain2.bans + \
        draft.captain1.picks + \
        draft.captain2.picks

    await channel.send(','.join(message))
