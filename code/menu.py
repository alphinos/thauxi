import pygame
from settings import *
from tiles import *

class Menu:
    def __init__(self):

        self.menu_surface = pygame.Surface((screen_width, screen_height))

        self.background = pygame.image.load("/home/carlitos/Projects/Pygame/game_v3/graphics/menu/menu_wallpaper.jpeg").convert()
        self.background = pygame.transform.scale(self.background, (1280, 720))

        fontTitle = pygame.font.Font("../fonts/Gaeilge.ttf", 194)
        fontText = pygame.font.Font("../fonts/Gaeilge.ttf", 100)

        self.Title = fontTitle.render("THAUXI", False, settings.great_color)

        self.TitleRect = self.Title.get_size()

        self.Play = fontText.render("PLAY", False, settings.great_color)
        self.Quit = fontText.render("QUIT", False, settings.great_color)

        self.PlayRect = self.Play.get_rect()
        self.QuitRect = self.Quit.get_rect()

        self.logo = pygame.image.load("/home/carlitos/Projects/Pygame/game_v3/graphics/menu/Thauxi logo.png")
        self.logo = pygame.transform.scale(self.logo, (800, 360))

        self.playButton = Button((220, 100), 530, 470 )
        self.quitButton = Button((226, 100), 530, 580 )

        self.buttons = pygame.sprite.Group()
        self.buttons.add(self.playButton)
        self.buttons.add(self.quitButton)

        self.state = "menu"

    def input(self):
        mousepos = pygame.mouse.get_pos()
        mouse_get_pressed = pygame.mouse.get_pressed()

        if mouse_get_pressed[0] == 1 and self.playButton.rect.collidepoint(mousepos[0], mousepos[1]):
            self.state = "loading"
        
        if mouse_get_pressed[0] == 1 and self.quitButton.rect.collidepoint(mousepos[0], mousepos[1]):
            self.state = "quit"

    def run(self):

        self.input()

        self.menu_surface.blit(self.background, (0, 0))

        self.menu_surface.blit(self.logo, (240, 10))

        #self.buttons.draw(self.menu_surface)

        self.menu_surface.blit(self.Title, (307, 120))
        self.menu_surface.blit(self.Play, (530, 470))
        self.menu_surface.blit(self.Quit, (530, 580))