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
	def height(self):
		return self._size[1]

	@property
	def w(self):
		return self.width

	@property
	def h(self):
		return self.height

	@property
	def left(self):
		return self.x

	@property
	def top(self):
		return self.y + self.height

	@property
	def right(self):
		return self.x + self.width

	@property
	def bottom(self):
		return self.y

	def __repr__(self):
		return '<Rect %r %r>' % (self._position, self._size)

class RectTree(object):

	def __init__(self):
		self._children = []
		self._parent = None

		self._cached_position = None
		self._cached_size = None
		self._is_dirty = None

	def _recache_parameters(self):
		self._cached_position = None
		self._cached_size = None
		if self._children:
			x = self.left
			y = self.bottom
			w = self.right - x
			h = self.top - y
			if x != None and y != None and w != None and h != None:
				self._cached_position = (x, y)
				self._cached_size = (w, h)

	def add(self, *rects):
		for rect in rects:
			self._add_rect(rect);
		self._recache_parameters()

	def _add_rect(self, rect):
		if hasattr(rect, 'parent'):
			if rect._parent == self:
				return
			if rect._parent:
				rect._parent.remove(rect)
			rect._parent = self

		self._children.append(rect)

	def remove(self, *rects):
		for rect in rects:
			self._remove_rect(rect)
		self._recache_parameters()

	def _remove_rect(self, rect):
		try:
			self._children.remove(rect)
		except ValueError:
			raise ValueError("rect %r not in tree" % rect)

		if hasattr(rect, 'parent'):
			rect._parent = None

	@property
	def parent(self):
		return self._parent

	@property
	def children(self):
		return self._children

	@property
	def left(self):
		if self._cached_position and self._cached_size:
			return self._cached_position[0]
		if self._children:
			return min(self._children, key=lambda rect: rect.left).left

	@property
	def right(self):
		if self._cached_position and self._cached_size:
			return self._cached_position[0] + self._cached_size[0]
		if self._children:
			return max(self._children, key=lambda rect: rect.right).right

	@property
	def top(self):
		if self._cached_position and self._cached_size:
			return self._cached_position[1] + self._cached_size[1]
		if self._children:
			return max(self._children, key=lambda rect: rect.top).top

	@property
	def bottom(self):
		if self._cached_position and self._cached_size:
			return self._cached_position[1]
		if self._children:
			return min(self._children, key=lambda rect: rect.bottom).bottom

	@property
	def size(self):
		return self._cached_size

	@property
	def position(self):
		return self._cached_position

	@property
	def x(self):
		if self._cached_position:
			return self._cached_position[0]

	@property
	def y(self):
		if self._cached_position:
			return self._cached_position[1]

	@property
	def width(self):
		if self._cached_size:
			return self._cached_size[0]

	@property
	def height(self):
		if self._cached_size:
			return self._cached_size[1]

	@property
	def w(self):
		return self.width

	@property
	def h(self):
		return self.height

	def __repr__(self):
		if self.position and self.size:
			return "<RectTree %r %r : %r>" % (self.position, self.size, self._children)
		return "<RectTree %r>" % (self._children)

if __name__ == '__main__':
	cr = Rect((0, 0), (10, 10))

	print min([cr], key=lambda x: x.x)

	rt = RectTree()
	rt2 = RectTree()
	rt.add(cr)
	rt2.add(cr)
	rt.add(rt2)
	print rt


