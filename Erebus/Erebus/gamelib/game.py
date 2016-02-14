import pygame, sys
from random import randint as rnd
from random import choice
from math import sqrt, log
import consts, image

#### An excessive excuse for a class: ####
#### Initializes, runs, predefines,   ####
#### and plays all the code.          ####

class Game(object):

    class Window(object):
        def __init__(self):
            pygame.display.set_caption('Erebus')
            self.screen = pygame.display.set_mode(consts.screen_size, pygame.FULLSCREEN)
            
    def __init__(self):
        self.window = self.Window()
        self.clock = pygame.time.Clock()
        self.scroll =  [0, 0]
        self.scroll_speed = [0, 0]
        pygame.mouse.set_visible(False)
        
        #### Background that probably won't get used ####
        self.bg = image.load_image('background2')
        self.bg = pygame.transform.scale(self.bg, consts.screen_size)

        pygame.mixer.init()
        pygame.font.init()

        self.font = pygame.font.FontType(None, 24)

        title = image.load_image('erebus')
        title_size = title.get_size()
        title = pygame.transform.scale(title, (title_size[0]*5, title_size[1]*5))
        title_rect = title.get_rect()
        title_rect.center = consts.screen_size[0]/2, consts.screen_size[1]/2
        self.window.screen.blit(title, title_rect)
 
        text = self.font.render('Press Any Key To Play', True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (consts.screen_size[0]/2, consts.screen_size[1]-24)
        self.window.screen.blit(text, text_rect)

        pygame.display.update()

        start = False
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    self.on_keydown(event)
                    start = True
                    
            if start:
                break

        try:
            pygame.mixer.init()
        except:
            print 'Cannot load sound'

        #### Creates sprite groups ####
        self.particles = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()
        self.bgstars = pygame.sprite.Group()

        #### Creates Sprites! ####
        [self.bgstars.add(bgStar()) for x in xrange(10)]
        [self.particles.add(Particle('Hydrogen')) for x in xrange(1)]
        #### Creat Player + Nemesis ####
        self.Player = Star()
        self.Nemesis = Nemesis()
        #### More precursors        ####
        self.stars.add(self.Player)
        self.instructions = True
        self.nemesis_exists = False
        self.nemesis_start = 1

        self.loop()

    def loop(self):
        #### Main game loop. Predefined Functions make it look pointless ####
        self.mouse_attract = False
        while True:
            self.clock.tick(consts.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.end_game()
                elif event.type == pygame.KEYDOWN:
                    self.on_keydown(event)
                elif event.type == pygame.KEYUP:
                    self.on_keyup(event)
            self.update()
            
    def on_keydown(self, event):
        self.instructions = False
        if event.key == pygame.K_ESCAPE:
            self.end_game()
        if event.key == pygame.K_UP:
            self.scroll[1] = 1
        if event.key == pygame.K_DOWN:
            self.scroll[1] = -1
        if event.key == pygame.K_LEFT:
            self.scroll[0] = 1
        if event.key == pygame.K_RIGHT:
            self.scroll[0] = -1
            
    def on_keyup(self, event):
        if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
            self.scroll[1] = 0
        if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
            self.scroll[0] = 0
            
    def update(self):
        #### Technically, the main game loop ####
        #### Can always change ####
        #self.window.screen.blit(self.bg, (0, 0))
        self.window.screen.fill((0, 0, 0))
        self.scroll_speed[0] += 8.*self.scroll[0]/self.Player.radius
        self.scroll_speed[1] += 8.*self.scroll[1]/self.Player.radius
        
        for star in self.stars.sprites():
            self.particles.update(False, True, self.Player.rect.center, star.mass)
            if self.nemesis_exists:
                self.particles.update(False, True, self.Nemesis.rect.center, star.mass)
        self.particles.update(self.scroll_speed)

        #### Checks for collisions, adding them to list ####
        self.Player.particle_collision = pygame.sprite.spritecollide(self.Player, self.particles,True)
        if self.nemesis_exists:
            if self.nemesis_start:
                self.stars.add(self.Nemesis)
                self.Nemesis.rect.center =  (choice([rnd(-consts.screen_size[0]*2., 0),
                                                           rnd(consts.screen_size[0], consts.screen_size[0]*3/2.)]),
                                            choice([rnd(-consts.screen_size[1]*2., 0),
                                                           rnd(consts.screen_size[1], consts.screen_size[1]*3/2.)]))
                self.nemesis_start = 0
            self.Nemesis.collisions = pygame.sprite.spritecollide(self.Nemesis, self.particles, True)
 
        self.bgstars.update(self.scroll_speed)

        if len(self.particles.sprites()) < 100:
            new_particle = Particle('Hydrogen')
            new_particle.mass = self.Player.radius
            self.particles.add(new_particle)
        if len(self.bgstars.sprites()) > 1000:
            choice(self.bgstars.sprites()).kill()
        new_bgstar = bgStar()
        new_bgstar.rect.center = (rnd(-consts.screen_size[0] , consts.screen_size[0]*2),
                                    rnd(-consts.screen_size[1], consts.screen_size[1]*2))
        self.bgstars.add(new_bgstar)

#### Updates remaining sprites. Draws ####
            
            #### Nemesis Sucks #### 
        if self.nemesis_exists:
            self.Nemesis.update(self.scroll_speed, self.Player)
            self.Player.update(self.Nemesis)
            if pygame.sprite.collide_circle(self.Player, self.Nemesis):
                self.Game_Over()
    
            #if self.Nemesis.extraction:
            #    self.Player.mass -= 1
            #    new_particle = Particle('Hydrogen')
            #    new_particle.mass = 1
            #    new_particle.rect.center = self.Player.rect.center
            #    new_particle.update(None, True, self.Nemesis.rect.center, self.Nemesis.mass)
            #    new_particle.rect.center = 1/new_particle.dx*self.Player.radius, 1/new_particle.dy*self.player.radius
            #    self.particles.add(new_particle)

        else:        
            self.Player.update(None)
        self.bgstars.draw(self.window.screen)
        self.particles.draw(self.window.screen)
        self.stars.draw(self.window.screen)
        
        if not(self.nemesis_exists):
            if self.Player.radius/8 == 3:
                self.nemesis_exists = True

        if self.instructions:
            text = self.font.render('Use Arrow Keys To Move', True, (255, 255, 255))
            text.set_alpha(10)
            text_rect = text.get_rect()
            text_rect.center = consts.screen_size[0]/2, consts.screen_size[1]/2
            self.window.screen.blit(text, text_rect)

        pygame.display.update()

    def Game_Over(self):
        for x in xrange(256):
            self.clock.tick(consts.FPS)
            self.window.screen.fill((x, x, x))
            pygame.display.update()
        self.end_game()
        

        
    def end_game(self):
        #### Very reduntant. Called once. ####
        #### It sould just be placed there####
        pygame.display.quit()
        pygame.quit()
        sys.exit()

#### Sprite Classes ####

        #### Gugh... this is where I got a little trigger happy ####
        #### Enjoy this spaghetti code ####
        
class Particle(pygame.sprite.Sprite):

    def __init__(self, name):
        pygame.sprite.Sprite.__init__(self)
        self.name = name

        self.frame = rnd(0, 3)
        self.image = image.animate('hydrospiro', 0)
        self.rect = self.image.get_rect()
        self.rect.center = (rnd(-consts.screen_size[0], consts.screen_size[0]*2),
                            rnd(-consts.screen_size[1], consts.screen_size[1]*2))
        self.mass = 1.
        self.dx, self.dy = 0, 0
        self.image.set_colorkey((0, 0, 0))
        self.radius = int(log(self.mass, 10))
        #self.col = []
        
    def update(self, scroll_speed, attractor = None, pos = None, mass = None):
        px, py = self.rect.center
        if attractor:
            mx, my = pos
            r = sqrt((mx-px)**2+(my-py)**2)
            if r:
                acc = consts.G*mass/r**2
                self.dx += acc*(mx-px)/r
                self.dy += acc*(my-py)/r
                
        else:
            #if px < 0 or px > consts.screen_size[0] or py < 0 or py > consts.screen_size[1]:
            #    self.kill()
            #for particle in self.col:
            #    self.mass += particle.mass
            self.image = image.animate('hydrospiro', self.frame/consts.period).convert()
            self.image.set_colorkey((0, 0, 0))
            self.rect.x += self.dx + scroll_speed[0]
            self.rect.y += self.dy + scroll_speed[1]
            self.frame += 1
            #self.image = pygame.transform.scale(self.image, (self.radius*2, self.radius*2)) 
            #self.rect = self.image.get_rect()
            #self.image.set_alpha(2*(self.mass%128)+1)

#### Weird order. Here's the actual player ####
class Star(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = image.animate('heliose', 0)
        self.rect = self.image.get_rect()
        self.particle_collision = []
        self.rect.center = consts.screen_size[0]/2, consts.screen_size[1]/2
        self.mass = 100.
        self.frame = 0
        self.radius = 8*int(log(self.mass, 10))
        self.dx, self.dy = 0, 0

    def update(self, nemesis):
        if nemesis:
            px, py = self.rect.center
            mx, my = nemesis.rect.center
            r = sqrt((mx-px)**2+(my-py)**2)
            acc = consts.G*nemesis.mass
            self.dx = acc*(mx-px)/r
            self.dy = acc*(my-py)/r
        else:
            for collision in self.particle_collision:
                self.mass += collision.mass
            self.internal_force = consts.G*self.mass/self.radius**2
            self.image = image.animate('heliose', self.frame/consts.period).convert()
            self.image.set_colorkey((0, 0, 0))
            self.frame += 1
            self.radius = 8*int(log(self.mass, 5))
            self.image = pygame.transform.scale(self.image, (self.radius*2, self.radius*2))
            self.rect = self.image.get_rect()
            self.rect.center = (consts.screen_size[0]/2 + self.dx, consts.screen_size[1]/2 + self.dy)
            # self.rect.center = pygame.mouse.get_pos()

class Nemesis(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.extraction = False
        self.frame = 0
        self.collisions = []
        self.image = image.animate('nemesis', self.frame)
        self.rect = self.image.get_rect()
        self.dx, self.dy = 0, 0
        self.dy = 0
        self.mass = 10000
        self.radius = 8*int(log(self.mass, 5))
        
    def update(self, scroll_speed, heliose):
        for collision in self.collisions:
            self.mass += collision.mass
        self.internal_force = consts.G*self.mass/self.radius**2
        mx, my = heliose.rect.center
        x, y = self.rect.center
        r = sqrt((x-mx)**2+(my-y)**2)
        pull_force = consts.G*self.mass*heliose.mass/r**2
        acc = consts.G*(heliose.mass+self.mass)/r**2
        self.dx += acc*(mx-x)/r
        self.dy += acc*(my-y)/r
        self.df = pull_force - heliose.internal_force
        if self.df > 0:
            self.extraction = True
        else:
            self.extraction = False
        
        self.image = image.animate('nemesis', self.frame/consts.period).convert()
        self.image.set_colorkey((0, 0, 0))
        self.frame += 1
        self.radius = 8*int(log(self.mass, 5))
        self.image = pygame.transform.scale(self.image, (self.radius*2, self.radius*2))
        self.rect = self.image.get_rect()
        self.rect.center = x, y
        self.rect.x += self.dx+scroll_speed[0]*2
        self.rect.y += self.dy+scroll_speed[1]*2
        self.rect.right %= consts.screen_size[0]*2
        self.rect.bottom %= consts.screen_size[1]*2
        self.frame += 1


#### Background stars for movement effect.   ####

class bgStar(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = image.load_image('particle').convert()
        self.rect = self.image.get_rect()
        self.rect.center = (rnd(0, consts.screen_size[0]),
                            rnd(0, consts.screen_size[1]))
        self.dx, self.dy = (rnd(-2, 2), rnd(-2, 2))

    def update(self, scroll_speed):
        px, py = self.rect.center

        self.image.set_alpha(rnd(0, 255))
        self.rect.x += self.dx + scroll_speed[0]
        self.rect.y += self.dy + scroll_speed[1]
