import pygame
from game.Miscellaneous.BaseShape.baseshape import BaseShape

class Weapon(BaseShape):
    SHOT_RADIUS = 5
    def __init__(self, x, y):
        super().__init__(x, y, self.SHOT_RADIUS)

    def update(self, dt):
        pass

    def draw(self, screen):
        pass
