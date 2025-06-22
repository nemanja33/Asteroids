import pygame
import os
from game.player.score import Score
from game.weapons.double_gun import DoubleGun
from game.weapons.triple_gun import TripleGun
from game.weapons.weapon import Weapon
from config.constants import *
from game.player.player import Player
from game.asteroids.asteroid import Asteroid
from game.asteroids.asteroidfield import AsteroidField
from game.explosion.explosion import Explosion

def main():
    # font
    pygame.font.init()
    font = pygame.font.SysFont("freesansbold.ttf", 16)

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
    bg_image_path = os.path.join("game", "bg.jpg")
    bg_image = pygame.transform.scale(pygame.image.load(bg_image_path), (SCREEN_WIDTH, SCREEN_HEIGHT))

    # asteroids
    asteroids_group = pygame.sprite.Group()
    Asteroid.containers = (asteroids_group, updatable, drawable)
    AsteroidField.containers = (updatable)
    AsteroidField()

    # shots
    shots_group = pygame.sprite.Group()
    Weapon.containers = (shots_group, updatable, drawable)

    # explosions
    explosion_group = pygame.sprite.Group()
    
    # init score
    score = Score()

    # game loop
    while (True):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        updatable.update(dt)

        # screen fill
        screen.blit(bg_image, (0, 0))

        # explosions
        explosion_group.draw(screen)
        explosion_group.update()

        # detect collision
        for asteroid in asteroids_group:
            if new_player.collision(asteroid):
                shield = new_player.shield.get_shield()
                if (shield > 0):
                    if new_player.shield.get_cd() <= 0:
                        new_player.shield.decrease_shield(1)
                        new_player.shield.increse_cd(2000)
                else:
                    if new_player.shield.get_cd() <= 0:
                        new_player.reduce_lives()
                        new_player.re_spawn()
                if (new_player.get_lives() < 0):
                    print("Game over!")
                    exit()

            for bullet in shots_group:
                if bullet.collision(asteroid):
                    explosion = Explosion(asteroid.position[0], asteroid.position[1])
                    explosion_group.add(explosion)
                    bullet.kill()
                    asteroid.split(bullet.dmg)
                    score.set_score(10)

                    if score.get_score() > 100:
                        new_player.set_gun(DoubleGun)

                    if score.get_score() > 300:
                        new_player.set_gun(TripleGun)

        score_text = font.render("Score {0}".format(score.get_score()), 1, "white")
        screen.blit(score_text, (5, 10))

        # lives text
        lives_text = font.render("Lives {0}".format(new_player.get_lives()), 1, "white")
        screen.blit(lives_text, (5, 30))

        # shield text
        shield_text = font.render("Shield {0}".format(new_player.shield.get_shield()), 1, "white")
        screen.blit(shield_text, (5, 50))

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
