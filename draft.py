import discord

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
        captain1 = Captain(user1)
        captain2 = Captain(user2) if user2 else None
