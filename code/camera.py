import pygame, settings

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        # Camera offset
        self.offset = pygame.math.Vector2(0, 0)
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2

        # hud details
        self.hud = pygame.image.load("../graphics/hud/hud_v1.png").convert_alpha()
        self.mask = pygame.image.load("../graphics/hud/mask.png").convert_alpha()
        self.soul = pygame.image.load("../graphics/hud/soul.png").convert_alpha()

    def draw_hud(self, player):

        actual_health = player.actual_health
        current_soul = player.current_soul

        self.display_surface.blit(self.hud, (20, 20))

        match actual_health:

            case 1:
                self.display_surface.blit(self.mask, (121, 90))
            case 2:
                self.display_surface.blit(self.mask, (121, 90))
                self.display_surface.blit(self.mask, (163, 90))
            case 3:
                self.display_surface.blit(self.mask, (121, 90))
                self.display_surface.blit(self.mask, (163, 90))
                self.display_surface.blit(self.mask, (205, 90))
            case 4:
                self.display_surface.blit(self.mask, (121, 90))
                self.display_surface.blit(self.mask, (163, 90))
                self.display_surface.blit(self.mask, (205, 90))
                self.display_surface.blit(self.mask, (247, 90))
            case 5:
                self.display_surface.blit(self.mask, (121, 90))
                self.display_surface.blit(self.mask, (163, 90))
                self.display_surface.blit(self.mask, (205, 90))
                self.display_surface.blit(self.mask, (247, 90))
                self.display_surface.blit(self.mask, (289, 90))
            case 6:
                self.display_surface.blit(self.mask, (121, 90))
                self.display_surface.blit(self.mask, (163, 90))
                self.display_surface.blit(self.mask, (205, 90))
                self.display_surface.blit(self.mask, (247, 90))
                self.display_surface.blit(self.mask, (289, 90))
                self.display_surface.blit(self.mask, (289, 90))
        match current_soul:
            case 1:
                self.display_surface.blit(self.soul, (123, 127))
            case 2:
                self.display_surface.blit(self.soul, (123, 127))
                self.display_surface.blit(self.soul, (149, 127))
            case 3:
                self.display_surface.blit(self.soul, (123, 127))
                self.display_surface.blit(self.soul, (149, 127))
                self.display_surface.blit(self.soul, (175, 127))
            case 4:
                self.display_surface.blit(self.soul, (123, 127))
                self.display_surface.blit(self.soul, (149, 127))
                self.display_surface.blit(self.soul, (175, 127))
                self.display_surface.blit(self.soul, (201, 127))
            case 5:
                self.display_surface.blit(self.soul, (123, 127))
                self.display_surface.blit(self.soul, (149, 127))
                self.display_surface.blit(self.soul, (175, 127))
                self.display_surface.blit(self.soul, (201, 127))
                self.display_surface.blit(self.soul, (227, 127))
            case 6:
                self.display_surface.blit(self.soul, (123, 127))
                self.display_surface.blit(self.soul, (149, 127))
                self.display_surface.blit(self.soul, (175, 127))
                self.display_surface.blit(self.soul, (201, 127))
                self.display_surface.blit(self.soul, (227, 127))
                self.display_surface.blit(self.soul, (253, 127))

    def center_camera_target(self, target):
        self.offset.x = target.rect.centerx - self.half_w
        self.offset.y = target.rect.centery - self.half_h
    
    def renderScreen(self, level, player):

        # Camera func
        self.center_camera_target(player)

        self.display_surface.fill(settings.bg_color)

        # Ground
        ground_offset = level.map_rect.topleft - self.offset

        self.display_surface.blit(level.map_surface, ground_offset)
        level.map_surface.fill(settings.bg_color)

        level.run()

        # Particles
        level.dust_sprite.draw(self.display_surface)

        # Active elements
        for sprite in self.sprites():
            offset_pos = sprite.rect.center - self.offset - (48, 58)
            self.display_surface.blit(sprite.image, offset_pos)
        
        self.draw_hud(player)