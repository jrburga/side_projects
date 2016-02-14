#!/usr/bin/env python

import pygame
import sys
import time
import math
from random import randint as rnd 
from random import choice

pygame.init()

screen_size = [600, 720]
sx, sy = screen_size

grid_size = [10, 24]
gx, gy = grid_size

pend_size = [6, 6]
px, py = pend_size

mx, my = sx/2/gx, sy/gy
spx, spy = 0, 0

screen = pygame.display.set_mode((sx, sy))

font_next = pygame.font.SysFont('emulogic', 17)
font_sl = pygame.font.SysFont('emulogic', 20)
txt_next = "NEXT PIECE"
txt_score = "SCORE: "
txt_lines = "LINES: "
txt_lvl = "LEVEL: "


center_x = sx/2 + sx/4
center_y = sy/2

txt_next_center = (center_x, 45)
txt_score_center = (center_x, center_y)
txt_lines_center = (center_x, center_y - 60)
txt_lvl_center = (center_x, center_y + 60)

clockwise = cw =  0
counterclockwise = ccw = 1

down = [0, 1]
left = [-1, 0]
right = [1, 0]
init_pos = [4, 2]
pend_pos = [2, 3]

pend = [[0 for x in xrange(px)] for y in xrange(py)]
grid = [[0 for x in xrange(gx)] for y in xrange(gy)]
colors = [[255*int(bit) for bit in list(bin(x))[3:]] 
           for x in xrange(15, 7, -1)]

colors[-1] = [255/2, 255/2, 255/2]

#pos[0] reserved for anchor.
pieces = [[[0, 0], [1, 0], [2,  0], [-1, 0]], #I 
		  [[0, 0], [0, 1], [0, -1], [1, -1]], #J
		  [[0, 0], [0, 1], [0, -1], [1,  0]], #T
		  [[0, 0], [0, 1], [0, -1], [1,  1]], #L 
		  [[0, 0], [1, 0], [1,  1], [0, -1]], #S 
		  [[0, 0], [0, 1], [1,  0], [1, -1]], #Z
		  [[0, 0], [0, 1], [1,  0], [1,  1]], #O
		 ]

def Rotate(piece, direction, grid):
	"""0 = clockwise, 1 = counterclockwise"""
	new_set = []
	a, b = piece[0]
	if direction:
		for pos in piece:
			x, y = pos
			new_set += [[y-b+a, a-x+b]]
	else:
		for pos in piece:
			x, y = pos
			new_set += [[b-y+a, x-a+b]]
	for pos in new_set:
		x, y = pos
		if x < 0 or x > 9 or y < 0 or y > 24:
			return piece
		if grid[y][x] != 0:
			return piece
	return new_set

def Translate(piece, direction, grid):
	"""direction is a set of coordinates which will
	be added to the current values of the piece"""
	new_set = []
	dx, dy = direction
	for pos in piece:
		x, y = pos
		new_set += [[x+dx, y+dy]]
	for pos in new_set:
		x, y = pos
		if x < 0 or x > 9:
			return piece
		if grid[y][x] != 0:
			return piece
	return new_set

def Clear_Lines(grid, score, speed, streak):
	new_grid = grid
	new_score = score
	m = 1
	for line in xrange(gy):
		for x in xrange(gx):
			if new_grid[line][x] == 0:
				break
		else:
			new_score += 10*m*(speed-1)*(streak+m-1)
			m += 1
			for y in xrange(line-1, 0, -1):
				for x in xrange(10):
					new_grid[y+1][x] = new_grid[y][x]
	return new_grid, new_score, m-1, new_score - score

points = 0
score = 0
lines = 0
line_factor = 5
total_lines = 0
streak = 1
speed = 2
sec = 1./speed

pin = rnd(0, 6)
pic = pieces[pin]
pos = Translate(pic, init_pos, grid)
for n in xrange(rnd(0, 4)):
		pos = Rotate(pos, cw, grid)

next_pin = rnd(0, 6)
next_pic = pieces[next_pin]
next_pos = Translate(next_pic, pend_pos, pend)

check_time = (time.clock()) + sec

run_game = True
end_game = False
while run_game:

	screen.fill((0, 0, 0))
	speed = 2+(total_lines/line_factor)

	for p in pos:
		x, y = p
		grid[y][x] = 0

	for p in next_pos:
		x, y = p
		pend[y][x] = 0

	for y in xrange(5):
		for x in xrange(10):
			if grid[y][x] != 0:
				end_game = True
				run_game = False

	if time.clock() >= check_time:
		if [p[1] for p in pos].count(gy-1) == 0 and [grid[p[1]+1][p[0]] for p in pos if p[1] != gy].count(0) == 4:
			pos = Translate(pos, down, grid)
		else:
			sec = 1./speed
			for p in pos:
				x, y = p
				grid[y][x] = pin + 1
			grid, score, lines, points = Clear_Lines(grid, score, speed, streak)
			if lines:
				streak += lines
			else:
				streak = 1
			total_lines += lines
			pin = next_pin
			pic = next_pic
			pos = Translate(pic, init_pos, grid)
			for n in xrange(rnd(0, 4)):
				pos = Rotate(pos, cw, grid)
			next_pin = rnd(0, 6)
			next_pic = pieces[next_pin]
			next_pos = Translate(next_pic, pend_pos, pend)

		check_time = (time.clock()) + sec

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run_game = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				run_game = False
			if event.key == pygame.K_LEFT:
				if [p[0] for p in pos].count(0) == 0:
					pos = Translate(pos, left, grid)
			if event.key == pygame.K_RIGHT:
				if [p[0] for p in pos].count(9) == 0:
					pos = Translate(pos, right, grid)
			if event.key == pygame.K_DOWN:
				sec = .01/speed
			if event.key == pygame.K_UP:
				pos = Rotate(pos, cw, grid)
				#if event.key == pygame.K_DOWN:
				#	pos = Rotate(pos, ccw, grid)
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_DOWN:
				sec = 1./speed


	for p in pos:
		x, y = p
		grid[y][x] = pin + 1

	for p in next_pos:
		x, y = p
		pend[y][x] = next_pin + 1

	for x in xrange(gx):
		for y in xrange(gy):
			pygame.draw.rect(screen, 
							 colors[grid[y][x]], 
							 (x*mx+spx, y*my+spy, mx-spx, my-spy))

	for x in xrange(px):
		for y in xrange(py):
			pygame.draw.rect(screen,
							 colors[pend[y][x]], 
							 ((x+12)*mx+spx, (y+1)*my+spy, mx-spx, my-spy))

	pygame.draw.line(screen, (255, 0, 0), (0, my*5), (300, my*5), 2)
	pygame.draw.line(screen, (0, 0, 255), (300, 0), (300, 720), 2)

	text1 = font_next.render(txt_next, True, (0, 0, 0))
	text2 = font_sl.render(txt_score + str(score), True, (255, 255, 255))
	text3 = font_sl.render(txt_lvl + str(speed - 1), True, (255, 255, 255))
	text4 = font_sl.render(txt_lines + str(total_lines), True, (255, 255, 255))

	txt_next_pos = text1.get_rect()
	txt_score_pos = text2.get_rect()
	txt_lvl_pos = text3.get_rect()
	txt_lines_pos = text4.get_rect()

	txt_next_pos.center = txt_next_center
	txt_score_pos.center = txt_score_center
	txt_lvl_pos.center = txt_lvl_center
	txt_lines_pos.center = txt_lines_center

	screen.blit(text1, txt_next_pos)
	screen.blit(text2, txt_score_pos)
	screen.blit(text3, txt_lvl_pos)
	screen.blit(text4, txt_lines_pos)

	pygame.display.set_caption("Score: " + str(score) + 
							   " | Lines: " + str(total_lines) +
							   " | Level: " + str(speed-1) +
							   " | Points: " + str(points))
	pygame.display.flip()

while end_game:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			end_game = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				end_game = False

pygame.display.quit()
pygame.quit()
sys.exit()
