import pygame
import os

class Bomb(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.velocity = pygame.Vector2(0, 500)
        self.image = pygame.transform.scale(
            pygame.image.load(
                os.path.join(os.path.dirname(__file__), "bomb.png")
            ),
            (30, 30)
        )
        self.rect = self.image.get_rect(center=(x, y))
        self.damage = 100
        
    def get_amount(self):
        return self.amount
    
    def draw(self, screen):
        print(self.image, self.rect.center)
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