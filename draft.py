import discord
import uuid

class Captain:
    def __init__(self, user: discord.member.Member):
        self.id = user.id
        self.name = user.name
        self.picks = [None, None, None]
        self.bans = [None, None]

    def pick(self, pick, pick_n):
        self.picks[pick_n] = pick
    
    def ban(self, ban, ban_n):
        self.bans[ban_n] = ban

class Draft:
    def __init__(self,
                 user1: discord.member.Member,
                 user2: discord.member.Member = None) -> None:

        self.id = str(uuid.uuid1())[:6]

        # init captains
        self.captain1 = Captain(user1)
        self.captain2 = Captain(user2) if user2 else None

        # init table
        empty_fields = '----\n----\n----\n\n----\n----'
        self.table = discord.Embed(color = 16753152)
        self.table.add_field(name = 'Captains', value = 'Picks\n\n\n\nBans')
        self.table.add_field(name = '**' + user1.name + '**', value = empty_fields)
        if user2:
            self.table.add_field(name = '**' + user2.name + '**', value = empty_fields)

    def add_captain(self, user: discord.member.Member) -> None:
        self.captain2 = Captain(user)
        self.table.add_field(
            name = '**' + user.name + '**',
            value = '----\n----\n----\n\n----\n----'
        )
