import pygame
from weapons import Weapon
from support import import_folder
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, group, level, create_jump_particles):
        super().__init__(group)
        self.player_surface = pygame.Surface((24, 68))
        self.import_character_assets()
        self.frame_index = 0
        self.animation_spd = 0.2
        self.image = self.animations["idle"][self.frame_index]
        self.rect = self.player_surface.get_rect( topleft = (pos_x, pos_y) )

        self.group = group

        # World awareness
        self.level_obj = level

        self.world_tiles = self.level_obj.terrain_sprites.sprites()
        self.enemies = self.level_obj.enemy_sprites
        self.bottles = self.level_obj.soul_sprites
        self.goal = self.level_obj.goal

        self.map_width = self.level_obj.map_surface.get_width()
        self.map_height = self.level_obj.map_surface.get_height()

        # Game state
        self.game_state = "level"

        # Dust particles
        self.import_dust_run_particles()
        self.dust_frame_index = 0
        self.dust_animation_spd = 0.2
        self.display_suface = self.level_obj.map_surface
        self.create_jump_particles = create_jump_particles

        # World constants
        self.gravity = 0.8

        # Player movement
        self.direction = pygame.math.Vector2(0, 0)
        self.hspd = 10
        self.vspd = -20

        # Double jump
        self.can_doubleJump = True
        self.doubleJumping = False

        self.jump_count = 0

        # Dash
        self.dashing = False
        self.can_dash = True
        self.dash_spd = 5
        self.dash_duration = 120
        self.dash_cooldown = 2000

        # Player Status
        self.status = "idle"
        self.on_ground = False
        self.on_ceiling = False
        self.facing_right = True
        self.on_right = False
        self.on_left = False

        # Player combat atributes

            #Life
        self.isAlive = True
        self.max_health = 5
        self.actual_health = self.max_health

            #Healing
        self.healing = False
        self.heal_duration = 2000

            #Invincibility
        self.invincible = False
        self.invincible_duration = 1000
        self.hurt_time = 0

            #Soul
        self.max_soul = 6
        self.current_soul = self.max_soul

        # Weapon
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]

        # Wall jump
        self.on_wall = False
        #self.can_walljump = True

        # Attack
        self.attacking = False
        self.current_attack = None
        self.attack_duration = 567
        self.can_attack = True

        self.attack_direction = ""
        self.facing_up = False
        self.facing_down = False

    def createAttack(self):
        self.current_attack = Weapon(self, self.group, self.enemies)

    def destroyAttack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def ver_attack_direction(self):

        if self.facing_right:
            self.attack_direction = "right"
        elif not self.facing_right:
            self.attack_direction = "left"

        if self.facing_up:
                self.attack_direction = "up"

        if not self.on_ground:
            if self.facing_down:
                self.attack_direction = "down"

    def import_character_assets(self):
        character_path = "../graphics/character/"
        self.animations = {"idle": [], "run": [], "jump": [], "doubleJump": [], "fall": [], "wall": [], "dash": [], "heal": [], "attack/down": [], "attack/left": [], "attack/right": [], "attack/up": [] }

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)
    
    def import_dust_run_particles(self):
        self.dust_run_particles = import_folder("../graphics/character/dust_particles/run")

    def animate(self):
        animation = self.animations[self.status]

        # loop over frame index
        self.frame_index += self.animation_spd
        if self.frame_index >= len(animation):
            self.frame_index = 0
        
        image = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = image
        else:
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image
    
    def run_dust_animation(self):
        if self.status == "run" and self.on_ground:
            self.dust_frame_index += self.dust_animation_spd
            if self.dust_frame_index >= len(self.dust_run_particles):
                self.dust_frame_index = 0
            dust_particle = self.dust_run_particles[int(self.dust_frame_index)]

            if self.facing_right:
                pos = self.rect.bottomleft - pygame.math.Vector2(6, 10)
                self.display_suface.blit(dust_particle, pos)
            else:
                pos = self.rect.bottomright - pygame.math.Vector2(6, 10)
                flipped_dust_particle = pygame.transform.flip(dust_particle, True, False)
                self.display_suface.blit(flipped_dust_particle, pos)

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0

        if keys[pygame.K_z] and self.on_ground:
            self.jump(self.vspd)
            self.jump_count += 1
        elif keys[pygame.K_z] and self.on_wall:
            self.jump(self.vspd)
            self.direction.x += self.direction_wall_jump * 4
            self.jump_count += 1
        elif keys[pygame.K_z] and self.can_doubleJump:
            self.doubleJumping = True
            self.can_doubleJump = False
            self.jump_count += 1
            self.jump(-16)
        elif not keys[pygame.K_z] and (not self.on_ceiling) and self.direction.y < 0:
            self.end_jump()
        
        if keys[pygame.K_a] and not self.healing and self.current_soul >= 3:
            self.heal_start = pygame.time.get_ticks()
            self.healing = True
        
        if keys[pygame.K_c] and not self.dashing and self.can_dash:
            self.dash_start_time = pygame.time.get_ticks()
            self.dashing = True

        if keys[pygame.K_x] and self.can_attack:

            if keys[pygame.K_DOWN]:
                self.facing_up = False
                self.facing_down = True

            elif keys[pygame.K_UP]:
                self.facing_down = False
                self.facing_up = True

            elif keys[pygame.K_LEFT]:
                self.facing_right = False
            
            elif keys[pygame.K_RIGHT]:
                self.facing_right = True

            self.ver_attack_direction()
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            self.createAttack()
            self.can_attack = False
        
        if keys[pygame.K_ESCAPE]:
            self.game_state = "pause"

    def attack(self):
        if self.attacking:
            current_time = pygame.time.get_ticks()
            if current_time - self.attack_time <= self.attack_duration:
                if self.current_attack:
                    self.current_attack.animate()
                    self.current_attack.updateWeapon()

                    self.on_wall = False

                    collided_enemies = pygame.sprite.spritecollide(self.current_attack, self.enemies, False)
                    if collided_enemies:
                        for enemy in collided_enemies:
                            enemy.takeDamage()
                            self.knockback()
                            self.destroyAttack()
                            self.current_soul += 1
                    self.end_animation_attack = pygame.time.get_ticks()
            elif current_time - self.end_animation_attack >= 100:
                self.attacking = False
                self.attack_direction = " "
                self.facing_up = False
                self.facing_down = False
                self.can_attack = True
                if self.current_attack:
                    self.destroyAttack()

    def knockback(self):
        match self.attack_direction:
            case "right":
                self.direction.x -= 1
            case "left":
                self.direction.x += 1
            case "up":
                self.direction.y += 12
            case "down":
                self.jump_count = 0
                self.jump(-20)
                self.jump_count += 1

    def dash(self):
        if self.dashing:
            current_time = pygame.time.get_ticks()
            if current_time - self.dash_start_time <= self.dash_duration:
                if self.facing_right:
                    self.direction.x = 1
                    self.direction.x *= self.dash_spd

                elif not self.facing_right:
                    self.direction.x = -1
                    self.direction.x *= self.dash_spd
        
                self.direction.y -= self.gravity
                self.rect.centery -= self.direction.y

                self.on_wall = False
            else:
                self.can_dash = False
                self.dashing = False
                self.end_dash_time = pygame.time.get_ticks()
        
        if not self.can_dash:
            current_time = pygame.time.get_ticks()
            if current_time - self.end_dash_time >= self.dash_cooldown:
                self.can_dash = True

    def get_status(self):

        if self.direction.y < 0:
            self.status = "jump"
        elif self.direction.y > 1:
            self.status = "fall"
            self.doubleJumping = False
        else:
            if self.direction.x != 0:
                if self.on_ground:
                    self.status = "run"
                    self.doubleJumping = False
            elif self.on_ground:
                self.status = "idle"
                self.doubleJumping = False
        
        if self.doubleJumping:
            self.status = "doubleJump"

        if self.attacking:
            self.status = f"attack/{self.attack_direction}"

        if self.dashing:
            self.status = "dash"
        
        if self.healing:
            self.status = "heal"

        if self.on_wall:
            self.status = "wall"

    def verDoubleJump(self):
        if 0 < self.jump_count < 2 and ( (self.direction.y == 0 and not self.on_ground) or self.status == "fall" ): #(not self.on_ground and self.direction.y > 0) ):
            self.can_doubleJump = True
            self.doubleJumping = False

    def jump(self, spd):
        self.direction.y = spd
        self.on_wall = False
    
    def end_jump(self):
        self.direction.y = 0

    def applyGravity(self):
        self.direction.y += self.gravity
        self.rect.centery += self.direction.y
    
    def horizontal_collision(self):
        self.rect.centerx += self.direction.x * self.hspd

        for sprite in self.world_tiles:
            if sprite.rect.colliderect(self.rect):
                if self.direction.x > 0:
                    self.rect.right = sprite.rect.left
                    self.on_right = True
                    self.level_obj.current_x = self.rect.right
                    if self.direction.y > 0 and not self.on_ground:
                        self.on_wall = True
                        if self.rect.left <= sprite.rect.right:
                            self.facing_right = True
                            self.direction_wall_jump = -1
                
                elif self.direction.x < 0:
                    self.rect.left = sprite.rect.right
                    self.on_left = True
                    self.level_obj.current_x = self.rect.left
                    if self.direction.y > 0 and not self.on_ground:
                        self.on_wall = True
                        if self.rect.right >= sprite.rect.left:
                            self.facing_right = False
                            self.direction_wall_jump = 1

        #if self.on_right and (self.rect.right > self.level_obj.current_x or self.direction. x <= 0):
            #self.on_right = False
        #if self.on_left and (self.rect.left < self.level_obj.current_x or self.direction.x >= 0):
            #self.on_left = False

    def outsideMap(self):
        if self.rect.x > self.map_width + 10:
            self.isAlive = False
        if self.rect.y > self.map_height + 200:
            self.isAlive = False

    def wall_collision(self):

        for sprite in self.world_tiles:
            if self.rect.left <= sprite.rect.right and not self.facing_right:
                self.facing_right = True
            elif self.rect.right >= sprite.rect.left and self.facing_right:
                self.facing_right = False

        if self.on_ground and self.direction.y == 0:
            self.on_wall = False

    def while_on_wall(self):
        if self.on_wall:
            self.direction.y = 8
            #self.can_walljump = True
            self.jump_count = 0

    def vertical_collision(self):
        
        self.applyGravity()

        for sprite in self.world_tiles:
            if sprite.rect.colliderect(self.rect):
                if self.direction.y > 0:
                    self.rect.bottom = sprite.rect.top
                    self.direction.y = 0
                    self.on_ground = True

                    self.jump_count = 0
                    self.doubleJumping = False

                elif self.direction.y < 0:
                    self.rect.top = sprite.rect.bottom
                    self.direction.y = 0
                    self.on_ceiling = True

                    self.doubleJumping = False
        
        if self.on_ground and self.direction.y < 0 or self.direction.y > 1:
            self.on_ground = False
        if self.on_ceiling and self.direction.y > 0.1:
            self.on_ceiling = False

    def checkLife(self):
        if self.actual_health <= 0:
            self.isAlive = False

    def collideEnemies(self):

        collided_enemies = pygame.sprite.spritecollide(self, self.enemies, False)

        if collided_enemies:
            if not self.invincible:
                self.actual_health -= 1
                self.invincible = True
                self.hurt_time = pygame.time.get_ticks()
            self.invincibility_timer()

    def invincibility_timer(self):
        if self.invincible:
            current_time = pygame.time.get_ticks()
            if current_time - self.hurt_time >= self.invincible_duration:
                self.invincible = False

    def heal(self):
        if self.healing:
            if self.actual_health < self.max_health:
                current_time = pygame.time.get_ticks()
                self.direction.x = 0
                self.on_wall = False
                if current_time - self.heal_start >= self.heal_duration:
                    self.actual_health += 1
                    self.current_soul -= 3
                    self.healing = False

    def getSoul(self):

        collided_soul = pygame.sprite.spritecollide(self, self.bottles, True)
        if collided_soul and self.current_soul < self.max_soul:
            for soul in collided_soul:
                self.current_soul += soul.value
        
        if self.current_soul >= self.max_soul:
            self.current_soul = self.max_soul

    def update(self):
        # movement
        self.input()

        #action
        self.verDoubleJump()
        self.dash()
        self.attack()

        # animation
        self.get_status()
        self.animate()
        self.run_dust_animation()

        # Health
        self.checkLife()
        self.collideEnemies()
        self.heal()

        # collision
        self.horizontal_collision()
        self.vertical_collision()

        #Outside map
        self.outsideMap()

        # wall
        self.wall_collision()
        self.while_on_wall()

        # Soul
        self.getSoul()

        print(self.actual_health)
        print(self.status)

        print(f"if alive: {self.isAlive}")

        #print(self.can_doubleJump)

        print(self.direction.y)
        print(f"is on ground: {self.on_ground}")
        print(f"is on wall: {self.on_wall}")
        print(self.jump_count)

        #print(self.attack_direction)