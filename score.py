class User(object):
	def __init__(self, name, id, keywords, numberOfLineChanges):
		self.id = id
		self.name = name
		self.keywords = keywords
		self.numberOfLineChanges = numberOfLineChanges
		self.score = 0

def scoreUser(userKeywords, taskKeywords, numberOfLineChanges):
	sharedElementCount = len(set(taskKeywords).intersection(userKeywords))
	return sharedElementCount * 0.8 + numberOfLineChanges * 0.2

def scoreUsers(users, taskKeywords):
	max = 0

	for user in users:
		score_calculated = scoreUser(user.keywords, taskKeywords, user.numberOfLineChanges)

		if score_calculated > max:
			max = score_calculated

		p#rint(user.id, ": ", score_calculated)

		user.score = score_calculated

	for user in users:
		user.score = user.score / max


arya = User("arya", "arya.vohra04", ["bwwitch", "wbitch", "bitcwh", "bitch"], 256)
taichi = User("taichi", "tkato0909", ["bww4itch", "w22bitch", "bitcwh", "bitc1h"], 377)
users = [arya, taichi]


scoreUsers(users, ["bwwitch", "wbitch", "we", "e"])
print(arya.name, arya.score)
print(taichi.name, taichi.score)

# print(scoreUser(["bwwitch", "wbitch", "bitcwh", "bitch"], ["bwwitch", "wbitch", "we", "e"], 5))