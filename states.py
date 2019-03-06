class MapND(object):
	def __init__(self, dimensions=1):
		self._dims = dimensions

	def __getitem__(self, key):
		'''key: n-dimensional tuple'''
		print 'getting', key

	def __setitem__(self, key, value):
		'''key: n-dimensional tuple'''
		print 'setting', key, value

	def __delitem__(self, key):
		print 'deleting', key

	def __missing__(self, key):
		print 'missing', key

	def __len__(self):
		pass

	def iter(self, start, end):
		pass

if __name__ == '__main__':
	map2d = MapND(2)

	map2d[0, 2]
	map2d[1, 0] = 2
	map2d[(0, 0):(1, 0):-1]
	map2d[0:1]