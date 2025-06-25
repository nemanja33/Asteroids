import pygame
import os

from random import randint
from game.powerup.powerup import PowerUp

class Shield(PowerUp):
    def __init__(self):
        super().__init__(
            amount=0,
            image=pygame.transform.scale(
                pygame.image.load(
                    os.path.join(os.path.dirname(__file__), "shield.png")
                ),
                (30, 30)
            ),
            x=randint(5, pygame.display.get_surface().get_width() - 5),
            y=-15,
            velocity=(0, 200),
            radius=30
        )