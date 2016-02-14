import pygame, random, math, sys
import consts, image

#### An excessive excuse for a class: ####
#### Initializes, runs, predefines,   ####
#### and plays all the code.          ####

class Game(object):

    class Window(object):
        #### Unecessary pre-optimization class ####
        def __init__(self):
            pygame.display.set_caption('Erebus')
            self.screen = pygame.display.set_mode(consts.screen_size, pygame.FULLSCREEN)
            
    def __init__(self):
        #### why it was so unecessary ####
        self.window = self.Window()
        self.scroll =  [0, 0]
        self.scroll_speed = [0, 0]
        self.scp = [lambda x, a: random.randint(0, a),
                    lambda x, a: 0,
                    lambda x, a: consts.screen_size[x]]
        self.cursor = self.Cursor()
        pygame.mouse.set_visible(False)
        
        #### Background that probably won't get used ####
        self.bg = image.load_image('background2')
        self.bg = pygame.transform.scale(self.bg, consts.screen_size)

        #### TODO: Sound... Title... Font...         ####
        pygame.mixer.init()
        pygame.font.init()

        title = image.load_image('erebus')
        title_size = title.get_size()
        title = pygame.transform.scale(title, (title_size[0]*5, title_size[1]*5))
        title_rect = title.get_rect()
        title_rect.center = consts.screen_size[0]/2, consts.screen_size[1]/2
        self.window.screen.blit(title, (title_rect.x, title_rect.y))

        pygame.display.update()

        start = False
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    self.on_keydown(event)
                    start = True
                    
            if start:
                break

        # pygame.mouse.set_visible(True)

        try:
            pygame.mixer.init()
        except:
            print 'Cannot load sound'

        #### Creates sprite groups ####
        self.particles = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()
        self.bgstars = pygame.sprite.Group()

        #### Creates Sprites! ####
        [self.bgstars.add(bgStar(self.scroll)) for x in xrange(1000)]
        [self.particles.add(Particle('Hydrogen')) for x in xrange(1)]

        self.Player = Star()
        self.Nemesis = Nemesis()
        
        self.stars.add(self.Player)

        #### Self executing code. How meta ####
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
            #### Just why!?! ####
            
    def on_keydown(self, event):
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
        self.scroll_speed[0] += .1*self.scroll[0]/self.Player.mass
        self.scroll_speed[1] += .1*self.scroll[1]/self.Player.mass
        for star in self.stars.sprites():
            self.particles.update(self.scroll_speed, True, self.Player.rect.center, star.mass)

        #### I don't know why I never thought of     ####
        #### conditions in an update function before ####
        self.particles.update(self.scroll_speed)

        #### Checks for collisions, adding them to list ####
        self.Player.particle_collision = pygame.sprite.spritecollide(self.Player,
                                                                     self.particles,
                                                                     True)
        self.Nemesis.particle_collision = pygame.sprite.spritecollide(self.Nemesis,
                                                                      self.particles,
                                                                      True)

        #for particle in self.particles.sprites():
        #    particle.col = pygame.sprite.spritecollide(particle, self.particles, True)
        self.bgstars.update(self.scroll_speed)

        #### Why my head hurts from playing this game ####
        if len(self.particles.sprites()) < 20:
            if random.choice([0]*8+[1]):
                new_particle = Particle('Hydrogen')
                set_scroll = self.scroll
                if self.scroll[0] and self.scroll[1]:
                    set_scroll = random.choice([(self.scroll[0], 0), (0, self.scroll[1])])
                new_particle.rect.center = (self.scp[set_scroll[0]](1, consts.screen_size[0]),
                                            self.scp[set_scroll[1]](0, consts.screen_size[1]))

                self.particles.add(new_particle)
        if len(self.bgstars.sprites()) < 2000:
            new_bgstar = bgStar(self.scroll)
            set_scroll = self.scroll
            if self.scroll[0] and self.scroll[1]:
                set_scroll = random.choice([(self.scroll[0], 0), (self.scroll[1], 0)])
            new_bgstar.rect.center = (self.scp[self.scroll[0]](0, consts.screen_size[0]),
                                      self.scp[self.scroll[1]](1, consts.screen_size[1]))
            self.bgstars.add(new_bgstar)

        #### Runs the updates and draws ####
        # self.stars.update()
        self.Player.update()
        self.bgstars.draw(self.window.screen)
        self.particles.draw(self.window.screen)
        self.stars.draw(self.window.screen)
        pygame.display.update()

        
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

        self.frame = random.randint(0, 3)
        self.image = image.animate('hydrospiro', 0)
        self.rect = self.image.get_rect()
        self.rect.center = random.randint(0, consts.screen_size[0]), random.randint(0, consts.screen_size[1])
        self.mass = 10
        self.dx, self.dy = 0, 0
        self.image.set_colorkey((0, 0, 0))
        self.radius = int(math.log(self.mass, 10))
        #self.col = []
        
    def update(self, scroll_speed, attractor = None, pos = None, mass = None):
        if attractor:
            mx, my = pos
            px, py = self.rect.center
            r = math.sqrt((mx-px)**2+(my-py)**2)
            if r:
                acc = consts.G*mass/r**2
                self.dx += acc*(mx-px)/r
                self.dy += acc*(my-py)/r
                
        else:
            if self.rect.center[0] < 0 or self.rect.center[0] > consts.screen_size[0] or self.rect.center[1] < 0 or self.rect.center[1] > consts.screen_size[1]:
                self.kill()
            #for particle in self.col:
            #    self.mass += particle.mass
            self.image = image.animate('hydrospiro', self.frame/consts.period).convert()
            self.image.set_colorkey((0, 0, 0))
            self.rect.x += self.dx+scroll_speed[0]
            self.rect.y += self.dy+scroll_speed[1]
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
        self.mass = 100
        self.frame = 0
        self.radius = 8*int(math.log(self.mass, 10))

    def update(self):
        for collision in self.particle_collision:
            self.mass += collision.mass
        self.image = image.animate('heliose', self.frame/consts.period).convert()
        self.image.set_colorkey((0, 0, 0))
        self.frame += 1
        self.radius = 8*int(math.log(self.mass, 5))
        self.image = pygame.transform.scale(self.image, (self.radius*2, self.radius*2))
        self.rect = self.image.get_rect()
        self.rect.center = consts.screen_size[0]/2, consts.screen_size[1]/2
        # self.rect.center = pygame.mouse.get_pos()
        # self.rect.center = pygame.mouse.get_pos()

class Nemesis(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.frame = 0
        self.image = image.animate('nemesis', self.frame)
        self.rect = self.image.get_rect()
        self.dx, self.dy = 0, 0
        self.mass = 0
        
    def update(self):
        
        self.image = image.animate('nemesis', self.frame)
        self.rect.x += self.dx
        self.rect.y += self.dy
        self.frame += 1

#### Background stars for movement effect.   ####

class bgStar(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = image.load_image('particle')
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(0, consts.screen_size[0]),
                            random.randint(0, consts.screen_size[1]))
        self.dx, self.dy = (0, 0)

    def update(self, scroll_speed):

        if self.rect.center[0] < 0 or self.rect.center[1] < 0 or self.rect.center[0] > consts.screen_size[0] or self.rect.center[1] > consts.screen_size[1]:
            self.kill()
        self.image.set_alpha(random.randint(0, 255))
        self.rect.x += self.dx+scroll_speed[0]
        self.rect.y += self.dy+scroll_speed[1]
