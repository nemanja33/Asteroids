import pygame
import math
from game.base_shape.base_shape import BaseShape
from game.weapons.base_gun import BaseGun
from config.constants import PLAYER_RADIUS, PLAYER_TURN_SPEED, PLAYER_SPEED, PLAYER_SHOOT_COOLDOWN, PLAYER_DEFAULT_BOMB_AMOUNT

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
        self.screen = None
        self.shield_amount = 0
        self.speed_up_active = False
        self.bomb_amount = PLAYER_DEFAULT_BOMB_AMOUNT
        self.bomb_regen_timer = 0 

    def get_lives(self):
        return self.lives

    def reduce_lives(self):
        self.lives -= 1

    def get_gun(self):
        return self.gun

    def set_gun(self, gun):
        self.gun = gun

    def get_respawn_cd(self):
        return self.respawn_cd

    def get_shield(self):
        return self.shield_amount

    def add_shield(self, amount):
        self.shield_amount += amount

    def use_shield(self):
        if self.shield_amount > 0:
            self.shield_amount -= 1

    def increse_cd(self, x):
        self.respawn_cd = x

    def decrease_cd(self, dt, x):
        self.respawn_cd -= dt * x
        
    def get_bomb_amount(self):
        return self.bomb_amount
    
    def decrease_bomb_amount(self):
        self.bomb_amount -= 1
    
    def regenerate_bomb_amount(self):
        self.bomb_amount += 1

    def respawn(self):
        self.position = pygame.Vector2(pygame.display.get_surface().get_width() / 2, pygame.display.get_surface().get_height() / 2)
        self.accelerate = 1

    def activate_speed_up(self, duration=5):
        self.speed_up_active = True
        self.speed_reset_time = duration * 1000

    def deactivate_speed_up(self):
        self.speed_up_active = False

    def set_acceleration(self, a):
        self.accelerate = a

    def draw(self, screen):
        self.screen = screen
        triangle_points = self.triangle()
        surface = pygame.Surface((pygame.display.get_surface().get_width(), pygame.display.get_surface().get_height()), pygame.SRCALPHA)
        if self.get_respawn_cd() > 0:
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
        speed_factor = 1.2 if self.speed_up_active else 1.0
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt * self.accelerate * speed_factor

        # Screen wrap
        screen_width = pygame.display.get_surface().get_width()
        screen_height = pygame.display.get_surface().get_height()
        if self.position.x < 0:
            self.position.x = screen_width
        elif self.position.x > screen_width:
            self.position.x = 0
        if self.position.y < 0:
            self.position.y = screen_height
        elif self.position.y > screen_height:
            self.position.y = 0

    def update(self, dt):
        if self.get_respawn_cd() > 0:
            self.decrease_cd(dt, 1000)

        if self.speed_up_active:
            self.speed_reset_time -= dt * 1000
            if self.speed_reset_time <= 0:
                self.deactivate_speed_up()

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
            
        # Acceleration
        if not keys[pygame.K_LSHIFT] and self.accelerate != 1:
            self.accelerate = 1
        if not keys[pygame.K_w] and self.accelerate != 1:
            self.accelerate = 1
        if keys[pygame.K_LSHIFT] and self.accelerate <= 2:
            self.accelerate += dt
            
        # Bomb regeneration
        if self.bomb_amount < PLAYER_DEFAULT_BOMB_AMOUNT:
            self.bomb_regen_timer += dt
            if self.bomb_regen_timer >= 10:  
                self.regenerate_bomb_amount()
                self.bomb_regen_timer = 0
        else:
            self.bomb_regen_timer = 0

        self.shoot_timer -= dt

    def attack(self):
        if self.shoot_timer <= 0:
            gun_class = self.get_gun()
            gun = gun_class(self.position[0], self.position[1])
            gun.shoot(self.rotation)
            self.shoot_timer = PLAYER_SHOOT_COOLDOWN

    # collision
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