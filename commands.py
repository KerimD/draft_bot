import discord

from draft import Draft

async def help_msg(args, author):
    await author.dm_channel.send(
        "`!help` : pull up this very dialog\n" \
        "`!draft` : start a draft\n" \
        "`!join [draft id]` : join a draft\n" \
        "`!ban [champ]` : during ban phase used to ban a champion\n" \
        "`!pick [champ]` : during pick phase used to pick a champion\n" \
        "`!exit` : exit the current draft you are in"
    )
    pass

async def start_draft(args, author):
    print(args, author)
    pass

async def join_draft(args, author):
    print(args, author)
    pass

async def pick_champ(args, author):
    print(args, author)
    pass

async def ban_champ(args, author):
    print(args, author)
    pass

async def exit_draft(args, author):
    print(args, author)
    pass