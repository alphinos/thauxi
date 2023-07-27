import pygame
from support import import_folder
from random import randint

class Enemy(pygame.sprite.Sprite):
    def __init__(self, width, height, pos_x, pos_y, path):
        super().__init__()
        self.surface = pygame.Surface((width, height))
        self.rect = self.surface.get_rect( topleft = (pos_x, pos_y))

        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

        self.speed = randint(6, 8)

        self.hit_points = 3

        self.invincible = False
        self.damageCD = 670

    def move(self):
        self.rect.x += self.speed
    
    def reverse_image(self):
        if self.speed > 0:
            self.image = pygame.transform.flip(self.image, True, False)

    def reverse(self):
        self.speed *= -1
    
    def animate(self):
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
    
    def checkDeath(self):
        if self.hit_points <= 0:
            self.kill()
            self.remove()

    def takeDamage(self):
        if not self.invincible:
            self.hit_points -= 1
            self.hurt_time = pygame.time.get_ticks()
            self.invincible = True
            self.image.fill((0, 0, 0))
    
    def invincibleCD(self):
        if self.invincible:
            current_time = pygame.time.get_ticks()
            if current_time - self.hurt_time >= self.damageCD:
                self.invincible = False
                self.image.fill((255, 255, 255))

    def update(self):
        self.animate()
        self.move()
        self.reverse_image()
        self.checkDeath()
        self.invincibleCD()