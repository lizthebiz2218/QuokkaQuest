# TODO: Set up sprite to move on keys (take from gettingStarted.py)
# TODO: Set up sprite bounce back on collision (take from PongExample.py)

from pygame import K_LEFT, K_RIGHT

try:
    import sys
    import math
    import os
    import pygame
    from pygame.locals import QUIT, KEYDOWN, KEYUP, K_a, K_z, K_UP, K_DOWN
except ImportError as err:
    print("couldn't load module. %s" % (err))
    sys.exit(2)

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "data")

# keep
def load_png(name):
    """Load image and return image object"""
    fullname = os.path.join(data_dir , name)
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pygame.error as message:
        raise SystemExit(message)
    return image, image.get_rect()

# arbitrary width and height values
screen_width = 800
screen_height = 800

class Quokka(pygame.sprite.Sprite):
    """A ball that will move across the screen
    Returns: ball object
    Functions: update, calcnewpos
    Attributes: area, vector"""

    def __init__(self, vector):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png('ball.png')
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.vector = vector
        self.state = "still"
        self.movepos = [0, 0]
        self.hit = 0
        self.speed_x = 10
        self.speed_y = 10

    def update(self, collision_group):
        self.movepos[0] += self.speed_x
        self.movepos[1] += self.speed_y

        # code to get a bounce when the ball hits the edge of the screen
        if self.rect.right >= screen_width or self.rect.left <= 0:
            self.speed_x *= -1
        if self.rect.bottom >= screen_height or self.rect.top <= 0:
            self.speed_y *= -1
        
        has_object_collision = pygame.sprite.spritecollide(self,collision_group,False)

        if has_object_collision:
            rect = has_object_collision[0].rect
            if rect.collidepoint(self.rect.midbottom): # if we hit from bottom
                if self.speed_y > 0: # and the player was moving down
                    self.speed_y *= -1 # go up
            elif rect.collidepoint(self.rect.midtop): # if we hit from top
                if self.speed_y < 0: # and the player was moving up
                    self.speed_y *= -1 # go down
    
    def moveup(self):
        self.movepos[1] = self.movepos[1] - (self.speed_y)
        self.state = "moveup"

    def movedown(self):
        self.movepos[1] = self.movepos[1] + (self.speed_y)
        self.state = "movedown"
    
    def moveright(self):
        self.movepos[0] = self.movepos[1] + (self.speed_x)
        self.state = "moveright"

    def moveleft(self):
        self.movepos[0] = self.movepos[1] - (self.speed_x)
        self.state = "moveleft"


class Wall(pygame.sprite.Sprite):
    """Movable tennis 'bat' with which one hits the ball
    Returns: bat object
    Functions: reinit, update, moveup, movedown
    Attributes: which, speed"""

    def __init__(self, side):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png('bat.png')
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.side = side

def main():
        # Initialise screen
        pygame.init()
        screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption('Quokka Quest')

        # Fill background
        background = pygame.Surface(screen.get_size())
        background = background.convert()
        background.fill((0, 0, 0))

        # Initialise walls
        wall1 = Wall("left")
        wall2 = Wall("right")

        # Initialise quokka
        quokka = Quokka((0,0))

        # Initialise sprites
        wallsprites = pygame.sprite.RenderPlain((wall1, wall2))
        quokkasprite = pygame.sprite.RenderPlain(quokka)

        # Blit everything to the screen
        screen.blit(background, (0, 0))
        pygame.display.flip()

        # Initialise clock
        clock = pygame.time.Clock()

        # Event loop
        while 1:
            # Make sure game doesn't run at more than 60 frames per second
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                elif event.type == KEYDOWN:
                    if event.key == K_UP:
                        quokka.moveup()
                    if event.key == K_DOWN:
                        quokka.movedown()
                    if event.key == K_RIGHT:
                        quokka.moveright()
                    if event.key == K_LEFT:
                        quokka.moveleft()
                elif event.type == KEYUP:
                    if event.key == K_UP or event.key == K_DOWN or event.key == K_RIGHT or event.key == K_LEFT:
                        quokka.movepos = [0, 0]
                        quokka.state = "still"

            screen.blit(background, quokkasprite.rect, quokkasprite.rect)
            screen.blit(background, wall1.rect, wall1.rect)
            screen.blit(background, wall2.rect, wall2.rect)
            quokkasprite.update(wallsprites)
            wallsprites.update()
            quokkasprite.draw(screen)
            wallsprites.draw(screen)
            pygame.display.flip()


if __name__ == '__main__':
    main()