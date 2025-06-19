import pygame
from game.weapons.base_gun import BaseGun
from game.Miscellaneous.BaseShape.baseshape import BaseShape
from config.constants import *

class Player(BaseShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.timer = 0
        self.score = 0
        self.lives = 2
        self.accelerate = 1
        self.running = False
        self.gun = BASE_GUN

    def set_lives(self):
        self.lives -= 1

    def get_lives(self):
        return self.lives

    def set_score(self, value):
        self.score += value

    def get_score(self):
        return self.score
    
    def set_gun(self, gun):
        self.gun = gun

    def get_gun(self):
        return self.gun

    def re_spawn(self):
        self.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.accelerate = 1

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * (self.radius / 1.5)

        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right

        return [a, b, c]

    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), 2)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt * self.accelerate

    def update(self, dt):
        keys = pygame.key.get_pressed()

        # Shooting
        if keys[pygame.K_SPACE]:
            self.shoot(self.gun)

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

        if keys[pygame.K_LSHIFT] and self.accelerate <=2:
            self.accelerate += dt

        self.timer -= dt

    def shoot(self, type):
        if (self.timer <= 0):
            forward = pygame.Vector2(0, 1).rotate(self.rotation)
            side = pygame.Vector2(1, 0).rotate(self.rotation)
            side_offset = side * 20
            # refactor later
            # weap type
            if (type == "BASE GUN"):
                shot = BaseGun(self.position[0], self.position[1])
                shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED

            if (type == "DOUBLE GUN"):
                positions = [
                    self.position - side_offset,
                    self.position + side_offset
                ]

                for pos in positions:
                    shot = BaseGun(pos.x, pos.y)
                    shot.velocity = forward * PLAYER_SHOOT_SPEED
                    shot.rotation = self.rotation

                
            if (type == "TRIPLE GUN"):
                angles = [10, 0, -10]
                positions = [
                    self.position - side_offset, 
                    self.position,
                    self.position + side_offset
                ]

                for angle, pos in zip(angles, positions):
                    shot = BaseGun(pos.x, pos.y)
                    shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation + angle) * PLAYER_SHOOT_SPEED
                    shot.rotation = self.rotation + angle


            self.timer = PLAYER_SHOOT_COOLDOWN

    def point_in_triangle(self, pt, tri):
        def sign(p1, p2, p3):
            return (p1.x - p3.x) * (p2.y - p3.y) - (p2.x - p3.x) * (p1.y - p3.y)

        b1 = sign(pt, tri[0], tri[1]) < 0.0
        b2 = sign(pt, tri[1], tri[2]) < 0.0
        b3 = sign(pt, tri[2], tri[0]) < 0.0

        return b1 == b2 == b3