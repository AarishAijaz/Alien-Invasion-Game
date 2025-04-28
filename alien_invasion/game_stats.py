class GameStats:
    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.reset_stats()
        self.game_active=True

    def reset_stats(self):
        self.shooters_left = self.settings.shooter_limit

    