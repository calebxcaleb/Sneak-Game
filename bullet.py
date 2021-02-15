import Paint
import pygame

class bullet:

    player_copy = None

    x = 0
    y = 0
    r = 10
    speed = 0.5
    x_speed = 0
    y_speed = 0

    def __init__(self, AI, player):
        self.player_copy = player
        self.x = AI.x
        self.y = AI.y
        self.setup()

    def setup(self):
        x_dif = self.player_copy.x - self.x
        y_dif = self.player_copy.y - self.y
        sum_dif = abs(x_dif) + abs(y_dif)
        x_per = x_dif / sum_dif
        y_per = y_dif / sum_dif
        self.x_speed = self.speed * x_per
        self.y_speed = self.speed * y_per

    def move(self):
        self.x += self.x_speed
        self.y += self.y_speed

    def paint_bullet(self):
        pygame.draw.circle(Paint.screen, Paint.dark_red, (int(self.x), int(self.y)), self.r)