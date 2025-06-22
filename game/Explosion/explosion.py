import pygame
import os

class Explosion(pygame.sprite.Sprite):
  def __init__(self, x, y):
    pygame.sprite.Sprite.__init__(self)
    self.images = []

    script_dir = os.path.dirname(__file__)
    images_dir = os.path.join(script_dir, "images")

    for num in range(1, 6):
      img_path = os.path.join(images_dir, f"exp{num}.png")
      img = pygame.image.load(img_path)
      img = pygame.transform.scale(img, (75, 75))
      self.images.append(img)
  
    self.index = 0
    self.image = self.images[self.index]
    self.rect = self.image.get_rect()
    self.rect.center = [x, y]
    self.counter = 0

  def update(self):
    explosion_speed = 4

    self.counter += 1
    
    if (self.counter >= explosion_speed
        and self.index < len(self.images) - 1):
      self.counter = 0
      self.index += 1
      self.image = self.images[self.index]
    
    if (self.index >= len(self.images) - 1
        and self.counter >= explosion_speed):
      self.kill()