import pygame
from support import import_folder

class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, groups, enemies):
        super().__init__(groups)
        
        direction = player.attack_direction
        self.destroyAttack = player.destroyAttack

        self.direction = direction

        self.player = player
        self.enemies = enemies

        self.frame_index = 0
        self.animation_spd = 0.15

        # Graphic
        full_path = f"../graphics/weapon/{player.weapon}/{direction}"
        self.animation = import_folder(full_path)

        self.image = self.animation[self.frame_index]

        # Placement

        if direction == "right":
            self.rect = self.image.get_rect( midleft = player.rect.midright + pygame.math.Vector2(16, 0) )
        elif direction == "left":
            self.rect = self.image.get_rect( midright = player.rect.midleft + pygame.math.Vector2(16, 0) )
        elif direction == "up":
            self.rect = self.image.get_rect( midbottom = player.rect.midtop - pygame.math.Vector2(3, -1) )
        elif direction == "down":
            self.rect = self.image.get_rect( midbottom = player.rect.midtop + pygame.math.Vector2(-3, 170) )

    def animate(self):
        
        #loop over frame index
        self.frame_index += self.animation_spd
        if self.frame_index >= len(self.animation):
            self.frame_index = 0
        
        image = self.animation[int(self.frame_index)]
        self.image = image
    
    def dealDamage(self):

        collided_enemies = pygame.sprite.spritecollide(self, self.enemies, False)

        if collided_enemies:
            for enemy in collided_enemies:
                enemy.hit_points -= 1
    
    def updateWeapon(self):
        if self.direction == "right":
            self.rect = self.image.get_rect( midleft = self.player.rect.midright + pygame.math.Vector2(16, 0) )
        elif self.direction == "left":
            self.rect = self.image.get_rect( midright = self.player.rect.midleft + pygame.math.Vector2(16, 0) )
        elif self.direction == "up":
            self.rect = self.image.get_rect( midbottom = self.player.rect.midtop - pygame.math.Vector2(3, -1) )
        elif self.direction == "down":
            self.rect = self.image.get_rect( midbottom = self.player.rect.midtop + pygame.math.Vector2(-3, 170) )