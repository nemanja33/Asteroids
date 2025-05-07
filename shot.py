import pygame
from circleshape import CircleShape

class Shot(CircleShape):
    SHOT_RADIUS = 5
    def __init__(self, x, y):
        super().__init__(x, y, self.SHOT_RADIUS)

    def update(self, dt):
        self.position += self.velocity * dt

    def draw(self, screen):
        pygame.draw.circle(screen, pygame.Color("white"), self.position, self.SHOT_RADIUS, 2)
