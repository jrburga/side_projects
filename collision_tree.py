class Rect(object):

	def __init__(self, position, size):
		self._size = size
		self._position = position

	@property
	def size(self):
		return self._size

	@property
	def position(self):
		return self._position

	@property
	def x(self):
		return self._position[0]

	@property
	def y(self):
		return self._position[1]

	@property
	def width(self):
		return self._size[0]

	@property
	def w(self):
		return self._size[0]

	@property
	def height(self):
		return self._size[1]

	@property
	def h(self):
		return self._size[1]

if __name__ == '__main__':
	cr = Rect()

	print cr