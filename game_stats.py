class GameStats():
    '''Stores statistic data of the alien invasion'''

    def __init__(self, ai_settings):
        '''Starts the statistic data'''
        self.ai_settings = ai_settings
        self.reset_stats()
        self.game_active = False

        # The maximum score must never be reset
        self.high_score = 0
        

    def reset_stats(self):
        '''Starts the statistic data that can change during the game'''
        self.ship_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
