import discord

from draft import Draft

# Global Variables
SESSIONS = {}
CAPTAINS = {}

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

    # check arguments
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

    CAPTAINS[author.id] = draft
    draft.add_captain(author)
    await channel.send(embed = draft.table)

async def pick_champ(args, author):
    print(args, author)
    pass

async def ban_champ(args, author):
    print(args, author)
    pass

async def exit_draft(args, author):
    print(args, author)
    pass