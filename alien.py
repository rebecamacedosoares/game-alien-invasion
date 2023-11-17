import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    '''Class that represents only one alien'''

    def __init__(self, ai_settings, screen):
        '''Starts the alien and defines the position'''
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Upload the image of the alien and defines rect
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # Starts each new alien on top lef
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Saves the exact position of the alien
        self.x = float(self.rect.x)


    def blitme(self):
        '''Draws the alien in the current position'''
        self.screen.blit(self.image, self.rect)


    def check_edges(self):
        '''Returns True if the alien is on the border of the screen'''
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True


    def update(self):
        '''Moves the alien to the right and to the left'''
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x
