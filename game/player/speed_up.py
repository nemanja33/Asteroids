import os
from random import randint
import pygame

from config.constants import SCREEN_HEIGHT, SCREEN_WIDTH

class SpeedUp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.amount = 1
        # down movement
        self.velocity = pygame.Vector2(0,200) 
        self.radius = 30
        self.image = pygame.transform.scale(
            pygame.image.load(
                os.path.join(os.path.dirname(__file__), "speed-up.png")
            ),
            (30, 30)
        )
        self.rect = self.image.get_rect(center=(randint(5, SCREEN_WIDTH - 5), -15))
        
    def get_amout(self):
        return self.amount

    def set_amount(self):
        self.amount = 1
        
    def update(self, dt):
        delta = self.velocity * dt
        self.rect.x += delta.x
        self.rect.y += delta.y

        if (self.rect.right < -10 or
            self.rect.left > SCREEN_WIDTH + 20 or
            self.rect.bottom < -10 or
            self.rect.top > SCREEN_HEIGHT + 20):
            self.kill()

        
    def draw(self, screen):
       screen.blit(self.image, self.rect.center)
       
    def collision(self, p):
        distance = p.position.distance_to(self.rect.center)
        return distance <= self.radius + p.radius
    