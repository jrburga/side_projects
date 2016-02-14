import pygame, random, math, sys
import consts, image

pygame.init()
screen = pygame.display.set_mode(consts.screen_size, pygame.FULLSCREEN)


scroll_speed = [0, 0]
scroll_dir = [0, 0]
scroll_acc = 1

pygame.mouse.set_visible(False)

clock = pygame.time.Clock()

#### Display Title
title = image.load_image('erebus')
title_size = title.get_size()
title = pygame.transform.scale(title, (title_size[0]*5, title_size[1]*5))
title_rect = title.get_rect()
title_rect.center = (consts.screen_size[0]/2, consts.screen_size[1]/2)
screen.blit(title, title_rect)

font12 = pygame.font.FontType(None, 12)
anykey = font12.render('Press Any Key To Continue', True, (255, 255, 255))
screen.blit(anykey, (0, 0))

pygame.display.update()

title_loop = True

while title_loop:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.type == pygame.quit():
                pygame.display.quit()
                pygame.quit()
                sys.exit()
            title_loop = False
#### Wait for user Imput >> Start Game

def on_keydown(event):
    if event.key == pygame.K_UP:
        scroll_dir[1] = -1
    if event.key == pygame.K_DOWN:
        scroll_dir[1] = 1
    if event.key == pygame.K_RIGHT:
        scroll_dir[0] = -1
    if event.key == pygame.K_LEFT:
        scroll_dir[0] = 1

def on_keyup(event):
    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
        scroll_dir[1] = 0
    if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
        scroll_dir[0] = 0
    
####################################################################
######### Sprite Classes ##########
####################################################################

####################################################################
class Adrasteia(pygame.sprite.Sprite):

    def __init__(self):
        pygame.display.init()
        pygame.sprite.Sprite.__init__(self)
        self.image_name = 'heliose'
        self.frame = 0
        self.collisions = []

    def update(self):
        for collision in self.particle_collision:
            self.mass += collision.mass
        self.radius = 8*int(math.log(self.mass, 5))
        self.animate()

    def animate(self):
        self.image = image.animate(self.image_name, self.frame/consts.period).convert()
        self.image.set_colorkey((0, 0, 0))
        self.image = pygame.transform.scale(self.image, [self.radius*2]*2) 
        self.rect = self.image.get_rect()
        self.rect.center = (consts.screen_size[0]/2,
                            consts.screen_size[1]/2)
        self.frame += 1
##################################################################
class Nemesis(pygame.sprite.Sprite):

    def __init__(self):
        pygame.display.init()
        pygame.sprite.Sprite.__init__(self)
        self.image_name = 'nemesis'
        self.frame = 0
        self.collisions = []
            
    def update(self):
        for collision in self.collisions:
            self.mass += collisions.mass
        self.radius = 8*int(math.log(self.mass, 5))
        self.animate()
        
    def animate(self):
        self.image = image.animate(self.image_name, self.frame/consts.period).convert()
        self.image.set_colorkey((0, 0, 0))
        self.image = pygame.transform.scale(self.image, [self.radius*2]*2)
        self.rect = self.image.get_rect()
        self.frame += 1
####################################################################
###################################################################
class Hydrose(pygame.sprite.Sprite):

    def __init__(self):
        pygame.display.init()
        pygame.sprite.Sprite.__init__(self)
        self.image_name = 'hydrospiro'
        self.frame = random.randint(0, 3)
        self.animate()
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(0, consts.screen_size[0]),
                            random.randint(0, consts.screen_size[1]))
        self.mass = 10
        self.dx, self.dy = 0, 0

    def update(self, scroll_speed, gravity = None, pos = None, mass = None):
        px, py = self.center
        if gravity:
            mx, my = pos
            r = math.sqrt((mx-px)**2 + (my-py)**2)
            if r:
                acc = consts.G*mass/r**2
                self.dx += acc*(mx-px)/r
                self.dy += acc*(my-py)/r
        else:
            if mx < 0 or mx > consts.screen_size[0] or my < 0 or my > consts.screen_size[1]:
                self.kill()
            self.animate()
            self.rect.x += self.dx + scroll_speed[0]
            self.rect.y += self.dy + scroll_speed[1]
            
    def animate(self):
        self.image = image.animate(self.image_name, self.frame/consts.period)
        self.image.set_colorkey((0, 0, 0))
        self.frame += 1
##################################################################
class bgStar(pygame.sprite.Sprite):

    def __init__(self):
        pygame.display.init()
        pygame.sprite.Sprite.__init__(self)
        self.image = image.load_image('particle').convert()
        alpha = random.randint(0, 255)
        self.image.set_alpha(alpha)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(0, consts.screen_size[0]),
                            random.randint(0, consts.screen_size[1]))
        
    def update(self, scroll_speed):
        px, py = self.rect.center
        if px < 0 or py < 0 or px > consts.screen_size[0] or py > consts.screen_size[1]:
            self.kill()
        self.rect.x += scroll_speed[0]
        self.rect.y += scroll_speed[1]

####################################################################
######### Main Game Loop ###########
####################################################################

stars = pygame.sprite.Group()
particles = pygame.sprite.Group()
bgstars = pygame.sprite.Group()

player = Adrasteia()
nemesis = Nemesis()

[particles.add(Hydrose()) for x in xrange(10)]
[bgstars.add(bgStar()) for x in xrange(100)]
stars.add(player, nemesis)


loop = True

while loop:
    self.clock.tick(consts.FPS)
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False
        if event.type == pygame.KEYDOWN:
            on_keydown(event)
        if event.type == pygame.KEYUP:
            on_keyup(event)
        
    scroll_speed[0] += scroll_dir[0]*scroll_acc
    scroll_speed[1] += scroll_dir[1]*scroll_acc

    bgstars.update(scroll_speed)
    particles.update(False, True, player.rect.center, player.mass)
    particles.update(False, True, nemesis.rect.center, nemesis.mass)
    particles.update(scroll_speed)
    stars.update()

    bgstars.draw(screen)
    particles.draw(screen)
    stars.draw(screen)

    pygame.display.update()



pygame.display.quit()
pygame.quit()
sys.exit()
