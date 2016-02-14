# Now with comments!

import pygame
from math import sqrt
from math import sin, cos, pi

'''
Controls:

Click anywhere on the screen to place a new charge.
Press space to change the sign of the charge 
Press the + and - keys to increase the drawing scale
Press the up and down arrow keys to change how much you change the drawing scale when you press + and -
Press the Z key to undo last charge placement.
Press the C key to clear the screen
Press Escape to close the window (you can also just cilck the close button)

'''

size = 800 # screen width and height
scale = 100 # grid with and height
# Change these numbers changes screen size and the number of points needed to update.
# Note: number of points need to update is scale**2. (assuming spacing is 1)
# Be careful how big you make this number. This shit easily crashes.

l = 2
# This is an incrementing factor that you can change while running the code by pressing 
# up and down arrows keys. 
# Afterwords, when you push + or -, you will change the k factor
# which will change the strength of the E field around the points.
# This is mostly just to get a better image if the colors on the screen are all confusing.

k = 10
# "constant" (not actually constant)
d = 1
# That's a good question. I forgot what this letter was. 
# That's why you make more descriptive names....
# Oh, wait, i figured it out. It's used in point.E function: something/(r**(d+1))
# d = 1 is 1/r**2, d = 0: 1/r. And so on. It essentially changes the physics and
# the 1 over r**2 law. This is kind of important because we can only render in 
# Two dimensional space.

spacing = 1 
# Setting this to 2 would mean you would update every other point.
s = size/scale
# A single letter variable name that is just a ratio used when drawing things.
speed = 2
# This isn't actually used anywhere. I probably had plans to make these particles move,
# But it runs too slowly for that to be reasonable anymore.
charge_set = 1
# Everytime  you place a new charge, this determines whether it's positive or negative.
# You can press space to switch between positive or negative charges.

screen = pygame.display.set_mode([size]*2)

grid = [[0 for x in xrange(scale)] for y in xrange(scale)] 
# Initiates the grid of points 

class Point():
	def __init__(self, charge=1, pos=[0, 0]):
		self.c = charge
		self.p = pos
	def E(self, x, y, k, d):
		# Calculates the force of the E field for each point around all particles.
		px, py = self.p 
		dx = px - x
		dy = py - y
		r = (dx**2+dy**2)**(.5)
		if r != 0:
			F = self.c*k*255./(r**(d+1))
			return F*dx/r, F*dy/r
		return 0, 0

class Particle(pygame.sprite.Sprite):
	# Defines main class for each particle.
	# Setting it to a python Sprite object to take advantage of pygame methods
	# such as update and draw.
	# You can find how these work on the pygame wiki.

	def __init__(self, pos = [0, 0], mass = 1000, charge = 1, vel = [0, 0], acc = [0, 0]):
		pygame.sprite.Sprite.__init__(self)

		self.image = pygame.Surface([1, 1])
		self.image.fill((255, 255, 255))
		self.rect = self.image.get_rect()

		self.p = pos 	# Since this code is mostly physics,
		self.v = vel 	# I kind of got into the habit of using 
		self.a = acc 	# one letter variable names.
		self.m = mass 	# Probably not the best idea.
		self.c = charge # Alwell.
		self.rect.center = self.p
	def update(self, points, k, d): # Main calculations
		'''Apparently these particles actually have the ability to move
			I'm assuming the reason they don't is because it takes to much
			processing power and this code sucks, so it will run slowly.'''
		x, y = self.p
		fieldsx = []
		fieldsy = []
		for point in points:
			fx, fy = point.E(x, y, k, d)
			fieldsx.append(fx)
			fieldsy.append(fy)
		Fx = sum(fieldsx)
		Fy = sum(fieldsy)
		self.a[0] = Fx/self.m # Updates acceleration
		self.a[1] = Fy/self.m

		self.v[0] += self.a[0] # Updates velocity
		self.v[1] += self.a[1]

		self.p[0] += self.v[0]	# Updates position
		self.p[1] += self.v[1]
		self.p[0] %= size		# ??? 
		self.p[1] %= size		# Oh yea, this just makes it so that if it goes off the screen
								# It reappears at the other side of the screen. 
								# It's a wrap-around. That's why modular arithmatic is being used.

		self.rect.center = self.p 	# Updates rect position,
									# what the pygame sprite object
									# uses when calling the draw command
'''
points = []
R = 10
for r in xrange(0, R):
	for t in xrange(-5, 6):
		points.append(Point(1, [scale/2-r-r*cos(t*pi/10), scale/2-r*sin(t*pi/10)]))
particles = pygame.sprite.Group()
#particles.add(Particle([size/2, size/2]))

I think this code is suppodes to draw a circle of charges

You can write your own code in this area to place particels acurately.

Draw circles or lines, or any other geometry to demonstrate things like 
Gausses law, or how slow this code is.
'''
state_change = True

clock = pygame.time.Clock() # Contros frame rate
							# but not important in this case
							# because screen only updates on mouse click

run = True
while run: # Main loop. Lazy method.
	
	mx, my = pygame.mouse.get_pos() # sets mx and my to mouse position
	mx = (scale*mx)/size
	my = (scale*my)/size

	pygame.display.set_caption("("+str(mx)+", "+str(my)+")" + " : " + str(round(grid[my][mx], 3)))
	if k == 0: k = 1
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.display.quit()
			run = False
		if event.type == pygame.KEYDOWN:
			state_change = True
			if event.key == pygame.K_ESCAPE: # Quits
				pygame.display.quit()
				run = False
			if event.key == pygame.K_SPACE: # Inverts charge when placing
				charge_set *= -1 
			if event.key == pygame.K_c: # clears screen
				points = []
			if event.key == pygame.K_z: # clears last placement
				if len(points) > 0:
					last = points.pop()
			if event.key == pygame.K_PLUS or event.key == pygame.K_p: # Increases render scale
				k *= l
			if event.key == pygame.K_MINUS: # Decreases render scale
				if k > 2: 
					k /= l
			if event.key == pygame.K_UP: # Increases incrementation
				if l < 16: 
					l *= 2
			if event.key == pygame.K_DOWN: # Decreases incrementation
				if l > 2: 
					l /= 2
		if event.type == pygame.MOUSEBUTTONDOWN: # Places charge
			if mx > 0 and mx < size and my > 0 and my < size:
				points.append(Point(charge_set, [mx, my]))
				state_change = True
	if state_change: # Only updates if things have changed.
		screen.fill((0, 0, 0))
		for y in xrange(0, scale, spacing):
			for x in xrange(0, scale, spacing):
				fieldsx = []
				fieldsy = []
				for point in points:
					fx, fy = point.E(x, y, k, d)
					fieldsx.append(fx)
					fieldsy.append(fy)
				Fx = sum(fieldsx)
				Fy = sum(fieldsy)
				F = (Fx**2+Fy**2)**(.5)
				grid[y][x] = F
				pygame.draw.rect(screen, (0, 0, 0), (x*s, y*s, s, s))
				if F != 0:
					pygame.draw.line(screen, ((F/6)%255, (F/2)%255, (F/1)%255), (s*x+s/2, s*y+s/2), (s*(x+3*Fx/F/4)+s/2, s*(y+3*Fy/F/4)+s/2))
		state_change = False
	particles.update(points, k, d) # Pygame method Update 
	particles.draw(screen) # Pygame method draw
	pygame.display.flip() # Pygame method flip screen
	# Technically, this stuff doesn't need to happen unless you click 
	# All of this could be placed in that part of the code.

''' 
You can probably figure out how the calculations are done on your own.

The general idea:

With all code like this, you essentially just have an infinite loop.
Each time we pass through this loop, we update everything.
This code goes to each point, determines the location of each charge, 
and applies the formula

k*charge/(r**2)

for the most part. I also added 255 to determine what color to use.

Each particle also has code that implies it has the ability to move. 
However, it isn't used because that would take too much processing.

Also, I noticed that it calculates the field in a for loop.
This is kind of stupid, because I could have put this in a python.sprite.Group
and used the update command like I did on the particles.

Now, the particles get to update, but never actually need to update,
and I'm using the slowest method possible to actually do all the real updating.

*sigh*

Wait a second, I think particles are their own thing. I forgot. I may have made it
so you can place particles that don't affect the charges, but move a round in the electric fields.


'''

