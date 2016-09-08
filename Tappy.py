import pygame
from random import randint as rnd

screen = pygame.display.set_mode((600, 400))
scrx, scry = screen.get_size()

pos = [50, 200]
vel = 0
acc = 0
rad = 7
obs = []

init_ypos = [0, 450]
gap_width = 75
column_width = 20
spacing = 1.5
speed = 4
passing = 0
count = False
passed = 0

FPS = 30

clock = pygame.time.Clock()
tick = pygame.time.get_ticks() + spacing*1000

full_game = True
while full_game:
	run_game = True
	while run_game:
		clock.tick(FPS)

		speed = 4 + passed/3
		gap_width = 75 - 2*passed/5
		column_width = 20 + 2*passed/8
		spacing = 2/(.1*(passed/2)+1)

		if tick < pygame.time.get_ticks():
			tick = pygame.time.get_ticks() + spacing*1000
			gap_ypos = rnd(gap_width, ((scry-2*gap_width)/gap_width)*gap_width)
			new_obs_top = pygame.Rect((scrx, 0), (column_width, gap_ypos))
			new_obs_bot = pygame.Rect((scrx, 0), (column_width, scry-gap_ypos-gap_width))
			new_obs_top.top = init_ypos[0]
			new_obs_bot.bottom = init_ypos[1]
			obs.append(new_obs_top)
			obs.append(new_obs_bot)

		screen.fill((0, 0, 0))

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run_game = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					failed_game = False
					full_game = False
					run_game = False
				if event.key == pygame.K_UP:
					acc = 1
					vel = -9
				if event.key == pygame.K_SPACE:
					acc = 1
					vel = -9
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_UP:
					acc = 1
				if event.key == pygame.K_SPACE:
					acc = 1

		vel += acc
		pos[1] += vel

		pygame.draw.circle(screen, (0, 0, 255), pos, rad)
		passing = 0

		removals = []
		for o in obs:
			o.x -= speed
			pygame.draw.rect(screen, (255, 0, 0), o)
			if o.x <= (pos[0] + rad) and (o.x + column_width) >= (pos[0] + rad):
				passing = 1
				if (pos[1]-rad > o.top and pos[1]-rad < o.bottom) or (pos[1]+rad > o.top and pos[1]+rad < o.bottom):
					run_game = False
			if o.x + column_width < 0:
				removals.append(o)

		for removal in removals:
			obs.remove(removal)

		if passing: 
			count = True
		if count:
			if not(passing):
				passed += 1
				count = False


		if pos[1]-rad < 0 or pos[1]+rad > 450:
			run_game = False

		pygame.display.flip()
		pygame.display.set_caption(str(passed))

	failed_game = True
	while failed_game:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				full_game = False
				failed_game = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					full_game = False
					failed_game = False
				if event.key == pygame.K_r or event.key == pygame.K_SPACE:
					obs = []
					pos = [50, 200]
					vel = 0
					acc = 0
					gap_width = 75
					column_width = 20
					speed = 4
					spacing = 1.5
					count = 0
					passed = 0
					failed_game = False



pygame.display.quit()