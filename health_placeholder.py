import pygame
import time

# all placeholder values, should be changed for appropriate graphics
start_quokka_health = 5
heart_width = 20
heart_height = 20
heart_file_name = ".png"

# starting from left most corner, arbitrarily located, should be changed in final
heart_poses_x = [0,1,2,3,4]
heart_poses_y = [1,2,3,4,5]

heart = pygame.transform.scale(pygame.image.load('').convert_alpha(), heart_width, heart_height)
heart_images = []

for lives in range(start_quokka_health) :
    heart_images.append(pygame.transform.scale(pygame.image.load(heart_file_name).convert_alpha(), heart_width, heart_height))

class health() :
    def __init__(self, default_health):
        self.health = default_health
        self.visible = True
        
    def updateHealth(self, was_hit) :
        if was_hit:
            if self.health > 0:
                self.health -= 1
            else:
                self.visible = False

# should go near main loop
quokka_health = health(start_quokka_health)

# in main loop
quokka_health.updateHealth(placeholder_wasHit)
if placeholder_wasHit :
    heart_images.remove(heart_images[quokka_health.health - 1])

for val in range(quokka_health.health) :
    placeholder_screen.blit(heart_images, heart_poses_x[val], heart_poses_y[val])
