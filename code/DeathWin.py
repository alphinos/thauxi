import pygame, sys
from tiles import Button
from settings import great_color
from support import import_folder

class death:
    def __init__(self):

        #Basic setup
        self.dead = True
        self.surface = pygame.surface.Surface( (1280, 720) )

        #Animation setup
        self.importDeathAssets()
        self.frame_index = 0
        self.animation_creation_spd = 0.06
        self.animation_gif_spd = 0.06
        self.image = self.animations["creation"][self.frame_index]

        self.animation_status = "creation"

        #State
        self.state = "dead"

        #Background
        self.background = pygame.image.load("../graphics/death/death_images/death_bg.jpg").convert()
        self.background = pygame.transform.scale(self.background, (1280, 720) )

        #Buttons
        #self.restartButton = Button( (222, 50), 529, 466 )
        self.menuButton = Button( (136, 50), 374, 576 )
        self.quitButton = Button( (134, 50), 373, 636 )

        #Text
        fontText = pygame.font.Font("../fonts/Gaeilge.ttf", 50)

        self.restartText = fontText.render("RESTART", False, great_color)
        self.menuText = fontText.render("MENU", False, great_color)
        self.quitText = fontText.render("QUIT", False, great_color)

    def importDeathAssets(self):
        death_path = "../graphics/death/"
        self.animations = { "creation": [], "gif": [] }

        for animation in self.animations.keys():
            full_path = death_path + animation
            self.animations[animation] = import_folder(full_path)
    
    def animate(self):
        animation = self.animations[self.animation_status]

        if self.animation_status == "creation":
            self.frame_index += self.animation_creation_spd
            if self.frame_index >= len(animation):
                self.animation_status = "gif"
        if self.animation_status == "gif":
            # loop over frame index
            self.frame_index += self.animation_gif_spd
            if self.frame_index >= len(animation):
                self.frame_index = 0
        
        self.image = animation[int(self.frame_index)]

    def input(self):
        mousepos = pygame.mouse.get_pos()
        mouse_get_pressed = pygame.mouse.get_pressed()

        #if mouse_get_pressed[0] == 1 and self.restartButton.rect.collidepoint(mousepos[0], mousepos[1]):
            #self.state = "restart"
        
        if mouse_get_pressed[0] == 1 and self.menuButton.rect.collidepoint(mousepos[0], mousepos[1]):
            self.state = "menu"

        if mouse_get_pressed[0] == 1 and self.quitButton.rect.collidepoint(mousepos[0], mousepos[1]):
            self.state = "quit"

    def run(self):

        #Pause
        self.input()

        self.surface.blit(self.background, (0, 0) )

        #self.surface.blit(self.restartText, self.restartButton.rect)
        self.surface.blit(self.menuText, self.menuButton.rect)
        self.surface.blit(self.quitText, self.quitButton.rect)

        #Animation
        self.animate()
        self.surface.blit(self.image, (448, 0) )


class win:
    def __init__(self):

        #Basic setup
        self.winner= True
        self.surface = pygame.surface.Surface( (1280, 720) )

        #State
        self.state = "win"

        #Background
        self.background = pygame.image.load("../graphics/win/godmaster_wallpaper.png").convert()
        self.background = pygame.transform.scale(self.background, (1280, 720) )

        #Buttons
        self.restartButton = Button( (222, 50), 529, 466 )
        self.menuButton = Button( (136, 50), 574, 526 )
        self.quitButton = Button( (134, 50), 573, 586 )

        #Text
        fontTitle = pygame.font.Font("../fonts/Gaeilge.ttf", 194)
        fontText = pygame.font.Font("../fonts/Gaeilge.ttf", 50)

        self.winnnerTitle = fontTitle.render("VENCEDOR", False, great_color)

        self.winnner_rect = self.winnnerTitle.get_rect( center = (640, 360 ))

        self.restartText = fontText.render("RESTART", False, great_color)
        self.menuText = fontText.render("MENU", False, great_color)
        self.quitText = fontText.render("QUIT", False, great_color)

    def input(self):
        mousepos = pygame.mouse.get_pos()
        mouse_get_pressed = pygame.mouse.get_pressed()

        if mouse_get_pressed[0] == 1 and self.restartButton.rect.collidepoint(mousepos[0], mousepos[1]):
            self.state = "loading"
        
        if mouse_get_pressed[0] == 1 and self.menuButton.rect.collidepoint(mousepos[0], mousepos[1]):
            self.state = "menu"

        if mouse_get_pressed[0] == 1 and self.quitButton.rect.collidepoint(mousepos[0], mousepos[1]):
            self.state = "quit"

    def run(self):

        #Pause
        self.input()

        self.surface.blit(self.background, (0, 0) )

        self.surface.blit(self.restartText, self.restartButton.rect)
        self.surface.blit(self.menuText, self.menuButton.rect)
        self.surface.blit(self.quitText, self.quitButton.rect)

        self.surface.blit(self.winnnerTitle, self.winnner_rect)