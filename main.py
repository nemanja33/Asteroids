import pygame
from constants import *
from player import Player

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

    # game loop
    while (True):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        updatable.update(dt)

        # screen fill
        screen.fill("black")

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
