import pygame
import os

from game.powerup.powerup import PowerUp

class Bomb(PowerUp):
    def __init__(self, x, y):
        super().__init__(
            amount=3,
            velocity=pygame.Vector2(0, 500),
            image=pygame.transform.scale(
                pygame.image.load(
                    os.path.join(os.path.dirname(__file__), "bomb.png")
                ),
                (30, 30)
            ),
            x=x,
            y=y,
        )
        self.damage = 100
    
    def draw(self, screen):
        screen.blit(self.image, self.rect.center)
        
    def update(self, dt):
        delta = self.velocity * dt
        self.rect.x += delta.x
        self.rect.y += delta.y
        
        if (self.rect.right < -10 or
            self.rect.left > pygame.display.get_surface().get_width() + 20 or
            self.rect.bottom < -10 or
            self.rect.top > pygame.display.get_surface().get_height() + 20):
            self.kill()
            
    def collision(self, obj):
        distance = obj.position.distance_to(self.rect.center)
        return distance <= 30 + obj.radius