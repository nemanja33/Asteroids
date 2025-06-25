import pygame
import os

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, image, x, y , amount, velocity=(0, 200), radius=30):
        super().__init__()
        self.amount = amount
        self.velocity = pygame.Vector2(*velocity)
        self.radius = radius
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        
    def get_amount(self):
        return self.amount
    
    def set_amount(self, amount):
        self.amount = amount
    
    def increase_amount(self, x):
        self.amount += x
        
    def decrease_amount(self, x):
        self.amount -= x
        

    def update(self, dt):
        delta = self.velocity * dt
        self.rect.x += delta.x
        self.rect.y += delta.y

        if (self.rect.right < -10 or
            self.rect.left > pygame.display.get_surface().get_width() + 20 or
            self.rect.bottom < -10 or
            self.rect.top > pygame.display.get_surface().get_height() + 20):
            self.kill()
            
    def draw(self, screen):
        screen.blit(self.image, self.rect.center)
        
    def collision(self, player):
        distance = player.position.distance_to(self.rect.center)
        return distance <= self.radius + player.radius