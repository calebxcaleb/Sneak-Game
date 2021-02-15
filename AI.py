import Paint
import Values
from bullet import bullet
import math
import Functions
import pygame

class AI:

    pygame.init()

    x = 0
    y = 0
    r = 25//2
    rr = 100//2
    flash_center = [0, 0]
    flash_rect = [0, 0, 0, 0]
    flash_r = 90//2
    exit_center = [0, 0]
    exit_rect = [0, 0, 0, 0]
    exit_r = 150//2
    collide_r = 40//2
    FOV = math.pi/4
    can_see_player = False
    pos = 0
    next = pos + 1
    attack = False
    returning = False
    return_set = False
    line_colour = (0, 0, 0)
    x_speed = 0
    y_speed = 0
    was_x_speed = 0
    was_y_speed = 0
    was_x_per = 0
    was_y_per = 0
    angle = 0
    new_angle = 0
    raw_angle = 0
    return_index = 0
    return_dir = 0
    return_index_now = 0
    speed = 0.1
    return_path = []
    attack_speed = 0.15
    norm_speed = 0.1
    path = []
    shoot_count = 0
    shoot_count_max = 1000
    up_rect = [0, 0, 0, 0]
    down_rect = [0, 0, 0, 0]
    left_rect = [0, 0, 0, 0]
    right_rect = [0, 0, 0, 0]
    rects = [up_rect, down_rect, left_rect, right_rect]
    suspicious = False
    suspicious_index = 0
    rotating = False
    rotate_dir = 0
    angle_speed = 0.1
    rotate_time = 0
    rotate_time_max = 10

    def __init__(self, path, return_index, return_path):
        self.return_path = return_path
        self.x = path[0][0]
        self.y = path[0][1]
        self.flash_center = [0, 0]
        self.flash_rect = [0, 0, 0, 0]
        self.exit_center = [0, 0]
        self.exit_rect = [0, 0, 0, 0]
        self.return_index = return_index
        self.return_dir = 1
        self.return_index_now = 0
        self.up_rect = [0, 0, 0, 0]
        self.down_rect = [0, 0, 0, 0]
        self.left_rect = [0, 0, 0, 0]
        self.right_rect = [0, 0, 0, 0]
        self.rects = [self.up_rect, self.down_rect, self.left_rect, self.right_rect]
        self.path = path
        self.rotating = False
        self.rotate_dir = 0
        self.angle_speed = 0.1
        self.setup()

    def check_player(self):
        if self.attack:
            self.suspicious = False
            self.suspicious_index = 0

            if Functions.player.x + Functions.player.r > self.x - self.r and Functions.player.x - Functions.player.r < self.x + self.r and\
               Functions.player.y + Functions.player.r > self.y - self.r and Functions.player.y - Functions.player.r < self.y + self.r:
                Functions.player.alive = False
                self.attack = False
                if not self.returning:
                    self.return_set = True
                self.returning = True
                # self.setup_special()
            if not (Functions.player.x + Functions.player.r > self.exit_rect[0] and Functions.player.x - Functions.player.r < self.exit_rect[0] + self.exit_rect[2] and
               Functions.player.y + Functions.player.r > self.exit_rect[1] and Functions.player.y - Functions.player.r < self.exit_rect[1] + self.exit_rect[3]):
                self.attack = False
                if not self.returning:
                    self.return_set = True
                self.returning = True
                # self.setup_special()
        elif Functions.player.x + Functions.player.r > self.flash_rect[0] and Functions.player.x < self.flash_rect[0] + self.flash_rect[2] and\
             Functions.player.y + Functions.player.r > self.flash_rect[1] and Functions.player.y < self.flash_rect[1] + self.flash_rect[3]:
            if Functions.player.alive and self.can_see_player and not Functions.player.hidden:
                self.attack = True
                self.returning = False
                self.return_set = False
        elif self.can_see_player and Functions.player.lit:
            self.suspicious = True
            self.suspicious_index = Functions.player.lit_index

    def check_see_player(self, wall, point_x, point_y):
        x1 = self.x
        y1 = self.y
        x2 = point_x
        y2 = point_y

        x3 = wall[0]
        y3 = wall[1]
        x4 = wall[0]
        y4 = wall[1] + wall[3]

        left = self.check_wall_sides(x1, y1, x2, y2, x3, y3, x4, y4)

        x3 = wall[0] + wall[2]
        y3 = wall[1]
        x4 = wall[0] + wall[2]
        y4 = wall[1] + wall[3]

        right = self.check_wall_sides(x1, y1, x2, y2, x3, y3, x4, y4)

        x3 = wall[0]
        y3 = wall[1]
        x4 = wall[0] + wall[2]
        y4 = wall[1]

        top = self.check_wall_sides(x1, y1, x2, y2, x3, y3, x4, y4)

        x3 = wall[0]
        y3 = wall[1] + wall[3]
        x4 = wall[0] + wall[2]
        y4 = wall[1] + wall[3]

        bottom = self.check_wall_sides(x1, y1, x2, y2, x3, y3, x4, y4)

        return top or bottom or right or left

    def check_wall_sides(self, x1, y1, x2, y2, x3, y3, x4, y4):
        n1 = (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1)
        n2 = (x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)
        n3 = (x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)

        uA = -1
        uB = -1

        if not n1 == 0:
            uA = n2 / n1
            uB = n3 / n1

        return 0 <= uA <= 1 and 0 <= uB <= 1

    def setup_attack(self):
        self.speed = self.attack_speed
        x_dif = Functions.player.x - self.x
        y_dif = Functions.player.y - self.y
        sum_dif = abs(x_dif) + abs(y_dif)
        x_per = x_dif / sum_dif
        y_per = y_dif / sum_dif
        self.x_speed = self.speed * x_per
        self.y_speed = self.speed * y_per
        self.was_x_per = x_per
        self.was_y_per = y_per
        self.was_x_speed = self.x_speed
        self.was_y_speed = self.y_speed
        if self.y_speed == 0:
            self.raw_angle = math.atan(abs(self.was_x_speed / 0.000001))
        else:
            self.raw_angle = math.atan(abs(self.was_x_speed / self.was_y_speed))
        self.angle = self.raw_angle - math.pi / 2

        if self.x_speed < 0:
            self.angle = math.pi - self.angle
        if self.y_speed < 0:
            self.angle *= -1

    def setup_return(self):
        self.speed = self.norm_speed
        x_dif = self.return_path[self.return_index_now][0] - self.x
        y_dif = self.return_path[self.return_index_now][1] - self.y
        sum_dif = abs(x_dif) + abs(y_dif)
        x_per = x_dif / sum_dif
        y_per = y_dif / sum_dif
        self.x_speed = self.speed * x_per
        self.y_speed = self.speed * y_per
        self.was_x_per = x_per
        self.was_y_per = y_per
        self.was_x_speed = self.x_speed
        self.was_y_speed = self.y_speed
        if self.y_speed == 0:
            self.raw_angle = math.atan(abs(self.was_x_speed / 0.000001))
        else:
            self.raw_angle = math.atan(abs(self.was_x_speed / self.was_y_speed))
        self.angle = self.raw_angle - math.pi / 2

        if self.x_speed < 0:
            self.angle = math.pi - self.angle
        if self.y_speed < 0:
            self.angle *= -1

    def setup_special(self):
        self.speed = self.norm_speed
        x_dif = self.path[self.next][0] - self.x
        y_dif = self.path[self.next][1] - self.y
        sum_dif = abs(x_dif) + abs(y_dif)
        x_per = x_dif / sum_dif
        y_per = y_dif / sum_dif
        self.x_speed = self.speed * x_per
        self.y_speed = self.speed * y_per
        self.was_x_per = x_per
        self.was_y_per = y_per
        self.was_x_speed = self.x_speed
        self.was_y_speed = self.y_speed
        if self.y_speed == 0:
            self.raw_angle = math.atan(abs(self.was_x_speed / 0.000001))
        else:
            self.raw_angle = math.atan(abs(self.was_x_speed / self.was_y_speed))
        self.angle = self.raw_angle - math.pi / 2

        if self.x_speed < 0:
            self.angle = math.pi - self.angle
        if self.y_speed < 0:
            self.angle *= -1

    def setup(self):
        self.speed = self.norm_speed
        x_dif = self.path[self.next][0] - self.path[self.pos][0]
        y_dif = self.path[self.next][1] - self.path[self.pos][1]
        sum_dif = abs(x_dif) + abs(y_dif)
        x_per = x_dif / sum_dif
        y_per = y_dif / sum_dif
        self.x_speed = self.speed * x_per
        self.y_speed = self.speed * y_per
        self.was_x_per = x_per
        self.was_y_per = y_per
        self.was_x_speed = self.x_speed
        self.was_y_speed = self.y_speed
        if self.y_speed == 0:
            self.raw_angle = math.atan(abs(self.was_x_speed / 0.000001))
        else:
            self.raw_angle = math.atan(abs(self.was_x_speed / self.was_y_speed))
        self.new_angle = self.raw_angle - math.pi / 2

        if self.x_speed < 0:
            self.new_angle = math.pi - self.new_angle
        if self.y_speed < 0:
            self.new_angle *= -1
        self.rotating = True
        self.setup_rotate()

    def shoot(self):
        if self.shoot_count >= self.shoot_count_max:
            self.shoot_count = 0
            Functions.bullets.append(bullet(self, Functions.player))
        else:
            self.shoot_count += 1

    def setup_rotate(self):
        while self.angle < 0:
            self.angle += 2 * math.pi
        while self.angle >= 2 * math.pi - 0.5:
            self.angle -= 2 * math.pi
        while self.new_angle < 0:
            self.new_angle += 2 * math.pi
        while self.new_angle >= 2 * math.pi - 0.5:
            self.new_angle -= 2 * math.pi

        if self.new_angle > self.angle:
            self.rotate_dir = 1
        elif self.new_angle < self.angle:
            self.rotate_dir = -1

        if abs(self.new_angle - self.angle) > math.pi + 0.5:
            self.rotate_dir *= -1

        # print("New AI -------------------------")
        # print("Now: " + str(self.angle))
        # print("New: " + str(self.new_angle))
        # print("Angle diff: " + str(self.new_angle - self.angle))

    def rotate(self):
        if self.rotate_time >= self.rotate_time_max:
            self.rotate_time = 0
            self.angle += self.angle_speed * self.rotate_dir
        else:
            self.rotate_time += 1

        if (self.rotate_dir == 1 and self.angle >= self.new_angle) or (self.rotate_dir == -1 and self.angle <= self.new_angle):
            self.angle = self.new_angle
            self.rotating = False

    def collider_update(self):
        self.flash_center[0] = self.x + self.was_x_per * self.flash_r
        self.flash_center[1] = self.y + self.was_y_per * self.flash_r
        self.flash_rect[0] = self.flash_center[0] - self.flash_r
        self.flash_rect[1] = self.flash_center[1] - self.flash_r
        self.flash_rect[2] = self.flash_r * 2
        self.flash_rect[3] = self.flash_r * 2
        self.exit_center[0] = self.x + self.was_x_per * self.exit_r
        self.exit_center[1] = self.y + self.was_y_per * self.exit_r
        self.exit_rect[0] = self.exit_center[0] - self.exit_r
        self.exit_rect[1] = self.exit_center[1] - self.exit_r
        self.exit_rect[2] = self.exit_r * 2
        self.exit_rect[3] = self.exit_r * 2

    def move(self):
        self.x += self.x_speed
        self.y += self.y_speed

        if self.attack:
            self.shoot()
        else:
            self.shoot_count = 0

        if self.returning:
            if not self.return_set:
                if self.x <= self.return_path[self.return_index_now][0] and self.x_speed < 0:
                    self.x_speed = 0
                    self.x = self.return_path[self.return_index_now][0]
                elif self.x >= self.return_path[self.return_index_now][0] and self.x_speed > 0:
                    self.x_speed = 0
                    self.x = self.return_path[self.return_index_now][0]

                if self.y <= self.return_path[self.return_index_now][1] and self.y_speed < 0:
                    self.y_speed = 0
                    self.y = self.return_path[self.return_index_now][1]
                elif self.y >= self.return_path[self.return_index_now][1] and self.y_speed > 0:
                    self.y_speed = 0
                    self.y = self.return_path[self.return_index_now][1]

                if self.x == self.return_path[self.return_index_now][0] and self.y == self.return_path[self.return_index_now][1]:
                    if self.return_path[self.return_index_now] == self.path[self.return_index]:
                        self.returning = False
                        self.pos = self.return_index
                        self.next = self.pos
                        if self.next + 1 is len(self.path):
                            self.next = 0
                        else:
                            self.next += 1
                        self.setup()
                    else:
                        self.return_index_now += 1 * self.return_dir
                        self.setup_return()

        elif self.attack:
            self.setup_attack()
        else:
            if self.x <= self.path[self.next][0] and self.x_speed < 0:
                self.x_speed = 0
                self.x = self.path[self.next][0]
            elif self.x >= self.path[self.next][0] and self.x_speed > 0:
                self.x_speed = 0
                self.x = self.path[self.next][0]

            if self.y <= self.path[self.next][1] and self.y_speed < 0:
                self.y_speed = 0
                self.y = self.path[self.next][1]
            elif self.y >= self.path[self.next][1] and self.y_speed > 0:
                self.y_speed = 0
                self.y = self.path[self.next][1]

            if self.x == self.path[self.next][0] and self.y == self.path[self.next][1]:
                self.pos = self.next
                if self.next + 1 is len(self.path):
                    self.next = 0
                else:
                    self.next += 1
                self.setup()

        self.rects[0] = [self.x - self.r / 2, self.y - self.r, self.r, self.r / 4]
        self.rects[1] = [self.x - self.r / 2, self.y + self.r - self.r / 4, self.r, self.r / 4]
        self.rects[2] = [self.x - self.r, self.y - self.r / 2, self.r / 4, self.r]
        self.rects[3] = [self.x + self.r - self.r / 4, self.y - self.r / 2, self.r / 4, self.r]

    def check_walls(self, walls):
        if self.returning and self.return_set:
            self.return_set = False

            possible_points = []
            return_index_new = 0
            hit_no_wall = True

            for i in range(len(self.return_path)):
                hit_no_wall = True
                if self.return_path[i][0] == self.path[self.return_index][0] and self.return_path[i][1] == self.path[self.return_index][1]:
                    return_index_new = i
                for wall in walls:
                    if self.check_see_player(wall, self.return_path[i][0], self.return_path[i][1]):
                        hit_no_wall = False
                        break
                if hit_no_wall:
                    possible_points.append(i)

            closest = 0

            for i in range(len(possible_points)):
                if abs(possible_points[i] - return_index_new) < abs(possible_points[closest] - return_index_new):
                    closest = i

            self.return_index_now = possible_points[closest]
            self.return_dir = 1
            if self.return_index_now > return_index_new:
                self.return_dir = -1

            self.setup_return()

        self.can_see_player = True
        self.line_colour = Paint.green
        for wall in walls:
            if self.check_see_player(wall, Functions.player.x, Functions.player.y):
                self.can_see_player = False
                self.line_colour = Paint.red
                break
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

    def paint_AI(self):
        pygame.draw.circle(Paint.screen, Paint.black, (int(self.x), int(self.y)), self.r)

    def paint_AI_flash(self):
        for i in range(self.rr):
            pygame.draw.arc(Paint.screen, Paint.yellow, (int(self.x) - (self.rr - i * 1), int(self.y) - (self.rr - i * 1), (self.rr - i * 1) * 2, (self.rr - i * 1) * 2), self.angle - self.FOV/2, self.angle + self.FOV/2, 1)

    def paint_AI_light(self):
        pygame.draw.circle(Paint.screen, Paint.light_gray, (int(self.flash_center[0]), int(self.flash_center[1])), self.flash_r)

    def paint_AI_mid(self):
        if self.attack:
            pygame.draw.circle(Paint.screen, Paint.mid_gray, (int(self.exit_rect[0] + self.exit_rect[2]/2), int(self.exit_rect[1] + self.exit_rect[3]/2)), int(self.exit_r + 5))

    def paint_AI_colliders(self):
        pygame.draw.line(Paint.screen, self.line_colour, (int(Functions.player.x), int(Functions.player.y)), (int(self.x), int(self.y)), 3)
        pygame.draw.circle(Paint.screen, Paint.black, (int(self.x), int(self.y)), self.collide_r, 3)
        pygame.draw.rect(Paint.screen, Paint.black, self.flash_rect, 3)
        pygame.draw.rect(Paint.screen, Paint.black, self.exit_rect, 3)
        pygame.draw.rect(Paint.screen, Paint.dark_blue, (int(self.x)-int(self.r), int(self.y)-int(self.r), int(self.r)*2, int(self.r)*2), 3)

        for point in self.path:
            pygame.draw.circle(Paint.screen, Paint.red, (int(point[0]), int(point[1])), 10)

        for rect in self.rects:
            pygame.draw.rect(Paint.screen, Paint.black, rect, 2)
