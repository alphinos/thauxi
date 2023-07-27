import pygame, settings, tiles
from enemy import *
from support import *
from particles import *
from level_data import *

class Level:
    def __init__(self, currentLevel, size):

        level_data = currentLevel

        # level setup
        self.map_surface = pygame.Surface(size)
        self.map_rect = self.map_surface.get_rect()
        self.current_x = 0

        # Player
        player_layout = import_csv_layout(level_data["player"])

        self.goal = pygame.sprite.Group()

        self.setupPlayer(player_layout)

        # dust
        self.dust_sprite = pygame.sprite.GroupSingle()
        self.player_on_ground = False

        # Background 2
        Background2_layout = import_csv_layout(level_data["Background2"])
        self.Background2_sprites = self.create_tile_group(Background2_layout, "Background2")

        # Background 1
        Background1_layout = import_csv_layout(level_data["Background1"])
        self.Background1_sprites = self.create_tile_group(Background1_layout, "Background1")

        # Sides 2
        #sides2_layout = import_csv_layout(level_data["sides2"])
        #self.sides2_sprites = self.create_tile_group(sides2_layout, "sides2")

        # Sides 1
        #sides1_layout = import_csv_layout(level_data["sides1"])
        #self.sides1_sprites = self.create_tile_group(sides1_layout, "sides1")

        # Upsidedown2
        #upsidedown2_layout = import_csv_layout(level_data["upsidedown2"])
        #self.upsidedown2_sprites = self.create_tile_group(upsidedown2_layout, "upsidedown2")

        # Upsidedown1
        #upsidedown1_layout = import_csv_layout(level_data["upsidedown1"])
        #self.upsidedown1_sprites = self.create_tile_group(upsidedown1_layout, "upsidedown1")

        # Terrain
        terrain_layout = import_csv_layout(level_data["terrain"])
        self.terrain_sprites = self.create_tile_group(terrain_layout, "terrain")

        # Enemy
        enemy_layout = import_csv_layout(level_data["enemy"])
        self.enemy_sprites = self.create_tile_group(enemy_layout, "enemy")

        # Constraints
        constraints_layout = import_csv_layout(level_data["constraints"])
        self.constraints_sprites = self.create_tile_group(constraints_layout, "constraints")

        # Soul
        soul_layout = import_csv_layout(level_data["soul"])
        self.soul_sprites = self.create_tile_group(soul_layout, "soul")

        # Decoration
        self.image_decoration = pygame.image.load("/home/carlitos/Projects/Pygame/game_v3/graphics/decoration/vincentiu-solomon-ln5drpv_ImI-unsplash.jpg").convert()
        self.image_decoration = pygame.transform.scale(self.image_decoration, (2560, 1440))

    def create_jump_particles(self, player):
        if player.facing_right:
            player.rect.center -= pygame.math.Vector2(10, 5)
        else:
            player.rect.center += pygame.math.Vector2(-10, 5)
        jump_particle_sprite = ParticleEffect(player.rect.center, "jump")
        self.dust_sprite.add(jump_particle_sprite)
    
    def get_player_on_ground(self, player):
        if player.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False
    
    def create_landing_dust(self, player):
        if not self.player_on_ground and player.on_ground and not self.dust_sprite.sprites():
            if player.facing_right:
                offset = pygame.math.Vector2(10, 15)
            else:
                offset = pygame.math.Vector2(-10, 15)
            fall_dust_particle = ParticleEffect(player.rect.midbottom - offset, "land")
            self.dust_sprite.add(fall_dust_particle)
    
    def setupPlayer(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if val == "0":
                    self.spawn_x = x
                    self.spawn_y = y
                if val == "1":
                    end_surface = pygame.image.load("/home/carlitos/Projects/Pygame/game_v3/graphics/character/end_thing.png").convert_alpha()
                    sprite = tiles.TeleporterBlock((tile_size, tile_size), x, y, end_surface)
                    self.goal.add(sprite)

    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != "-1":
                    x = col_index * tile_size
                    y = row_index * tile_size
                    
                    match type:

                        case "Background2":
                            Background2_tile_list = import_cut_graphics("/home/carlitos/Projects/Pygame/game_v3/graphics/terrain/props2.png")
                            tile_surface = Background2_tile_list[int(val)]
                            sprite = tiles.StaticBlock((tile_size, tile_size), x, y, tile_surface)

                        case "Background1":
                            Background1_tile_list = import_cut_graphics("/home/carlitos/Projects/Pygame/game_v3/graphics/terrain/props2.png")
                            tile_surface = Background1_tile_list[int(val)]
                            sprite = tiles.StaticBlock((tile_size, tile_size), x, y, tile_surface)
                        
                        case "sides2":
                            sides2_tile_list = import_cut_graphics("/home/carlitos/Projects/Pygame/game_v3/graphics/terrain/props1.png")
                            tile_surface = sides2_tile_list[int(val)]
                            sprite = tiles.StaticBlock((tile_size, tile_size), x, y, tile_surface)
                        
                        case "sides1":
                            sides1_tile_list = import_cut_graphics("/home/carlitos/Projects/Pygame/game_v3/graphics/terrain/props1.png")
                            tile_surface = sides1_tile_list[int(val)]
                            sprite = tiles.StaticBlock((tile_size, tile_size), x, y, tile_surface)
                        
                        case "upsidedown2":
                            upsidedown_2_tile_list = import_cut_graphics("/home/carlitos/Projects/Pygame/game_v3/graphics/terrain/props1.png")
                            tile_surface = upsidedown_2_tile_list[int(val)]
                            sprite = tiles.StaticBlock((tile_size, tile_size), x, y, tile_surface)
                        
                        case "upsidedown1":
                            upsidedown_1_tile_list = import_cut_graphics("/home/carlitos/Projects/Pygame/game_v3/graphics/terrain/props1.png")
                            tile_surface = upsidedown_1_tile_list[int(val)]
                            sprite = tiles.StaticBlock((tile_size, tile_size), x, y, tile_surface)
                        
                        case "terrain":
                            terrain_tile_list = import_cut_graphics("/home/carlitos/Projects/Pygame/game_v3/graphics/terrain/mainlev_build_v2.png")
                            tile_surface = terrain_tile_list[int(val)]
                            sprite = tiles.StaticBlock((tile_size, tile_size), x, y, tile_surface)

                        case "enemy":
                            sprite = Enemy(32, 64, x, y, "/home/carlitos/Projects/Pygame/game_v3/graphics/enemy")
                        
                        case "constraints":
                            sprite = tiles.Block((tile_size, tile_size), x, y)
                        
                        case "soul":
                            sprite = tiles.Soul((tile_size, tile_size), x, y)
                    
                    sprite_group.add(sprite)
                    
        return sprite_group

    def enemy_collision_reverse(self):
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.constraints_sprites, False):
                enemy.reverse()
    
    def run(self):

        self.map_surface.blit(self.image_decoration, (640, 0))

        self.Background2_sprites.draw(self.map_surface)
        self.Background1_sprites.draw(self.map_surface)

        #self.sides2_sprites.draw(self.map_surface)
        #self.sides1_sprites.draw(self.map_surface)

        #self.upsidedown2_sprites.draw(self.map_surface)
        #self.upsidedown1_sprites.draw(self.map_surface)

        self.terrain_sprites.draw(self.map_surface)

        self.enemy_sprites.update()
        self.enemy_collision_reverse()
        self.enemy_sprites.draw(self.map_surface)

        self.soul_sprites.draw(self.map_surface)

        #self.goal.draw(self.map_surface)