from config.constants import PLAYER_SHOOT_SPEED
from game.weapons.weapon import Weapon
from game.weapons.base_gun import BaseGun
import pygame

class TripleGun(Weapon):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.dmg = 20

    def shoot(self, rotation):
        angles = [10, 0, -10]
        forward = pygame.Vector2(0, 1)
        side = pygame.Vector2(1, 0).rotate(rotation) * 20

        positions = [
            self.position - side,
            self.position,
            self.position + side
        ]

        for angle, pos in zip(angles, positions):
            dir = forward.rotate(rotation + angle)
            bullet = BaseGun(pos.x, pos.y)
            bullet.velocity = dir * PLAYER_SHOOT_SPEED
            bullet.rotation = rotation + angle
