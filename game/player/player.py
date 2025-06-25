import pygame
import math
from game.base_shape.base_shape import BaseShape
from game.player.shield.shield import Shield
from game.player.speed_up.speed_up import SpeedUp
from game.weapons.base_gun import BaseGun
from config.constants import *

class Player(BaseShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.lives = 2
        self.shoot_timer = 0
        self.accelerate = 1
        self.respawn_cd = 0
        self.speed_reset_time = 0
        self.gun = BaseGun
        self.speed_up = SpeedUp()
        self.shield = Shield()

    def get_lives(self):
        return self.lives

    def reduce_lives(self):
        self.lives -= 1
    
    def get_gun(self):
        return self.gun

    def set_gun(self, gun):
        self.gun = gun
        
    def get_cd(self):
        return self.respawn_cd
    
    def get_shield(self):
        return self.shield
    
    def set_shield(self, shield):
        self.shield = shield
        
    def get_speed_up(self):
        return self.speed_up
    
    def set_speed_up(self, speed_up):
        self.speed_up = speed_up
    
    def increse_cd(self, x):
        self.respawn_cd = x
    
    def decrease_cd(self, dt, x):
        self.respawn_cd -= dt * x

    def respawn(self):
        self.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.accelerate = 1
        
    def set_acceleration(self, a):
        self.speed_reset_time = 5000
        self.speed_up.increase_amount(a)
        
    def draw(self, screen):
        triangle_points = self.triangle()

        surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

        if self.get_cd() > 0:
            t = pygame.time.get_ticks()
            flicker = int((math.sin(t * 0.02) + 1) / 2 * 255)
            color = (255, 255, 255, flicker)
        else:
            color = (255, 255, 255, 255)

        pygame.draw.polygon(surface, color, triangle_points, 2)

        screen.blit(surface, (0, 0))

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt * self.accelerate * self.speed_up.get_amount()

    def update(self, dt):
        if self.get_cd() > 0:
            self.decrease_cd(dt, 1000)
        
        if self.speed_reset_time > 0:
            self.speed_reset_time -= dt * 1000
            
        if self.speed_reset_time <= 0:
            self.speed_up.set_amount(1)

        keys = pygame.key.get_pressed()

        # Shooting
        if keys[pygame.K_SPACE]:
            self.attack()

        # Movement
        if keys[pygame.K_a]:
            self.rotate(-dt)

        if keys[pygame.K_d]:
            self.rotate(dt)

        if keys[pygame.K_w]:
            self.move(dt)

        if keys[pygame.K_s]:
            self.accelerate = 1
            self.move(-dt)

        # Accelleration
        if not keys[pygame.K_LSHIFT] and self.accelerate != 1:
            self.accelerate = 1

        if not keys[pygame.K_w] and self.accelerate != 1:
            self.accelerate = 1

        if keys[pygame.K_LSHIFT] and self.accelerate <= 2:
            self.accelerate += dt

        self.shoot_timer -= dt

    def attack(self):
        if (self.shoot_timer <= 0):
            gun_class = self.get_gun()
            gun = gun_class(self.position[0], self.position[1])
            gun.shoot(self.rotation)
            self.shoot_timer = PLAYER_SHOOT_COOLDOWN
            
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * (self.radius / 1.5)

        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right

        return [a, b, c]

    def triangle_collision(self, pt, tri):
        def sign(p1, p2, p3):
            return (p1.x - p3.x) * (p2.y - p3.y) - (p2.x - p3.x) * (p1.y - p3.y)

        b1 = sign(pt, tri[0], tri[1]) < 0.0
        b2 = sign(pt, tri[1], tri[2]) < 0.0
        b3 = sign(pt, tri[2], tri[0]) < 0.0

        return b1 == b2 == b3