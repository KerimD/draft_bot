import uuid
import discord

from errors import *

class Captain:
    def __init__(self, user: discord.User):
        self.id = user.id
        self.name = user.name
        self.dm_channel = user.dm_channel
        self.picks = [None, None, None]
        self.bans = [None, None]

    def pick(self, pick, pick_n):
        self.picks[pick_n] = pick
    
    def ban(self, ban, ban_n):
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
    "polo": "poloma"
}

unique_ids = []

class DraftState(Enum):
    FIRST_BAN = 0
    FIRST_PICK = 1
    SECOND_PICK = 2
    SECOND_BAN = 3
    THIRD_PICK = 4
    COMPLETE = 5

class Draft:
    def __init__(self, user1: discord.User, user2: discord.User = None) -> None:

        # regenerate id until unique
        while self.id in unique_ids:
            self.id = str(uuid.uuid1())[:6]
        unique_ids.append(self.id)

        self.state = DraftState.FIRST_BAN
        self.message = None

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

    def pick(self, author: discord.User, champ: str) -> str:
        if champ in CHAMP_ALIAS_DICT:
            champ = CHAMP_ALIAS_DICT[champ]

        if champ not in CHAMP_LIST:
            raise InvalidChampion(champ + ' is not a valid champ.')

        switch (self.state) {
            case 1:
                pass
            case 2:
                pass
            case 4:
                pass
            default:
                raise WrongPhase(
                    'You are not currently picking, try `!ban [champ]`'
                )
        }

    def ban(self, author: discord.User, champ: str) -> None:
        if champ in CHAMP_ALIAS_DICT:
            champ = CHAMP_ALIAS_DICT[champ]

        if champ not in CHAMP_LIST:
            raise InvalidChampion(champ + ' is not a valid champ.')

        switch (self.state) {
            case 0:
            pass
            case 3:
                pass
            default:
                raise WrongPhase(
                    'You are not currently banning, try `!pick [champ]`'
                )
        }
