from config.constants import PLAYER_SHOOT_SPEED
from game.weapons.weapon import Weapon
from game.weapons.base_gun import BaseGun
import pygame

class DoubleGun(Weapon):
    def __init__(self, x, y):
        super().__init__(x, y)

    def shoot(self, rotation):
        forward = pygame.Vector2(0, 1).rotate(rotation)
        side = pygame.Vector2(1, 0).rotate(rotation) * 20

        positions = [self.position - side, self.position + side]

        for pos in positions:
            bullet = BaseGun(pos.x, pos.y)
            bullet.velocity = forward * PLAYER_SHOOT_SPEED
            bullet.rotation = rotation
