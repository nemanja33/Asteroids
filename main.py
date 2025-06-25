import pygame
import os
from random import randint
from game.player.bomb.bomb import Bomb
from game.player.score.score import Score
from game.player.shield.shield import Shield
from game.player.speed_up.speed_up import SpeedUp
from game.weapons.double_gun import DoubleGun
from game.weapons.triple_gun import TripleGun
from game.weapons.weapon import Weapon
from config.constants import SCREEN_HEIGHT, SCREEN_WIDTH, PLAYER_SHOOT_COOLDOWN
from game.player.player import Player
from game.asteroids.asteroid import Asteroid
from game.asteroids.asteroidfield import AsteroidField
from game.explosion.explosion import Explosion

def main():
    # init data
    pygame.init()
    font = pygame.font.SysFont("freesansbold.ttf", 16)
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    bg_image = pygame.transform.scale(
        pygame.image.load(os.path.join("game", "bg.jpg")),
        (pygame.display.get_surface().get_width(), pygame.display.get_surface().get_height())
    )

    # player info
    x, y = pygame.display.get_surface().get_width() / 2, pygame.display.get_surface().get_height() / 2
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    Player.containers = (updatable, drawable)
    new_player = Player(x, y)

    # asteroids
    asteroids_group = pygame.sprite.Group()
    Asteroid.containers = (asteroids_group, updatable, drawable)
    AsteroidField.containers = (updatable,)
    AsteroidField()

    # weapon
    shots_group = pygame.sprite.Group()
    Weapon.containers = (shots_group, updatable, drawable)

    # explosion
    explosion_group = pygame.sprite.Group()
    score = Score()
    
    # bomb
    bomb_group = pygame.sprite.Group()

    # shield
    SHIELD_EVENT = pygame.USEREVENT + 1
    shield_group = pygame.sprite.Group()

    def start_shield_timer():
        pygame.time.set_timer(SHIELD_EVENT, randint(2000, 10000))

    if not shield_group:
        start_shield_timer()

    # speed up
    SPEED_UP_EVENT = pygame.USEREVENT + 2
    speed_up_group = pygame.sprite.Group()

    def start_speed_up_timer():
        pygame.time.set_timer(SPEED_UP_EVENT, randint(2000, 10000))

    if not speed_up_group:
        start_speed_up_timer()

    running = True
    while running:
        dt = clock.tick(60) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # shield and speed up handling
            if event.type == SHIELD_EVENT and not shield_group:
                shield = Shield()
                shield_group.add(shield)
                pygame.time.set_timer(SHIELD_EVENT, randint(2000, 10000))

            if event.type == SPEED_UP_EVENT and not speed_up_group:
                speed_up = SpeedUp()
                speed_up_group.add(speed_up)
                pygame.time.set_timer(SPEED_UP_EVENT, randint(2000, 10000))
                
            # bomb handling
            bomb_ready = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e and bomb_ready:
                    if new_player.shoot_timer <= 0 and player_bomb_amount > 0:
                        bomb = Bomb(new_player.position[0], new_player.position[1])
                        bomb_group.add(bomb)
                        new_player.shoot_timer = PLAYER_SHOOT_COOLDOWN * 2
                        new_player.decrease_bomb_amount()
                        bomb_ready = False

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_e:
                    bomb_ready = True

        # update data
        updatable.update(dt)
        explosion_group.update()
        shield_group.update(dt)
        speed_up_group.update(dt)
        bomb_group.update(dt)

        # show images and sprites
        screen.blit(bg_image, (0, 0))
        explosion_group.draw(screen)
        shield_group.draw(screen)
        speed_up_group.draw(screen)
        bomb_group.draw(screen)

        # player data
        player_shield = new_player.get_shield()
        player_lives = new_player.get_lives()
        player_respawn_cd = new_player.get_respawn_cd()
        player_bomb_amount = new_player.get_bomb_amount()

        # asteroid collision
        for asteroid in asteroids_group:
            if new_player.collision(asteroid):
                if player_respawn_cd <= 0:
                    new_player.increse_cd(2000)
                    if player_shield > 0:
                        new_player.use_shield()
                    else:
                        new_player.respawn()
                        new_player.reduce_lives()
                if player_lives <= 0:
                    print("Game over!")
                    running = False

            for bullet in shots_group:
                if bullet.collision(asteroid):
                    explosion_group.add(Explosion(asteroid.position[0], asteroid.position[1]))
                    bullet.kill()
                    asteroid.split(bullet.dmg)
                    score.set_score(10)
                    
            for bomb in bomb_group:
                if bomb.collision(asteroid):
                    explosion_group.add(Explosion(asteroid.position[0], asteroid.position[1]))
                    bomb.kill()
                    asteroid.split(bomb.damage)
                    score.set_score(10)

        # shield collision
        for shield in shield_group:
            if shield.collision(new_player):
                new_player.add_shield(1)
                shield.kill()

        # speed up collision
        for speed_up in speed_up_group:
            if speed_up.collision(new_player):
                new_player.activate_speed_up()
                speed_up.kill()

        # weapon change
        current_score = score.get_score()
        if current_score > 300:
            new_player.set_gun(TripleGun)
        elif current_score > 100:
            new_player.set_gun(DoubleGun)
            
        # game info
        score_text = font.render(f"Score {current_score}", True, "white")
        lives_text = font.render(f"Lives {player_lives}", True, "white")
        shield_text = font.render(f"Shield {player_shield}", True, "white")
        bomb_text = font.render(f"Bombs {player_bomb_amount}", True, "white")

        screen.blit(score_text, (5, 10))
        screen.blit(lives_text, (5, 30))
        screen.blit(shield_text, (5, 50))
        screen.blit(bomb_text, (5, 70))

        for item in drawable:
            item.draw(screen)

        pygame.display.flip()

if __name__ == "__main__":
    main()