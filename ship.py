import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    def __init__(self, ai_settings, screen):
        '''Define the first position'''
        super(Ship, self).__init__()

        self.screen = screen
        self.ai_settings = ai_settings

        # Upload image
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Start each new spaceship in the current position
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        self.center = float(self.rect.centerx)

        self.moving_right = False
        self.moving_left = False


    def update(self):
        '''Updates the position'''
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor

        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        # Updates the object
        self.rect.centerx = self.center


    def blitme(self):
        '''Draws the spaceship'''
        self.screen.blit(self.image, self.rect)

    
    def center_ship(self):
        '''Centralizes the spaceship'''
        self.center = self.screen_rect.centerx