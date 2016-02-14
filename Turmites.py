import pygame
from random import randint as rnd
from random import choice

pygame.init()
screen = pygame.display.set_mode((300, 300))

class Turmite():
    def __init__(self):
        self.alive = True
        self.energy = 50
        self.dirs = [[1, 0], [0, 1], [-1, 0], [0, -1]]
        self.dir = rnd(0, 3)
        self.pos = [rnd(0, 99), rnd(0, 99)]
        self.state = rnd(0, 1)
        self.chrom = bin(rnd(0, 2**12-1))[2:]
        self.chrom = '0'*(12-len(self.chrom))+self.chrom
        c = self.chrom
        self.Read()
        self.Color()
    def Step(self, grid):
        self.energy -= 1
        a = grid[0]
        s = self.state
        r = self.read
        x, y = self.pos
        c = grid[1][y][x][a]
        self.state = self.read[1][s == r[0][0]][c == r[0][1]]
        grid[1][y][x][a] = self.read[2][c == r[0][0]][s == r[0][1]]
        nc = grid[1][y][x][a]
        if c:
            if not(nc):
                self.energy -= 1
        else:
            if nc:
                self.energy += 1
        if s == r[0][0]: self.dir += r[3][c == r[0][1]]
        else: self.dir -= r[3][c == r[0][1]]
        self.dir %= 4
        x += self.dirs[self.dir][0]
        y += self.dirs[self.dir][1]
        x %= len(grid[1][0])
        y %= len(grid[1])
        self.pos = [x, y]
    def Draw(self, screen):
        x, y = self.pos
        pygame.draw.rect(screen, self.color, (x*3, y*3, 2, 2))
    def Read(self):
        c = self.chrom
        self.read = [[int(x) for x in list(c[0:2])],
                     [[int(x) for x in list(c[2:4])], [int(x) for x in list(c[4:6])]],
                     [[int(x) for x in list(c[6:8])], [int(x) for x in list(c[8:10])]],
                     [int(x) for x in list(c[10:12])]]
    def Color(self):
        self.color = [eval('0b' +self.chrom[x:x+8]) for x in xrange(0, 5, 2)]
    def Kill(self, grid):
        c = grid[0]
        x, y = self.pos
        grid[1][y][x][c] = 1
        self.alive = False

def Mate(turmite1, turmite2):
    split = rnd(1, 11)
    s = rnd(0, 1)
    chroms = turmite1.chrom, turmite2.chrom
    new_turmite = Turmite()
    new_turmite.chrom = chroms[s][0:split]+chroms[not[s]][split:12]
    new_turmite.Read()
    new_turmite.Color()
    new_turmite.parents = (turmite1, turmite2)
    return new_turmite
        
def Step(grid):     # Updates Screen, Values, and Grid, according to Conway's Game of Life
     c = grid[0]    # Value To Check
     ly = len(grid[1])   # Modulus 
     lx = len(grid[1][0])# Modulus 
     for y in enumerate(grid[1]):       # Returns Rows of grid with accompanying Position
          for x in enumerate(y[1]):      # Returns Respective Column with accompanying Position
               n = 0                      # Neighbors
               x[1][not(c)] = x[1][c]     # Sets final value to initial value to start
               for iy in [-1, 0, 1]:      # Iterates Row Difference
                    for ix in [-1, 0, 1]:  # Iterates Column Difference
                         if not(ix == 0 and iy == 0):# If the value to be checked will not be itself
                              if grid[1][(y[0]+iy)%ly][(x[0]+ix)%lx][c]: n += 1
                              #In the main Grid, uses current x, y node,
                              #adds iy, ix differences
                              #modulates, to keep in range
                              #uses c for the current grid
                              #and checks if it is alive
                              # Then adds one to neigbor if True
               if x[1][c]: #Checks to see if node lives on
                    if n < 2 or n > 3:
                         x[1][not(c)] = 0
               else:       #Checks to see if node is born
                    if n == 3:
                         x[1][not(c)] = 1
               if x[1][not(c)]:
                    pygame.draw.rect(screen, (0, 0, 0), (x[0]*3, y[0]*3, 2, 2))
                    # Draws live node
     c = not(c)
     grid[0] = c

grid = [0,
        [[[choice([0]*20+[1]), 0]
          for x in xrange(100)]
         for y in xrange(100)]]

turmites = [Turmite() for x in xrange(50)]

Font = pygame.font.SysFont('None', 20)

clock = pygame.time.Clock()
run = True
steps = 0
generation = 0
dead = {}
while run:
    steps += 1
    clock.tick(15)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.display.quit()
                run = False
        if event.type == pygame.QUIT:
            pygame.display.quit()
            run = False
    screen.fill((255, 255, 255))
    Step(grid)
    for turmite in turmites:
        if turmite.alive:
            turmite.Step(grid)
            turmite.Draw(screen)
            if turmite.energy < 1:
                turmite.Kill(grid)
                dead[steps] = turmite
    alive = [turmite for turmite in turmites if turmite.alive]
    if len(alive) == 0:
        generation += 1
        turmites = []
        while len(dead) > 1:
            parent1 = dead.pop(max(dead))
            parent2 = dead.pop(max(dead))
            turmites.append(Mate(parent1, parent2))
            turmites.append(Mate(parent1, parent2))
        
            
    screen.blit(Font.render('%s:%s' % (generation, steps), 0, (0, 0, 255)), (5, 5))
    screen.blit(Font.render('Turmites: %s' % len(alive), 0, (255, 0, 0)), (5, 20))
    pygame.display.flip()

pygame.display.quit()
for step in dead:
    print dead[step].chrom, step
        
