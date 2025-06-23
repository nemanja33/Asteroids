import pygame

class BaseShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def draw(self, screen):
        pass

    def update(self, dt):
        pass

    def collision(self, shape):
        is_triangle = hasattr(self, "triangle_collision")
        if is_triangle and self.triangle_collision(shape.position, self.triangle()):
            return True

        distance = self.position.distance_to(shape.position)
        
        return distance <= self.radius + shape.radius