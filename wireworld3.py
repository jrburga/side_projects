from enum import IntEnum
from collections import namedtuple

class CellType(IntEnum):
	TAIL      = -1
	CONDUCTOR =  0
	HEAD_1    =  1
	HEAD_2    =  2

class Map2D(object):

	point = namedtuple('point', 'x, y')
	point.__new__.func_defaults = (-1, ) * len(point._fields)
	class Element2D(object):
		def __init__(self, entry, x, y):
			self.entry = entry
			self.point = Map2D.point(x, y)

	def __init__(self):
		self._dim = 100
		self._base_array = [[] for x in xrange(self._dim * self._dim)]

	def __getitem__(self, (x, y)):
		index = self.__pos_to_index(x, y)
		for elem in self._base_array[index]:
			if elem.point == (x, y):
				return elem.entry
		return None

	def __setitem__(self, (x, y), value):
		index = self.__pos_to_index(x, y)
		entry_index = -1
		for elem in self._base_array[index]:
			elem.entry = value
			return
		self._base_array[index] += [Map2D.Element2D(value, x, y)]

	def iterrange(self, start, end):
		try:
			x1, y1 = self.__check_range(start)
			x2, y2 = self.__check_range(end)
		except ValueError:
			raise ValueError

		for x in range(x1, x2):
			for y in range(y1, y2):
				yield self[x, y]

	def __pos_to_index(self, x, y):
		return (y * self._dim + x) % (self._dim * self._dim)

	def __check_range(self, range_point):
		if type(range_point) is int:
			return (range_point, range_point)
		elif (type(range_point) is tuple and len(range_point) == 2):
			return range_point
		else:
			raise ValueError, "Start and end must be of same type"

if __name__ == '__main__':
	map2d = Map2D()
	map2d[0, 0] = 1
	for elem in map2d.iterrange(0, (1, 2)):
		print elem
