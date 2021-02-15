import pygame
import Values
import random
import math
from AI import AI
from Player import Player
# from Player import Player

pygame.init()

ais = []
bullets = []
player = Player(750, 150)

def Player_main(lasers, walls, pots, lights):
    if player.alive:
        player.move()
        laser_kill(lasers)
        player.check_life()
        key_move(lasers, check_laser(lasers))
        player.check_walls(walls)
        player.check_hidden(pots)
        player.check_light(lights)

def check_laser(lasers):
    on_laser_switch = False
    laser_switch_index = 0

    for i in range(len(lasers)):
        if player.x + player.r > lasers[i].switch_rect[0] and player.x - player.r < lasers[i].switch_rect[0] + lasers[i].switch_rect[2] and \
           player.y + player.r > lasers[i].switch_rect[1] and player.y - player.r < lasers[i].switch_rect[1] + lasers[i].switch_rect[3]:
            on_laser_switch = True
            laser_switch_index = i
            break

    return [on_laser_switch, laser_switch_index]

def laser_kill(lasers):
    for laser in lasers:
        if player.x + player.r > laser.laser_rect[0] and player.x - player.r < laser.laser_rect[0] + laser.laser_rect[2] and \
           player.y + player.r > laser.laser_rect[1] and player.y - player.r < laser.laser_rect[1] + laser.laser_rect[3]:
            if laser.laser_on:
                player.alive = False

def AI_main():
    for guy in ais:
        guy.collider_update()
        if guy.rotating:
            guy.rotate()
        else:
            guy.move()
        guy.check_player()

def add_AI(num):
    for i in range(num):
        path = set_path(4)
        temp = AI(path)
        ais.append(temp)

def bullet_main(walls):
    for ammo in bullets:
        ammo.move()
        remove_bullet(ammo, walls)

def remove_bullet(ammo, walls):
    for wall in walls:
        if wall[0] + wall[2] > ammo.x - ammo.r and wall[0] < ammo.x + ammo.r and \
           wall[1] + wall[3] > ammo.y - ammo.r and wall[1] < ammo.y + ammo.r:
            bullets.remove(ammo)

    if ammo.x + ammo.r > Values.screen_width or ammo.x - ammo.r < 0 or ammo.y + ammo.r > Values.screen_height or ammo.y - ammo.r < 100:
        bullets.remove(ammo)

    if player.x + player.r > ammo.x - ammo.r and player.x - player.r < ammo.x + ammo.r and\
       player.y + player.r > ammo.y - ammo.r and player.y - player.r < ammo.y + ammo.r:
        player.life -= 1
        bullets.remove(ammo)

def set_path(num):
    path = []

    for i in range(num):
        point = [random.uniform(50, Values.screen_width - 50), random.uniform(50, Values.screen_height - 50)]
        path.append(point)

    return path

def key_move(lasers, lasering):
    up_down = False
    left_right = False

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_w]:
        y_dir = -1
        up_down = True
    if pressed[pygame.K_s]:
        y_dir = 1
        up_down = True
    if pressed[pygame.K_a]:
        x_dir = -1
        left_right = True
    if pressed[pygame.K_d]:
        x_dir = 1
        left_right = True

    if up_down:
        if left_right:
            player.y += y_dir * math.sqrt(player.speed ** 2 / 2)
        else:
            player.y += y_dir * player.speed

    if left_right:
        if up_down:
            player.x += x_dir * math.sqrt(player.speed ** 2 / 2)
        else:
            player.x += x_dir * player.speed

    if pressed[pygame.K_e]:
        if lasering[0] and Values.can_E:
            Values.can_E = False
            lasers[lasering[1]].laser_on = not lasers[lasering[1]].laser_on

def mouse_check_start():
    if pygame.mouse.get_pressed() == (1, 0, 0):
        if Values.start_button_rect[0] < pygame.mouse.get_pos()[0] < Values.start_button_rect[0] + Values.start_button_rect[2] and \
           Values.start_button_rect[1] < pygame.mouse.get_pos()[1] < Values.start_button_rect[1] + Values.start_button_rect[3]:
            Values.starting = False

def mouse_pause_check():
    if pygame.mouse.get_pressed() == (1, 0, 0):
        if Values.pause_rect[0] < pygame.mouse.get_pos()[0] < Values.pause_rect[0] + Values.pause_rect[2] and \
           Values.pause_rect[1] < pygame.mouse.get_pos()[1] < Values.pause_rect[1] + Values.pause_rect[3]:
            if Values.can_pause:
                Values.paused = not Values.paused
                Values.can_pause = False

def mouse_check():
    if pygame.mouse.get_pressed() == (1, 0, 0):

        if Values.exit_rect[0] < pygame.mouse.get_pos()[0] < Values.exit_rect[0] + Values.exit_rect[2] and \
           Values.exit_rect[1] < pygame.mouse.get_pos()[1] < Values.exit_rect[1] + Values.exit_rect[3]:
            Values.end = True

        if Values.pause_rect[0] < pygame.mouse.get_pos()[0] < Values.pause_rect[0] + Values.pause_rect[2] and \
           Values.pause_rect[1] < pygame.mouse.get_pos()[1] < Values.pause_rect[1] + Values.pause_rect[3]:
            if Values.can_pause and player.alive:
                Values.paused = not Values.paused
                Values.can_pause = False

        if Values.restart_rect[0] < pygame.mouse.get_pos()[0] < Values.restart_rect[0] + Values.restart_rect[2] and \
           Values.restart_rect[1] < pygame.mouse.get_pos()[1] < Values.restart_rect[1] + Values.restart_rect[3]:
            Values.restart = True

        if Values.dev_rect[0] < pygame.mouse.get_pos()[0] < Values.dev_rect[0] + Values.dev_rect[2] and \
           Values.dev_rect[1] < pygame.mouse.get_pos()[1] < Values.dev_rect[1] + Values.dev_rect[3]:
            if Values.can_dev:
                Values.dev_view = not Values.dev_view
                Values.can_dev = False