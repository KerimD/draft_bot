import uuid
import enum
import discord

from helper import clear_dm, format_tables

class Captain:
    def __init__(self, user: discord.User):
        self.id = user.id
        self.name = user.name
        self.dm_channel = user.dm_channel
        self.picks = [None, None, None]
        self.bans = [None, None]

    def pick(self, pick: str, pick_n: int) -> None:
        self.picks[pick_n] = pick

    def ban(self, ban: str, ban_n: int) -> None:
        self.bans[ban_n] = ban

CHAMP_LIST = [
    "alysia", "ashka", "bakko", "blossom", "croak", "destiny", "ezmo", "freya", 
    "iva", "jade", "jamila", "jumong", "lucie", "oldur", "pearl", "pestilus", 
    "poloma", "raigon", "rook", "ruh kaan", "shen rao", "shifu", "sirius",
    "taya", "thorn", "ulric", "varesh", "zander",
]
CHAMP_ALIAS_DICT = {
	"blos": "blossom", "pest": "pestilus", "dio": "pearl", 
	"ruh": "ruh kaan", "rk": "ruh kaan", "shen": "shen rao",
	"luke": "freya", "dest": "destiny", "pol": "poloma",
	"lucy": "lucie", "jam": "jamila", "jum": "jumong",
	"var": "varesh", "uni": "jumong", "frog": "croak",
    "polo": "poloma", "catchy": "thorn", "tomiy": "rook",
    "LDK": "bakko", "chisaku": "jade", "peon": "poloma",
    "averse": "taya", "arkdn": "rook", "mGalante": "rook"
}

unique_ids = []

class DraftState(enum.Enum):
    FIRST_BAN = 0
    FIRST_PICK = 1
    SECOND_PICK = 2
    SECOND_BAN = 3
    THIRD_PICK = 4
    COMPLETE = 5

class Draft:
    def __init__(self, user1: discord.User, user2: discord.User = None) -> None:

        # regenerate id until unique
        self.id = str(uuid.uuid1())[:6]
        while self.id in unique_ids:
            self.id = str(uuid.uuid1())[:6]
        unique_ids.append(self.id)

        self.state = DraftState.FIRST_BAN
        self.messages = []
        self.ihl_channel_id = 710901389232046080

        # init captains
        self.captain1 = Captain(user1)
        self.captain2 = Captain(user2) if user2 else None

        # init table
        empty_fields = '----\n----\n----\n\n----\n----'
        self.table = discord.Embed(color = 16753152)
        self.table.add_field(name = 'Captains', value = 'Picks\n\n\n\nBans')
        self.table.add_field(
            name = '**' + user1.name + '**',
            value = empty_fields
        )
        if user2:
            self.table.add_field(
                name = '**' + user2.name + '**',
                value = empty_fields
            )

    def add_captain(self, user: discord.User) -> None:
        self.captain2 = Captain(user)
        self.table.add_field(
            name = '**' + user.name + '**',
            value = '----\n----\n----\n\n----\n----'
        )

    def advance_state(self) -> None:
        if self.state == DraftState.FIRST_BAN:
            self.state = DraftState.FIRST_PICK
        elif self.state == DraftState.FIRST_PICK:
            self.state = DraftState.SECOND_PICK
        elif self.state == DraftState.SECOND_PICK:
            self.state = DraftState.SECOND_BAN
        elif self.state == DraftState.SECOND_BAN:
            self.state = DraftState.THIRD_PICK
        elif self.state == DraftState.THIRD_PICK:
            self.state = DraftState.COMPLETE

    def update_table(self, captain: Captain, champ: str) -> None:
        index = 1 if captain == self.captain1 else 2

        name = self.table.fields[index].name
        value = self.table.fields[index].value

        picks = []
        bans = []

        for pick in captain.picks:
            if pick:
                picks.append(pick.capitalize())
            else:
                picks.append('----')
        picks = '\n'.join(picks)

        for ban in captain.bans:
            if ban:
                bans.append(ban.capitalize())
            else:
                bans.append('----')
        bans = '\n'.join(bans)

        self.table.set_field_at(
            index = index,
            name = name,
            value = '\n\n'.join([picks, bans])
        )

    async def pick(self, author: discord.User, champ: str) -> bool:
        channel = author.dm_channel

        if champ in CHAMP_ALIAS_DICT:
            champ = CHAMP_ALIAS_DICT[champ]

        if champ not in CHAMP_LIST:
            await channel.send(champ + ' is not a valid champ.')
            return False

        if author.id == self.captain1.id:
            captain = self.captain1
            enemy_captain = self.captain2
            captain_num = 0
        else:
            captain = self.captain2
            enemy_captain = self.captain1
            captain_num = 1

        # checks for pickable champ
        if champ in enemy_captain.bans:
            await channel.send(
                champ.capitalize() + ' has been banned by the enemy team.'
            )
            return False
        elif champ in captain.picks:
            await channel.send(
                champ.capitalize() + ' has already been picked by your team.'
            )
            return False

        both_picked = False

        if self.state == DraftState.FIRST_PICK:
            if captain.picks[0]:
                await channel.send(
                    'Updated pick to ' + champ.capitalize()
                )
            captain.pick(champ, 0)
            if enemy_captain.picks[0]:
                both_picked = True
        elif self.state == DraftState.SECOND_PICK:
            if captain.picks[1]:
                await channel.send(
                    'Updated pick to ' + champ.capitalize()
                )
            captain.pick(champ, 1)
            if enemy_captain.picks[1]:
                both_picked = True
        else:
            if captain.picks[2]:
                await channel.send(
                    'Updated pick to ' + champ.capitalize()
                )
            captain.pick(champ, 2)
            if enemy_captain.picks[2]:
                both_picked = True

        champ = champ.capitalize()

        if both_picked:
            self.update_table(captain, champ)
            self.advance_state()
            return True

        self.update_table(captain, champ)
        await clear_dm(captain.dm_channel)
        tables = format_tables(self.table)
        await channel.send(embed = tables[captain_num])
        await channel.send('Waiting for opposing captain to pick.')
        return False

    async def ban(self, author: discord.User, champ: str) -> bool:
        channel = author.dm_channel

        if champ in CHAMP_ALIAS_DICT:
            champ = CHAMP_ALIAS_DICT[champ]

        if champ not in CHAMP_LIST:
            await channel.send(champ + ' is not a valid champ.')
            return False

        if author.id == self.captain1.id:
            captain = self.captain1
            enemy_captain = self.captain2
            captain_num = 0
        else:
            captain = self.captain2
            enemy_captain = self.captain1
            captain_num = 1

        # checks for banable champ
        if champ in enemy_captain.picks:
            await channel.send(
                champ.capitalize() + ' has already been picked by the enemy team.'
            )
            return False
        elif champ in captain.bans:
            await channel.send(
                champ.capitalize() + ' has already been banned by your team.'
            )
            return False

        both_banned = False

        if self.state == DraftState.FIRST_BAN:
            if captain.bans[0]:
                await channel.send(
                    'Updated ban to ' + champ.capitalize()
                )
            captain.ban(champ, 0)
            if enemy_captain.bans[0]:
                both_banned = True
        else:
            if captain.bans[1]:
                await channel.send(
                    'Updated ban to ' + champ.capitalize()
                )
            captain.ban(champ, 1)
            if enemy_captain.bans[1]:
                both_banned = True

        champ = champ.capitalize()

        if both_banned:
            self.update_table(captain, champ)
            self.advance_state()
            return True

        self.update_table(captain, champ)
        await clear_dm(captain.dm_channel)
        tables = format_tables(self.table)
        await channel.send(embed = tables[captain_num])
        await channel.send('Waiting for opposing captain to ban.')
        return False
