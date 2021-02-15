import Paint
import pygame

class Light:

    x = 0
    y = 0
    r1 = 30
    r2 = 45
    index = 0

    def __init__(self, x, y, index):
        self.x = x
        self.y = y
        self.index = index

    def paint_light_back(self):
        pygame.draw.circle(Paint.screen, Paint.light_mid_gray, (self.x, self.y), self.r2)

    def paint_light_for(self):
        pygame.draw.circle(Paint.screen, Paint.light_gray, (self.x, self.y), self.r1)
