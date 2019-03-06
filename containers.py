from itertools import izip

class Map2D(object):
	def __init__(self):
		self._rows = 100
		self._cols = 100
		self._base = [[] for _i in xrange(self._rows * self._cols)]

	def __getitem__(self, (x, y)):
		idx = self._get_idx((x, y))
		for value, pos in self._base[idx]:
			if pos == (x, y):
				return value
		return None

	def __setitem__(self, (x, y), value):
		idx = self._get_idx((x, y))
		switch_i = -1
		for i, (value, pos) in enumerate(self._base[idx]):
			if pos == (x, y):
				switch_i = i
				break

		self._base[idx].append(value)

	def _get_idx(self, (x, y)):
		return x + self._rows * y

class ArrayND(object):
	def __init__(self, *args):
		prod = 1
		for arg in args:
			assert type(arg) is int
			assert arg > 0
			prod *= arg
		self._dims = args
		self._base = [None] * prod

	@property
	def size(self):
		return self._dims

	@property
	def dimension(self):
		return len(self._dims)

	def _check(self, *keys):
		assert len(keys[0]) == self.dimension, "key: %i, dims: %i" % (len(keys), self.dimension)
		for key in keys[0]:
			assert type(key) is int
			assert key >= 0

	def _get_idx(self, *keys):
		idx = 0
		prod = 1
		for i, key in enumerate(keys[0]):
			idx += prod * key
			prod *= self._dims[i]
		return idx

	def __len__(self):
		return len(self._base)

	def __getitem__(self, *keys):
		self._check(*keys)
		for d, _d in izip(self._dims, keys[0]):
			if _d >= d:
				raise IndexError, "array index out of range"
		idx = self._get_idx(*keys)
		return self._base[idx]

		
	def __setitem__(self, *args):
		keys, value = args
		self._check(keys)
		for d, _d in izip(self._dims, keys):
			if _d >= d:
				raise IndexError, "array index out of range"

		idx = self._get_idx(keys)
		self._base[idx] = value

if __name__ == '__main__':
	map2d = Map2D()

	map2d[0, 1]
	map2d[1, 1]