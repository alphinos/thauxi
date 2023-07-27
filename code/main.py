import pygame, sys

import gamemanager as gm

#General setup
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()

#gamemanager
gamemanager = gm.GameManager()

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        """if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                gamemanager.state = "menu"""

    #Game
    gamemanager.stateManager()
    if gamemanager.state == "quit":
        pygame.quit()
        sys.exit()

    print(gamemanager.state)

    #Setting
    pygame.display.update()
    clock.tick(60)
    print(clock.get_fps())