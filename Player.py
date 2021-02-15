import Paint
import Values
import pygame

class Player:

    pygame.init()

    x = 0
    y = 0
    r = 25//2
    max_life = 3
    life = max_life
    hidden = False
    lit = False
    lit_index = 0
    speed = 0.2
    alive = True
    up_rect = [0, 0, 0, 0]
    down_rect = [0, 0, 0, 0]
    left_rect = [0, 0, 0, 0]
    right_rect = [0, 0, 0, 0]
    rects = [up_rect, down_rect, left_rect, right_rect]

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self):
        if self.x + self.r > Values.screen_width:
            self.x = Values.screen_width - self.r
        if self.x - self.r < 0:
            self.x = self.r
        if self.y + self.r > Values.screen_height:
            self.y = Values.screen_height - self.r
        if self.y - self.r < 100:
            self.y = self.r + 100

        self.rects[0] = [self.x - self.r / 2, self.y - self.r, self.r, self.r / 4]
        self.rects[1] = [self.x - self.r / 2, self.y + self.r - self.r / 4, self.r, self.r / 4]
        self.rects[2] = [self.x - self.r, self.y - self.r / 2, self.r / 4, self.r]
        self.rects[3] = [self.x + self.r - self.r / 4, self.y - self.r / 2, self.r / 4, self.r]

    def check_life(self):
        if self.life <= 0:
            self.alive = False
            self.life = 0

    def check_hidden(self, pots):
        for pot in pots:
            if self.x - self.r < pot.rect[0] + pot.rect[2] and self.y - self.r < pot.rect[1] + pot.rect[3] and self.x + self.r > pot.rect[0] and self.y + self.r > pot.rect[1]:
                self.hidden = True
                break
            else:
                self.hidden = False

    def check_light(self, lights):
        for light in lights:
            if self.x - self.r < light.x + light.r2 and self.y - self.r < light.y + light.r2 and self.x + self.r > light.x - light.r2 and self.y + self.r > light.y - light.r2:
                self.lit = True
                self.lit_index = light.index
                break
            else:
                self.lit = False

    def check_walls(self, walls):
        for i in range(len(self.rects)):
            for wall in walls:
                if self.rects[i][0] + self.rects[i][2] > wall[0] and self.rects[i][0] < wall[0] + wall[2] and self.rects[i][1] + self.rects[i][3] > wall[1] and self.rects[i][1] < wall[1] + wall[3]:

                    if i == 3:
                        self.x = wall[0] - self.r
                    if i == 2:
                        self.x = wall[0] + wall[2] + self.r
                    if i == 1:
                        self.y = wall[1] - self.r
                    if i == 0:
                        self.y = wall[1] + wall[3] + self.r

                    break

    def paint_player(self):
        pygame.draw.circle(Paint.screen, Paint.dark_blue, (int(self.x), int(self.y)), self.r)

    def paint_player_colliders(self):
        pygame.draw.rect(Paint.screen, Paint.dark_blue, (int(self.x) - self.r, int(self.y) - self.r, self.r * 2, self.r * 2), 3)
        for rect in self.rects:
            pygame.draw.rect(Paint.screen, Paint.black, rect, 2)