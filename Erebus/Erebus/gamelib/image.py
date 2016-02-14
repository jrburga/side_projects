import pygame
import consts

tile_data = consts.tile_data
data_file = 'data//images//'
pyxel_file = 'data//pyxel//'

def load_image(name):
    return pygame.image.load(data_file+name+'.png')

def animate(name, frame):
    
    data = tile_data[name]
    image = load_image(name)
    
    tileswide = data['tiles'][0][0]
    size_x, size_y = data['tiles'][1]
    modulus = frame%tileswide
    rotation = modulus/tileswide
    frame_x, frame_y = (data['tiles'][1][0]*modulus, data['tiles'][1][1]*rotation)
    
    surface = pygame.Surface(data['tiles'][1])
    surface.blit(image, (0, 0), (frame_x, frame_y, size_x, size_y))
    surface.set_colorkey((255, 255, 255))
    return surface
    
    
