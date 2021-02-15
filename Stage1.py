import pygame
import Values
import Functions
from Laser import Laser
from Pot import Pot
from Light import Light
import Paint
from AI import AI

class Stage1:

    pygame.init()

    # Walls
    walls = []
    walls.append([700, 300, 50, 150])
    walls.append([750, 400, 400, 50])
    walls.append([1000, 100, 50, 100])
    walls.append([1050, 150, 50, 150])
    walls.append([1100, 250, 100, 50])
    walls.append([1150, 300, 50, 50])
    walls.append([1250, 150, 150, 50])
    walls.append([1350, 200, 50, 50])
    walls.append([1250, 250, 150, 200])
    walls.append([800, 250, 100, 100])
    walls.append([1100, 500, 300, 50])
    walls.append([1100, 450, 50, 50])
    walls.append([1250, 450, 150, 50])

    # Return Points
    return_path = []
    basic_path = []
    basic_path.append([25, 125])
    basic_path.append([775, 125])
    basic_path.append([775, 375])
    basic_path.append([1225, 375])
    basic_path.append([1225, 125])
    basic_path.append([1375, 125])

    # Lazers
    lasers = []
    lasers.append(Laser(725, 125, 725, 275, 775, 375, [725 - 2, 125 - 2, 4, 150 + 4]))

    # Pots
    pots = []
    pots.append(Pot(900, 200))
    pots.append(Pot(500, 200))

    # Lights
    lights = []
    lights.append(Light(925, 225, 0))
    lights.append(Light(1225, 375, 0))

    # Goal
    goal = [250, 150]

    def laser_paint_for(self):
        for laser in self.lasers:
            laser.paint_laser_for()

    def laser_paint_back(self):
        for laser in self.lasers:
            laser.paint_laser_back()

    def pot_paint(self):
        for pot in self.pots:
            pot.paint_pot()

    def light_paint_back(self):
        for light in self.lights:
            light.paint_light_back()

    def light_paint_for(self):
        for light in self.lights:
            light.paint_light_for()

    def laser_set(self):
        for laser in self.lasers:
            laser.laser_on = True

    def set_return_path(self):
        for i in range(len(self.basic_path)-1):
            xy = 0
            if self.basic_path[i][0] == self.basic_path[i+1][0]:
                xy = 1

            direction = 1
            if self.basic_path[i][xy] > self.basic_path[i+1][xy]:
                direction = -1

            num = (self.basic_path[i+1][xy] - self.basic_path[i][xy]) * direction // 50

            for a in range(num):
                if xy == 0:
                    self.return_path.append([self.basic_path[i][0] + a * 50 * direction, self.basic_path[i][1]])
                else:
                    self.return_path.append([self.basic_path[i][0], self.basic_path[i][1] + a * 50 * direction])

    def set_player(self):
        Functions.player.x = 1075
        Functions.player.y = 125

    def add_AI(self):
        Functions.ais = []
        path1 = [[1375, 125], [1225, 125], [1225, 375], [1075, 375], [1225, 375], [1225, 125]]
        Functions.ais.append(AI(path1, 2, self.return_path))
        path2 = [[775, 225], [775, 375], [925, 375], [925, 225]]
        Functions.ais.append(AI(path2, 1, self.return_path))

    def remove_AI(self):
        Functions.ais.clear()

    def draw_stage_back_master(self):
        self.light_paint_back()

    def draw_stage_back(self):
        if Values.dev_view:
            for point in self.return_path:
                pygame.draw.circle(Paint.screen, Paint.green, (point[0], point[1]), 5)

        self.light_paint_for()
        self.laser_paint_back()
        self.pot_paint()

        pygame.draw.circle(Paint.screen, Paint.green, self.goal, 25)
        pygame.draw.circle(Paint.screen, Paint.black, self.goal, 26, 3)

    def draw_stage_for(self):
        for wall in self.walls:
            pygame.draw.rect(Paint.screen, Paint.black, wall)

        self.laser_paint_for()


