import pygame
import random
import math
from game.BaseShape.baseshape import BaseShape
from config.constants import ASTEROID_MIN_RADIUS

class Asteroid(BaseShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.rotation = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-10, 10)  # degrees per second
        self.num_points = random.randint(8, 12)
        self.offsets = [random.uniform(0.5, 1.2) for _ in range(self.num_points)]

    def draw(self, screen):
        cx, cy = self.position
        points = []

        for i in range(self.num_points):
            base_angle = 2 * math.pi / self.num_points * i
            angle = base_angle + math.radians(self.rotation)
            varied_radius = self.radius * self.offsets[i]
            x = cx + math.cos(angle) * varied_radius
            y = cy + math.sin(angle) * varied_radius
            points.append((x, y))

        pygame.draw.polygon(screen, pygame.Color("white"), points, 2)

    def split(self, dmg):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        if (dmg >= self.radius):
            return

        rand_angle = random.uniform(20, 50)
        pos_vector = self.velocity.rotate(rand_angle)
        neg_vector = self.velocity.rotate(-rand_angle)

        new_radius = self.radius - dmg

        pos_asteroid = Asteroid(self.position[0], self.position[1], new_radius)
        neg_asteroid = Asteroid(self.position[0], self.position[1], new_radius)

        pos_asteroid.velocity = pos_vector * 1.2
        neg_asteroid.velocity = neg_vector * 1.2

    def update(self, dt):
        self.position += self.velocity * dt
        self.rotation += self.rotation_speed * dt