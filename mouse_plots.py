import pygame
import time

BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
base_rect = pygame.Rect(0, 0, 1, 1)

def draw_values(screen, color, values, base_rect, axis='x'):
    for i, v in enumerate(values):
        if axis == 'x':
            base_rect.x = i
            base_rect.y = v
        if axis == 'y':
            base_rect.y = i
            base_rect.x = v
        pygame.draw.rect(screen, color, base_rect)

def draw_points(screen, color, points, base_rect):
    for (x, y) in points:
        base_rect.x = x
        base_rect.y = y
        pygame.draw.rect(screen, color, base_rect)

def run():
    screen = pygame.display.set_mode((600, 600))
    running = True

    mouse_points = []
    x_points = []
    y_points = []
    max_points = 600
    samples = 0
    last_time = time.time()
    while running:
        current_time = time.time()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        (x, y) = pygame.mouse.get_pos()
        mouse_points.append((x, y))
        last_x = x_points[-1] if x_points else 0
        last_y = y_points[-1] if y_points else 0
        x_points.append(x/(samples+1) + )
        y_points.append(y)
        if len(mouse_points) > max_points:
            mouse_points.pop(0)
        if len(x_points) > max_points:
            x_points.pop(0)
        if len(y_points) > max_points:
            y_points.pop(0)
        screen.fill(BLACK)
        draw_values(screen, BLUE, x_points, base_rect, axis='y')
        draw_values(screen, GREEN, y_points, base_rect, axis='x')
        pygame.display.set_caption("%f" % (current_time - last_time))
        pygame.display.flip()
        last_time = current_time

        
    pygame.display.quit()
    pygame.quit()

if __name__ == "__main__":
    run()