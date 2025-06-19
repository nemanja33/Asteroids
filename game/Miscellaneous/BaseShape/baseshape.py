import pygame

# Base class for game objects
class BaseShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        # we will be using this later
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def draw(self, screen):
        # sub-classes must override
        pass

    def update(self, dt):
        # sub-classes must override
        pass

    def collision(self, shape):
        is_triangle = hasattr(self, "point_in_triangle")
        if is_triangle and self.point_in_triangle(shape.position, self.triangle()):
            return True

        distance = self.position.distance_to(shape.position)
        return distance <= self.radius + shape.radius