import sys
import pygame #python -m pygame --version #pip install pygame
from settings import Settings
from alien_shooter import Shooter
from bullet import Bullet
from human import Human
from time import sleep
from game_stats import GameStats

class AlienInvasion:
    def __init__(self):
        pygame.init()
        self.settings=Settings()

        
        #self.screen=pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.settings.screen_width=self.screen.get_rect().width
        self.settings.screen_height=self.screen.get_rect().height
        
        pygame.display.set_caption("Alien Invasion")
        self.stats = GameStats(self)
        self.shooter=Shooter(self)
        self.bullets=pygame.sprite.Group()
        self.humans=pygame.sprite.Group()

        self._create_fleet()

    def run_game(self):
        while True:
            self._check_events()
            if self.stats.game_active:
                self.shooter.update()
                self._update_bullets()
                self._update_humans()
            self._update_screen()

    def _create_fleet(self):
        human=Human(self)
        human_width, human_height = human.rect.size
        available_space_x = self.settings.screen_width - (2 * human_width)
        number_humans_x = available_space_x // (2 * human_width)
        
        shooter_height = self.shooter.rect.height
        available_space_y = (self.settings.screen_height -(3 * human_height) - shooter_height)
        number_rows = available_space_y // (2 * human_height)
        
        for row_number in range(number_rows):
            for human_number in range(number_humans_x):
                self._create_human(human_number,row_number)

    def _create_human(self,human_number,row_number):
        human = Human(self)
        human_width,human_height = human.rect.size
        human.x = human_width + 2 * human_width * human_number
        human.rect.x = human.x
        human.rect.y=human_height+2*human.rect.height*row_number
        self.humans.add(human)


    def _fire_bullet(self):
        if len(self.bullets)<self.settings.bullets_allowed:
            new_bullet=Bullet(self)
            self.bullets.add(new_bullet)
    
    def _shooter_hit(self):
        if self.stats.shooters_left>0:
            self.stats.shooters_left-=1
            self.humans.empty()
            self.bullets.empty()
            self._create_fleet()
            self.shooter.center_shooter()

            sleep(0.5)
        else:
            self.stats.game_active=False

    def _check_humans_bottom(self):
        screen_rect = self.screen.get_rect()
        for human in self.humans.sprites():
            if human.rect.bottom >= screen_rect.bottom:
                self._shooter_hit()
                break

    def _change_fleet_direction(self):
        for human in self.humans.sprites():
            human.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_fleet_edges(self):
        for human in self.humans.sprites():
            if human.check_edges():
                self._change_fleet_direction()
                break

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type==pygame.KEYUP:
                self._check_keyup_events(event)


    def _check_keydown_events(self,event):
        if event.key == pygame.K_RIGHT:
            self.shooter.moving_right=True
        elif event.key == pygame.K_LEFT:
            self.shooter.moving_left=True
        elif event.key==pygame.K_q:
            sys.exit()
        elif event.key==pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self,event):
        if event.key==pygame.K_RIGHT:
            self.shooter.moving_right=False
        elif event.key==pygame.K_LEFT:
            self.shooter.moving_left=False 

    def _check_bullet_human_collisions(self):
        collisions=pygame.sprite.groupcollide(self.bullets,self.humans,True,True)
        if not self.humans:
            self.bullets.empty()
            self._create_fleet()

    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom<=0:
                self.bullets.remove(bullet)
        self._check_bullet_human_collisions()

    def _update_humans(self):
        self._check_fleet_edges()
        self.humans.update()
        if pygame.sprite.spritecollideany(self.shooter,self.humans):
            self._shooter_hit()
        self._check_humans_bottom()

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.shooter.draw_img()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.humans.draw(self.screen)
        
        pygame.display.flip()


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
