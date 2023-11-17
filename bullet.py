import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    '''Manages the bullets from the ship'''

    def __init__(self, ai_settings, screen, ship):
        '''Creates an object to the bullet in the current position of the ship'''
        super(Bullet, self).__init__()
        self.screen = screen


        # Creates a rectangle to the bullet in (0,0) and next it defines the right position
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # Saves the bullet's position as a decimal
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor


    def update(self):
        '''Moves the bullet up the screen'''

        # Updates the position of the bulelt
        self.y -= self.speed_factor

        # Updates the position of rect
        self.rect.y = self.y


    def draw_bullet(self):
        '''Draws the bullet'''

        pygame.draw.rect(self.screen, self.color, self.rect)
