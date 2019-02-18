import pygame
import time

BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
base_rect = pygame.Rect(0, 0, 1, 1)

class Accumulator():
    def __init__(self, size):
        self._array = [0]*size
        self._averages = [0]*size
        self._index = 0
        self._average = 0
        self._num_values = 0
        self._max_size = size

    def acc_function(self, new_value, old_value):
        return old_value + (new_value - old_value) / float(self._num_values)

    def acc_function(self, new_value, old_value):
        alpha = .005
        return (new_value * alpha) + (old_value * (1 - alpha))

    def accumulate(self, value):
        if self._max_size == 0:
            return
        if self._num_values < self._max_size:
            self._num_values += 1
            
        last_index = (self._index + 1) % self._max_size
        last_value = self._array[last_index]

        self._average = self.acc_function(value, self._average) 
        self._averages[self._index] = self._average

        self._array[self._index] = value
        self._index = last_index

    @property
    def average(self):
        return self._average

    @property
    def values(self):
        return self._array

    @property
    def averages(self):
        return self._averages

def draw_values(screen, color, values, base_rect, axis='x'):
    for i, v in enumerate(values):
        if axis == 'x':
            base_rect.x = i
            base_rect.y = v
        if axis == 'y':
            base_rect.y = i
            base_rect.x = v
        pygame.draw.rect(screen, color, base_rect)

def draw_points(screen, color, points, base_rect, scale=(600, 600), offset=(0, 0)):
    for (x, y) in points:
        base_rect.x = x * scale[0] + offset[0]
        base_rect.y = y * scale[1] + offset[1]
        pygame.draw.rect(screen, color, base_rect)

def run():
    screen = pygame.display.set_mode((600, 600))
    running = True

    mouse_points = []
    
    max_points = 600
    x_acc = Accumulator(max_points)
    y_acc = Accumulator(max_points)
    samples = 0
    last_time = time.time()
    while running:
        current_time = time.time()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        (x, y) = pygame.mouse.get_pos()
        mouse_points.append((x, y))
        x_acc.accumulate(x)
        y_acc.accumulate(y)
        screen.fill(BLACK)
        draw_values(screen, BLUE, x_acc.values, base_rect, axis='y')
        draw_values(screen, GREEN, y_acc.values, base_rect, axis='x')
        draw_values(screen, RED, x_acc.averages, base_rect, axis='y')
        draw_values(screen, WHITE, y_acc.averages, base_rect, axis='x')
        pygame.display.set_caption("%f" % (current_time - last_time))
        pygame.display.flip()
        last_time = current_time

        
    pygame.display.quit()
    pygame.quit()

if __name__ == "__main__":
    run()