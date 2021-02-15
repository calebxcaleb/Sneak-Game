import Paint
import pygame
import Values

class Laser:

    laser_x1 = 0
    laser_y1 = 0
    laser_x2 = 0
    laser_y2 = 0
    switch_x = 0
    switch_y = 0
    laser_on = True
    switch_rect = [0, 0, 0, 0]
    laser_rect = [0, 0, 0, 0]

    def __init__(self, laser_x1, laser_y1, laser_x2, laser_y2, switch_x, switch_y, laser_rect):
        self.laser_x1 = laser_x1
        self.laser_y1 = laser_y1
        self.laser_x2 = laser_x2
        self.laser_y2 = laser_y2
        self.switch_x = switch_x
        self.switch_y = switch_y
        self.switch_rect = [switch_x - 12, switch_y - 12, 24, 24]
        self.laser_rect = laser_rect

    def paint_laser_back(self):
        pygame.draw.rect(Paint.screen, Paint.dark_green, self.switch_rect)
        pygame.draw.circle(Paint.screen, Paint.dark_red, (self.switch_x, self.switch_y), 9)
        pygame.draw.rect(Paint.screen, Paint.light_mid_gray, (self.laser_x1 - 12, self.laser_y1 - 12, 24, 24))
        pygame.draw.rect(Paint.screen, Paint.light_mid_gray, (self.laser_x2 - 12, self.laser_y2 - 12, 24, 24))
        pygame.draw.circle(Paint.screen, Paint.black, (self.laser_x1, self.laser_y1), 9)
        pygame.draw.circle(Paint.screen, Paint.black, (self.laser_x2, self.laser_y2), 9)

    def paint_laser_for(self):
        if self.laser_on:
            pygame.draw.line(Paint.screen, Paint.red, (self.laser_x1, self.laser_y1), (self.laser_x2, self.laser_y2), 5)
            pygame.draw.circle(Paint.screen, Paint.red, (self.laser_x1, self.laser_y1), 5)
            pygame.draw.circle(Paint.screen, Paint.red, (self.laser_x2, self.laser_y2), 5)

        if Values.dev_view:
            if self.laser_on:
                col = Paint.green
            else:
                col = Paint.red
            pygame.draw.line(Paint.screen, col, (self.switch_x, self.switch_y), (self.laser_x1, self.laser_y1), 3)