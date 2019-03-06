from enum import IntEnum
from collections import namedtuple

class CellType(IntEnum):
	EMPTY     = -2
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

		def __repr__(self):
			return "<%r : %r>" % (self.point, self.entry)

	def __init__(self):
		self._dim = 100
		self._base_array = [[] for x in xrange(self._dim * self._dim)]
		self._elems = []
		self.__dirty = False

	def __getitem__(self, (x, y)):
		index = self.__pos_to_index(x, y)
		for elem in self._base_array[index]:
			if elem.point == (x, y):
				return elem.entry
		return None

	def __setitem__(self, (x, y), value):
		index = self.__pos_to_index(x, y)
		for elem in self._base_array[index]:
			if elem.point == (x, y):
				elem.entry = value
				return
		new_elem = Map2D.Element2D(value, x, y)
		self._base_array[index] += [new_elem]
		self._elems += [new_elem]

	def __delitem__(self, (x, y)):
		index = self.__pos_to_index(x, y)
		elem = None
		for i in xrange(len(self._base_array[index])):
			if self._base_array[index][i].point == (x, y):
				elem = self._base_array[index][i]
				del self._base_array[index][i]
				break
		if elem:
			self._elems.remove(elem)
		else:
			raise KeyError, "(%i, %i)" % (x, y)

	def __len__(self):
		if self.__dirty:
			c = 0
			for elem in self.iteritems():
				c += 1
			return c
		else:
			return len(self._elems)

	def __iter__(self):
		for elem in self._elems:
			yield (elem.point, elem.entry)

	def reset(self):
		for (x, y), value in self:
			del self._base_array[self.__pos_to_index(x, y)][-1]
		for i in xrange(len(self._elems)):
			del self._elems[-1]

	def update(self, other_map):
		for (x, y), value in other_map:
			self[x, y] = value

	def iterkeys(self):
		for point, entry in self.__iter__():
			yield point

	def itervalues(self):
		for point, entry in self.__iter__():
			yield entry

	def iteritems(self):
		return self.__iter__()

	def iterrange(self, start, end):
		try:
			x1, y1 = self.__check_range(start)
			x2, y2 = self.__check_range(end)
		except ValueError, msg:
			raise ValueError, msg

		for y in xrange(y1, y2):
			for x in xrange(x1, x2):
				yield Map2D.point(x, y), self.__getitem__((x, y))

	def __pos_to_index(self, x, y):
		return (y * self._dim + x) % (self._dim * self._dim)

	def __check_range(self, range_point):
		if type(range_point) is int:
			return (range_point, range_point)
		elif (type(range_point) is tuple and len(range_point) == 2):
			return range_point
		else:
			raise ValueError, "start and end must be int or 2-tuple"

class WireWorld3(object):
	def __init__(self, init_map):
		self.map = None
		if init_map:
			self.map = init_map
		else:
			self.map = Map2D()
		self.next_map = Map2D()

	def step(self):
		self.next_map.reset()
		for (x, y), cell_type in self.map:
			if cell_type == CellType.EMPTY:
				continue
			elif cell_type == CellType.TAIL:
				self.next_map[x, y] = CellType.CONDUCTOR
				continue
			elif cell_type == CellType.HEAD_2:
				converted = False
				for (_x, _y), cell_type in self.map.iterrange((x-1, y-1), (x+2, y+2)):
					if _x == x and _y == y:
						continue
					if cell_type != None:
						if cell_type == CellType.HEAD_1:
							self.next_map[x, y] = CellType.HEAD_1
							converted = True
							continue
				if not converted:
					self.next_map[x, y] = CellType.TAIL
			elif cell_type == CellType.HEAD_1:
				self.next_map[x, y] = CellType.TAIL
			elif cell_type == CellType.CONDUCTOR:
				head1_count = 0 
				head2_count = 0
				for (_x, _y), cell_type in self.map.iterrange((x-1, y-1), (x+2, y+2)):
					if _x == x and _y == y:
						continue
					if cell_type != None:
						if cell_type == CellType.HEAD_1:
							head1_count += 1
						elif cell_type == CellType.HEAD_2:
							head2_count += 1
				if head1_count > 0 and head2_count <= head1_count:
					self.next_map[x, y] = CellType.HEAD_1
					continue
				elif head2_count > 0 and head1_count < head2_count:
					self.next_map[x, y] = CellType.HEAD_2
					continue

		self.map.update(self.next_map)

	def __repr__(self):
		min_x, max_x = float('inf'), -float('inf')
		min_y, max_y = float('inf'), -float('inf')
		for (x, y) in self.map.iterkeys():
			if x < min_x: min_x = x
			if x > max_x: max_x = x
			if y < min_y: min_y = y
			if y > max_y: max_y = y

		string = "=" * (max_x - min_x + 1) + "\n"
		_y = min_y
		for (x, y), cell_type in self.map.iterrange((min_x, min_y), (max_x+1, max_y+1)):
			if _y != y:
				string += '\n'
				_y = y
			if cell_type == CellType.EMPTY or cell_type == None:
				string += ' '
			if cell_type == CellType.CONDUCTOR:
				string += '0'
			if cell_type == CellType.HEAD_1:
				string += '+'
			if cell_type == CellType.HEAD_2:
				string += '-'
			if cell_type == CellType.TAIL:
				string += '.'
		return string


def StringToMap(string):
	string = string.strip()
	map2d = Map2D()
	x, y = 0, 0
	for c in string:
		if c == '\n':
			y += 1
			x = 0
			continue
		elif c == '.':
			map2d[x, y] = CellType.TAIL
		elif c == '+':
			map2d[x, y] = CellType.HEAD_1
		elif c == '-':
			map2d[x, y] = CellType.HEAD_2
		elif c == '0':
			map2d[x, y] = CellType.CONDUCTOR
		print c, x, y, map2d[x, y]
		x += 1
	return map2d

if __name__ == '__main__':
	mapString = """
00000+
000-
"""
	map2d = StringToMap(mapString)

	ww = WireWorld3(map2d)
	print ww
	for x in xrange(3):
		ww.step()
		print ww


