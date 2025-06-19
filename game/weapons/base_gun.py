from config.constants import SCREEN_HEIGHT, SCREEN_WIDTH
from game.weapons.weapon import Weapon
import pygame

class BaseGun(Weapon):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.dmg = 20

    def update(self, dt):
        self.position += self.velocity * dt

    def draw(self, screen):
        pygame.draw.circle(screen, pygame.Color("white"), self.position, self.SHOT_RADIUS, 2)
        if (self.position[0] > SCREEN_WIDTH + 20
            or self.position[1] > SCREEN_HEIGHT + 20
            or self.position[0] < -10
            or self.position[1] < -10):
            self.kill()