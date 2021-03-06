import itertools
import random


class Game:

	def __init__(self, cards=None):
		if not cards:
			self.cards = [self.random_card() for _ in xrange(12)]
		else:
			self.cards = cards

	def __repr__(self):
		return '\n'.join(str(card) for card in self.cards)

	def random_card(self):
		"""Return random tuple (color, shape, number, texture)"""
		return tuple(random.choice([1, 2, 3]) for _ in xrange(4))

	def is_set(self, x, y, z):
		"""Returns true if card trio is a set at every position based on sum mod 3,
		which is only 0 IFF all same or all different"""
		return sum(sum(i) % 3 for i in zip(x, y, z)) == 0

	def compare_all(self, idx=False):
		"""Compare all combinations of three cards,
		and return list of tuples of winning sets.
		If idx, also return corresponding list index of each card."""
		sets = []
		self.trios = itertools.combinations(enumerate(self.cards), 3)
		for x, y, z in self.trios:
			if self.is_set(x[1], y[1], z[1]):
				cards_idx = (x[0], y[0], z[0])
				if idx:
					sets.append(map(lambda x: (x, self.cards[x]), cards_idx))
				else:
					sets.append(map(lambda x: self.cards[x], cards_idx))
		return sets

	def play(self, idx=False):
		if len(self.cards) < 3:
			return False
		results = self.compare_all(idx)
		if results:
			return results
		return False


def test(n):
	return '{}%'.format(sum(Game().play() for _ in xrange(n)) / float(n) * 100.0)
