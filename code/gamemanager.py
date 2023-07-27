import pygame, settings, sys

import level, camera, player

from DeathWin import *

from level_data import *

from menu import *

from pause import *

from sound import *

class GameManager:
    def __init__(self):

        #main screen
        self.screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))

        icon = pygame.image.load("../graphics/hud/mask.png").convert_alpha()

        pygame.display.set_icon(icon)
        pygame.display.set_caption("Thauxi")

        self.state = "start"
        self.index_level = 0
        self.max_level = len(levels) - 1
        self.current_level = levels[self.index_level]

        self.player = None

        self.maintain_hp = 5
        self.maintain_soul = 6

    def createLevel(self, current_level):
        
        if current_level == level_1:
            self.level = self.level1
        elif current_level == level_2:
            self.level = self.level2

        #camera
        self.camera_group = camera.CameraGroup()

        #player
        self.player = player.Player(self.level.spawn_x, self.level.spawn_y, self.camera_group, self.level, self.level.create_jump_particles)
    
    def createMenu(self):
        self.menu = Menu()
        self.state = "menu"

    def runLevel(self):
        self.screen.fill(settings.bg_color)

        #dust particles
        self.level.dust_sprite.update(self.camera_group.offset.x)

        self.camera_group.update()
        self.camera_group.renderScreen(self.level, self.player)

    def checkNextLevel(self):
        if pygame.sprite.spritecollide(self.player, self.player.goal, False):
            if self.index_level < self.max_level:
                self.index_level += 1
                self.current_level = levels[self.index_level]
                self.state = "loading"
            else:
                self.index_level = 0
                self.state = "win"
                self.menu.state = "menu"

    def checkDeathPlayer(self):
        if not self.player.isAlive:
            self.state = "dead"
            self.index_level = 0

    def stateManager(self):

        if self.state == "start":

            # Load levels
            self.level1 = level.Level(level_1, (3840, 1440) )
            self.level2 = level.Level(level_2, (3840, 1440) )

            #Load pause
            self.pause = Pause()

            #Screens
            self.dead_screen = death()
            self.win_screen = win()

            #sound
            self.songs = Music(self.state)

            self.createMenu()
            self.index_level = 0

        elif self.state == "menu":
            self.menu.run()
            self.screen.blit(self.menu.menu_surface, (0, 0))
            self.state = self.menu.state

            self.dead_screen.state = "dead"
            self.win_screen.state = "win"

            if self.player:
                self.player.game_state = "level"
            
            self.maintain_hp = 5
            self.maintain_soul = 6


        elif self.state == "loading":
            
            self.current_level = levels[self.index_level]
            self.createLevel(self.current_level)

            self.player.actual_health = self.maintain_hp
            self.player.current_soul = self.maintain_soul

            self.player.game_state = "level"

            self.state = "level"
            self.dead_screen.state = "dead"
            self.win_screen.state = "win"

        elif self.state == "level":
            self.maintain_hp = self.player.actual_health
            self.maintain_soul = self.player.current_soul
            self.state = self.player.game_state
            self.pause.state = "pause"
            self.menu.state = "menu"
            self.runLevel()
            self.checkDeathPlayer()
            self.checkNextLevel()

        elif self.state == "restart":

            # Load levels
            self.level1 = level.Level(level_1, (3840, 1440) )
            self.level2 = level.Level(level_2, (3840, 1440) )

            self.state = "loading"
            self.menu.state = "menu"

        elif self.state == "pause":
            self.state = self.pause.state
            self.player.game_state = self.state
            self.menu.state = self.pause.state
            self.pause.run()
            self.screen.blit(self.pause.surface, (0, 0) )

        elif self.state == "dead":
            self.state = self.dead_screen.state
            self.player.game_state = self.state
            self.menu.state = self.dead_screen.state
            self.dead_screen.run()
            self.screen.blit(self.dead_screen.surface, (0, 0) )
            self.player.actual_health = 1
            self.player.isAlive = True
        
        elif self.state == "win":
            self.state = self.win_screen.state
            self.player.game_state = self.state
            self.menu.state = self.win_screen.state
            self.win_screen.run()
            self.screen.blit(self.win_screen.surface, (0, 0) )

        elif self.state == "quit":
            pygame.quit()
            sys.exit()
        
        self.songs.playSong(self.state)

        print(self.state)