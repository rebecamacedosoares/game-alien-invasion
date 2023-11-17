class Settings():
    '''Class to save the settings of the invasion'''
    
    def __init__(self):
        '''Start the settings of the game'''

        # Screen settings
        self.screen_width = 900
        self.screen_height = 600
        self.bg_color = (230, 230, 230)
        self.ship_speed_factor = 1.5

        # Spaceship settings
        self.ship_limit = 3

        # Bullets settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        # Settings of aliens
        self.fleet_drop_speed = 10

        # The rate that speed changes
        self.speedup_scale = 1.1

        # The rate at which the points for each alien increase
        self.score_scale = 1.5

        self.initialize_dynamic_settings()


    def initialize_dynamic_settings(self):
        '''Starts the settings that change during the game'''
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1

        # Score
        self.alien_points = 50

        # fleet_direction igual a 1 representa a direita e igual a -1 representa a esquerda
        self.fleet_direction = 1

    
    def increase_speed(self):
        '''Increases tha speed settings'''
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        
        self.alien_points = int(self.alien_points * self.score_scale)
