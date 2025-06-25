from config.constants import PLAYER_SHOOT_SPEED
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
        if (self.position[0] > pygame.display.get_surface().get_width() + 20
            or self.position[1] > pygame.display.get_surface().get_height() + 20
            or self.position[0] < -10
            or self.position[1] < -10):
            self.kill()
            
    def shoot(self, r):
        self.velocity = pygame.Vector2(0, 1).rotate(r) * PLAYER_SHOOT_SPEED