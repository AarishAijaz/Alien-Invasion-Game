import pygame

class Shooter:
    def __init__(self,ai_game):
        self.screen=ai_game.screen
        self.settings=ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        self.image = pygame.image.load('C:/Users/Admin/Desktop/self_python/alien_invasion/images/alien_shooter.bmp')
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom
        self.x=float(self.rect.x)
        self.moving_right=False
        self.moving_left=False

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x+=self.settings.shooter_speed
        if self.moving_left and self.rect.left > 0:
            self.x-=self.settings.shooter_speed
        self.rect.x=self.x

    def draw_img(self):
        self.screen.blit(self.image, self.rect)

    def center_shooter(self):
        self.rect.midbottom=self.screen_rect.midbottom
        self.x=float(self.rect.x)