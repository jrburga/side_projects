from vgengine.game import *
from vgengine.systems.graphics import *
from cbd.system import SystemABC, ComponentABC

from collections import defaultdict

class CellsSystemComponent(ComponentABC):
	name = 'cells_system'

class CellsSystem(SystemABC):
	name = 'cells_system'
	component_type = CellsSystemComponent

class CellsSystem2D(CellsSystem):
	
	def __init__(self, spt=1, *args, **kwargs):
		super(CellsSystem2D, self).__init__(*args, **kwargs)
		self._time = 0
		self.spt = spt
		self.cell_dict = {}

	@property
	def cells(self):
		return self._components

	def update(self, dt=0, *args, **kwargs):
		self._time = (self._time + dt)
		if self._time >= self.spt:
			self.tick()
			self._time = 0

	def tick(self):
		dead_dict = defaultdict(lambda : defaultdict(lambda : 0))

		to_die = []
		to_live = []
		for x in self.cell_dict.keys():
			for y, cell in self.cell_dict[x].iteritems():
				if cell:
					live, dead = self.get_neighbors(x, y)
					if len(live) < 2 or len(live) > 3:
						to_die.append((x, y))
						#dies
					elif len(live) >= 2 and len(live) <= 3:
						#lives
						pass
					for _x, _y in dead:
						dead_dict[_x][_y] += 1

		for x, y in to_die:
			self.remove(self.cell_dict[x][y])

		for x in dead_dict.keys():
			for y, count in dead_dict[x].iteritems():
				if count == 3:
					new_cell = Cell2D(pos=(x, y))
					self.add(new_cell)
					#bring to life

	def __remove_cell(self, cell):
		x, y = cell.position
		if x in self.cell_dict:
			if y in self.cell_dict[x]:
				del self.cell_dict[x][y]
				if len(self.cell_dict[x]) == 0:
					del self.cell_dict[x]
					return
		assert False, "(%d, %d)" % (x ,y)

	def remove(self, *cells):
		super(CellsSystem2D, self).remove(*cells)
		for cell in cells:
			self.__remove_cell(cell)

	def __add_cell(self, cell):
		x, y = cell.position
		if x in self.cell_dict:
			if y in self.cell_dict[x]:
				assert self.cell_dict[x][y] == None
		else:
			self.cell_dict[x] = {}
		self.cell_dict[x][y] = cell

	def add(self, *cells):
		super(CellsSystem2D, self).add(*cells)
		for cell in cells:
			self.__add_cell(cell)

	def get_cell(self, x, y):
		if x in self.cell_dict:
			if y in self.cell_dict[x]:
				return self.cell_dict[x][y]
		return None

	def get_neighbors(self, x, y):
		live = []
		dead = []
		for _x in [x-1, x, x+1]:
			for _y in [y-1, y, y+1]:
				if _x != x or _y != y:
					if self.get_cell(_x, _y):
						live.append((_x, _y))
					else:
						dead.append((_x, _y))
		return live, dead

class Cell2D(CellsSystemComponent):
	name = 'cell'

	def __init__(self, pos=(0, 0), *args, **kwargs):
		super(Cell2D, self).__init__(*args, **kwargs)
		self._pos = pos

	@property
	def position(self):
		return self._pos

	def init(self, *args, **kwargs):
		pass

	def quit(self, *args, **kwargs):
		pass

if __name__ == '__main__':
	pass

	# def quit(scene, event):
	# 	print 'quiting scene'
	# 	scene.game.quit()

	# def escape(scene, event):
	# 	if event.key == control.Keyboard.K_ESCAPE:
	# 		scene.game.quit()

	# def debug(scene, event):
	# 	print 'debugging'
	# 	if event.key == control.Keyboard.K_SPACE:
	# 		print 'space key pressed'
	# 		for go in scene.game_objects:
	# 			print go

	# def on_click(scene, event):
	# 	if event.button == 1:
	# 		print event.pos

	# scene = Scene(
	# 	graphics.Graphics2D((400, 400)),
	# 	CellsSystem2D(spt=1)
	# 	)

	# cell_gen = GameObject()

	# cell_gen.add(
	# 	Cell2D(pos=(100, 100))
	# 	)

	# scene.add_event_handler('quit', quit)
	# scene.add_event_handler('keydown', escape)
	# scene.add_event_handler('keydown', debug)
	# scene.add_event_handler('click', on_click)

	# game = Game()
	# scene.add(cell_gen)
	# game.add(scene)
	# display = Graphics2D.create_display((400, 400))
	# game.run(display=display, fps=60)

