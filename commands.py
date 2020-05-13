import discord

from draft import Draft, DraftState
from helper import init_draft

# Global Variables
SESSIONS = {}
CAPTAINS = {}

BOT_ID = 709635454252613643
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

    await channel.send(
        draft.pick(author, ' '.join(args))
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

    await channel.send(
        draft.ban(author, ' '.join(args))
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
