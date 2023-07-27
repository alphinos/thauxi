import pygame

# Screen setup
screen_width = 1280
screen_height = 720

# Global variables
bg_color = pygame.Color("#0f070d")
accent_color = pygame.Color(152, 142, 230)
great_color = pygame.Color(200, 20, 51)

# Map setup
tile_size = 32

# Weapons
weapon_data = {
    "nail": { "cooldown": 200, "damage": 1, "graphics": "../graphics/weapon/nail" }
}