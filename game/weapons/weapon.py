from game.base_shape.base_shape import BaseShape

class Weapon(BaseShape):
    SHOT_RADIUS = 5
    def __init__(self, x, y):
        super().__init__(x, y, self.SHOT_RADIUS)

    def update(self, dt):
        pass

    def draw(self, screen):
        pass
    
    def shoot(self, r):
        pass
