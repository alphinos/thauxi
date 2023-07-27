import pygame

class Music:
    def __init__(self, state):

        self.main_volume = 0.3

        self.enteringThauxi = pygame.mixer.Sound("../audio/ost-hollowknight/Hollow_Knight_OST_-_Enter_Hallownes_(getmp3.pro).ogg")
        self.enteringThauxi.set_volume(self.main_volume)
    
        self.queensGarden = pygame.mixer.Sound("../audio/ost-hollowknight/Hollow_Knight_OST_-_Queens_Gardens_(getmp3.pro).ogg")
        self.queensGarden.set_volume(self.main_volume)

        self.city_of_Tears = pygame.mixer.Sound("../audio/ost-hollowknight/Hollow_Knight_OST_-_City_of_Tears_(getmp3.pro).ogg")
        self.city_of_Tears.set_volume(self.main_volume)

        self.deathDirtmouth = pygame.mixer.Sound("../audio/ost-hollowknight/Hollow_Knight_OST_-_Dirtmouth_(getmp3.pro).ogg")
        self.deathDirtmouth.set_volume(self.main_volume)

        self.winDungDefender = pygame.mixer.Sound("../audio/ost-hollowknight/Hollow_Knight_OST_-_Dung_Defender_(getmp3.pro).ogg")
        self.winDungDefender.set_volume(self.main_volume)

        self.isPlayingSound = False
        self.actualState = state

        self.channel = pygame.mixer.Channel(1)

    def playSong(self, state):
            match state:
                case "menu":
                    currentSong = self.enteringThauxi
                case "level":
                    currentSong = self.queensGarden
                case "pause":
                    currentSong = self.city_of_Tears
                case "win":
                    currentSong = self.winDungDefender
                case "dead":
                    currentSong = self.deathDirtmouth
                case _:
                    currentSong = self.enteringThauxi
            
            currentSongState = state
            
            if not self.isPlayingSound:
                self.channel.play(currentSong, -1, 0, 500)
                self.actualState = currentSongState
                self.isPlayingSound = True
            elif self.isPlayingSound and currentSongState != self.actualState:
                self.channel.fadeout(1500)
                self.actualState = currentSongState
                self.isPlayingSound = False