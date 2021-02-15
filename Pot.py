import Paint
import pygame

class Pot:

    x = 0
    y = 0
    rect = [0, 0, 0, 0]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = [x, y, 50, 50]

    def paint_pot(self):
        pygame.draw.rect(Paint.screen, Paint.black, (self.x + 21, self.y + 5, 7, 15))
        pygame.draw.rect(Paint.screen, Paint.brown, (self.x + 17.5, self.y + 5, 15, 5))
        pygame.draw.circle(Paint.screen, Paint.brown, (self.x + 25, self.y + 30), 15)
