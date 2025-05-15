import pygame
from config.constants import *
from game.player.player import Player
from game.asteroids.asteroid import Asteroid
from game.asteroids.asteroidfield import AsteroidField
from game.player.score import Score
from game.player.shot import Shot

def main():
    # player
    x = SCREEN_WIDTH / 2
    y = SCREEN_HEIGHT / 2
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    Player.containers = (updatable, drawable)
    new_player = Player(x, y)

    # game
    pygame.init()
    clock = pygame.time.Clock()
    dt = 0
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # asteroids
    asteroids = pygame.sprite.Group()
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    asteroid_field = AsteroidField()

    # shots
    shots = pygame.sprite.Group()
    Shot.containers = (shots, updatable, drawable)

    # game loop
    while (True):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        updatable.update(dt)

        # detect collision
        for asteroid in asteroids:
            if new_player.collision(asteroid):
                print("Game over!")
                exit()

            for bullet in shots:
                if bullet.collision(asteroid):
                    bullet.kill()
                    asteroid.split()

        # screen fill
        screen.fill("black")

        # score
        score = Score(screen)

        # player
        for item in drawable:
            item.draw(screen)

        # idk
        pygame.display.flip()

        # fps
        clock.tick(60)
        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()
