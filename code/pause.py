import pygame, sys
from tiles import Button
from settings import great_color


class Pause:
    def __init__(self):

        #Basic setup
        self.paused = True
        self.surface = pygame.surface.Surface( (1280, 720) )

        # State
        self.state = "pause"

        #Background
        self.background = pygame.image.load("../graphics/pause/background.jpg").convert()
        self.background = pygame.transform.scale(self.background, (1280, 720) )

        #Buttons
        self.continueButton = Button( (490, 100), 395, 260 )
        self.menuButton = Button( (270, 100), 495, 370 )
        self.quitButton = Button( (226, 100), 520, 480 )

        #Text
        fontText = pygame.font.Font("../fonts/Gaeilge.ttf", 100)

        self.continueText = fontText.render("CONTINUE", False, great_color)
        self.menuText = fontText.render("MENU", False, great_color)
        self.quitText = fontText.render("QUIT", False, great_color)

    def input(self):
        mousepos = pygame.mouse.get_pos()
        mouse_get_pressed = pygame.mouse.get_pressed()

        if mouse_get_pressed[0] == 1 and self.continueButton.rect.collidepoint(mousepos[0], mousepos[1]):
            self.state = "level"
        
        if mouse_get_pressed[0] == 1 and self.menuButton.rect.collidepoint(mousepos[0], mousepos[1]):
            self.state = "menu"

        if mouse_get_pressed[0] == 1 and self.quitButton.rect.collidepoint(mousepos[0], mousepos[1]):
            self.state = "quit"

    def run(self):

        #Pause
        self.input()

        self.surface.blit(self.background, (0, 0) )

        self.surface.blit(self.continueText, self.continueButton.rect)
        self.surface.blit(self.menuText, self.menuButton.rect)
        self.surface.blit(self.quitText, self.quitButton.rect)