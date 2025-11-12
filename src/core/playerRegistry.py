import random

class PlayerRegistry:
	def __init__(self):
		self._MAX_PLAYERS = 99
		self.IdToName = {}
		self._NamesList = self._NamesList = [
			# ! Names MUST NOT contain spaces
			# Real Madrid
			"DiStefano", "Puskas", "Zidane", "Figo", "Raul", "Mbappe", "Ramos",
			"Carlos", "Marcelo", "Kroos", "Modric", "Benzema", "Bellingham", "Vinicius",
			"Rodrygo", "Courtois",

			# Barcelona
			"Cruyff", "Maradona", "Koeman", "Guardiola", "Rivaldo", "Ronaldinho", "Xavi",
			"Iniesta", "Busquets", "Puyol", "Pique", "Neymar", "Lewandowski", "Pedri",

			# Manchester City
			"Bell", "Summerbee", "Trautmann", "Kompany", "Aguero", "Silva", "Toure",
			"Foden", "DeBruyne", "Haaland", "Ederson", "RubenDias",

			# Liverpool
			"Dalglish", "Rush", "Barnes", "Fowler", "Carragher", "Gerrard", "Alonso",
			"VanDijk", "Alisson", "Salah",

			# Man Utd
			"Charlton", "Best", "Law", "Cantona", "Giggs", "Scholes", "Keane", "Beckham",
			"Rooney", "Schmeichel", "Vidic", "Ferdinand", "Casemiro", "Fernandes",

			# Bayern Munich
			"Beckenbauer", "Muller", "Kahn", "Matthaus", "Schweinsteiger", "Lahm", "Robben", "Ribery",
			"Lewandowski", "Kimmich", "Musiala", "Neuer", "Kane",

			# Paris SG
			"Doue", "Donaruma", "Hakimi", "Cavani", "Verratti", "Marquinhos", "Vitinha",

			# Sparta Praha
			"Nedved", "Rosicky", "Zeleny", "Birmancevic", "Lafata", "Blazek",
			"Haraslin", "Kuchta", "Rrahmani", "Vindahl",

			# Other
			"Pele", "Messi", "Ronaldo", "Platini", "Baggio", "Maldini", "Baresi",
			"Totti", "Zanetti", "Saka", "Son"
		]

		# Create a shuffled copy of the names to be used for assignment.
		self._availableNames = list(self._NamesList)
		random.shuffle(self._availableNames)

	def getNameById(self, playerId: int) -> str:
		if playerId in self.IdToName:
			return self.IdToName[playerId]

		# If the ID is new, assign a name.
		if self._availableNames:
			newName = self._availableNames.pop()
			self.IdToName[playerId] = newName
			return newName
		else:
			# If we've run out of predefined names, create a generic one.
			# But this should never happen...
			genericName = f"Player_{playerId}"
			self.IdToName[playerId] = genericName
			return genericName
