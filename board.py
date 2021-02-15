# Sneak Game

import pygame
import Values
import Paint
import Functions
from Stage1 import Stage1

pygame.init()

stgs = []
stgs.append(Stage1())

stgs[0].set_return_path()
stgs[0].add_AI()
stgs[0].set_player()

# Functions.add_AI(3)

# Main game loop
running = True
while running:

    if Values.restart:
        Values.restart = False
        Functions.player.life = Functions.player.max_life
        Functions.player.alive = True
        stgs[Values.stage_num].remove_AI()
        stgs[Values.stage_num].add_AI()
        stgs[Values.stage_num].set_player()
        stgs[Values.stage_num].laser_set()

    while Values.paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Values.paused = False
                running = False
            if not Values.can_pause:
                Values.can_pause = True

        Paint.paint_back_master()
        stgs[Values.stage_num].draw_stage_back_master()
        Paint.paint_back()
        stgs[Values.stage_num].draw_stage_back()
        Paint.paint_for()
        stgs[Values.stage_num].draw_stage_for()
        Paint.text_paint()
        Functions.mouse_pause_check()
        Paint.paint_flip()

    while Values.starting:
        Paint.start_paint()
        Paint.paint_flip()
        Functions.mouse_check_start()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Values.starting = False
                running = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT or Values.end:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            if not Values.can_pause:
                Values.can_pause = True
            if not Values.can_dev:
                Values.can_dev = True
        if event.type == pygame.KEYUP and event.key == pygame.K_e:
            if not Values.can_E:
                Values.can_E = True

    Paint.paint_back_master()
    stgs[Values.stage_num].draw_stage_back_master()
    Paint.paint_back()
    stgs[Values.stage_num].draw_stage_back()
    Paint.paint_for()
    stgs[Values.stage_num].draw_stage_for()
    Paint.text_paint()
    Functions.AI_main()
    Functions.Player_main(stgs[Values.stage_num].lasers, stgs[Values.stage_num].walls, stgs[Values.stage_num].pots, stgs[Values.stage_num].lights)
    Functions.bullet_main(stgs[Values.stage_num].walls)
    Functions.mouse_check()
    Paint.paint_flip()

    for ai in Functions.ais:
        ai.check_walls(stgs[Values.stage_num].walls)

pygame.quit()
