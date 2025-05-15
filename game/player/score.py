import pygame

class Score():
    def __init__(self, screen) -> None:
        self.score = 0
        self.screen = screen
        self.display(self.score)

    def display(self, new_score):
        pygame.font.init()
        font = pygame.font.Font("freesansbold.ttf", 16)
        score = font.render(str(new_score), True, "white", "black")
        self.screen.blit(score, dest=(5, 10))

    def update(self, new_score):
        self.score += new_score
        self.display(int(self.score))
