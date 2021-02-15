import pygame
import Values
import Functions
import math

pygame.init()

# Colours
gray = (60, 60, 60)             # ground
dark_gray = (60, 60, 60)        # tower 3
light_gray = (128, 128, 128)    # light light
light_mid_gray = (100, 100, 100)    # light light
mid_gray = (90, 90, 90)         # light mid
brown = (160, 82, 45)           # pot
green = (50, 205, 50)           # background
dark_green = (0, 128, 0)        # menu
black = (0, 0, 0)               # text
white = (255, 255, 255)         # general
blue = (0, 191, 255)            # tower 1
dark_blue = (0, 0, 128)         # tower 1 dark
yellow = (255, 255, 0)          # tower 2 / start wave
lime_yellow = (173, 255, 47)    # tower 5
purple = (255, 0, 255)          # tower 3
dark_purple = (75, 0, 130)      # tower 3 dark
dark_yellow = (128, 128, 0)     # start wave / tower 2 dark
red = (220, 20, 60)             # enemy light
dark_red = (128, 0, 0)          # enemy heave
now_white_pause = white
now_white_dev = white

# Images

# Fonts
font1 = pygame.font.Font('freesansbold.ttf', 20)
font2 = pygame.font.Font('freesansbold.ttf', 40)
font3 = pygame.font.Font('freesansbold.ttf', 15)
font4 = pygame.font.Font('freesansbold.ttf', 30)
font_start_big = pygame.font.Font('freesansbold.ttf', 80)
font_pause = pygame.font.Font('freesansbold.ttf', 160)

# Set up the drawing window
screen = pygame.display.set_mode([Values.screen_width, Values.screen_height])
pygame.display.set_caption('Show Text')

# Text - Starting
title1_text = font_start_big.render('Caleb\'s', True, black, blue)
title1_textRect = title1_text.get_rect()
title1_textRect.center = (Values.screen_width / 2, 80)
title2_text = font_start_big.render('Sneak \'em up', True, black, blue)
title2_textRect = title2_text.get_rect()
title2_textRect.center = (Values.screen_width / 2, 200)
start_button_text = font_start_big.render('Start', True, black, white)
start_button_textRect = start_button_text.get_rect()
start_button_textRect.center = (Values.screen_width / 2, Values.screen_height - 350)

# Text - pause
pause_button_text = font1.render('Pause', True, black, None)
pause_button_textRect = pause_button_text.get_rect()
pause_button_textRect.center = (Values.pause_rect[0] + Values.pause_rect[2] / 2, Values.pause_rect[1] + Values.pause_rect[3] / 2)
pause_text = font_pause.render('Paused...', True, white, None)
pause_textRect = pause_text.get_rect()
pause_textRect.center = (Values.screen_width / 2, Values.screen_height / 2)

# Text - dev
dev_button_text = font1.render('Dev Mode', True, black, None)
dev_button_textRect = dev_button_text.get_rect()
dev_button_textRect.center = (Values.dev_rect[0] + Values.dev_rect[2] / 2, Values.dev_rect[1] + Values.dev_rect[3] / 2)

# Text - exit
exit_button_text = font1.render('Exit', True, black, None)
exit_button_textRect = exit_button_text.get_rect()
exit_button_textRect.center = (Values.exit_rect[0] + Values.exit_rect[2] / 2, Values.exit_rect[1] + Values.exit_rect[3] / 2)

# Text - dead
dead_text = font_pause.render('You got caught', True, white, None)
dead_textRect = dead_text.get_rect()
dead_textRect.center = (Values.screen_width / 2, Values.screen_height / 2)

# Text - life
life_text = font1.render('Life: ' + str(Functions.player.life), True, black, None)
life_textRect = life_text.get_rect()
life_textRect.center = (Values.life_rect[0] + Values.life_rect[2] / 2, Values.life_rect[1] + Values.life_rect[3] / 2)

# Text - restart
restart_button_text = font1.render('Restart', True, black, None)
restart_button_textRect = restart_button_text.get_rect()
restart_button_textRect.center = (Values.restart_rect[0] + Values.restart_rect[2] / 2, Values.restart_rect[1] + Values.restart_rect[3] / 2)

def change_colour():
    global now_white_pause
    global now_white_dev

    if Values.paused:
        now_white_pause = gray
    else:
        now_white_pause = white

    if Values.dev_view:
        now_white_dev = gray
    else:
        now_white_dev = white

def paint_back_master():
    # background
    screen.fill(gray)

def paint_back():
    # display AI lights
    for ai in Functions.ais:
        ai.paint_AI_mid()

    for ai in Functions.ais:
        ai.paint_AI_light()

def paint_for():
    global life_text

    # set colour
    change_colour()

    # display AI
    for ai in Functions.ais:
        ai.paint_AI_flash()

    if Values.dev_view:
        for ai in Functions.ais:
            ai.paint_AI_colliders()

    for ai in Functions.ais:
        ai.paint_AI()

    for ammo in Functions.bullets:
        ammo.paint_bullet()

    Functions.player.paint_player()

    if Values.dev_view:
        Functions.player.paint_player_colliders()

    # pause, restart and dev button
    pygame.draw.rect(screen, light_gray, (0, 0, Values.screen_width, 100))

    pygame.draw.rect(screen, now_white_pause, Values.pause_rect)
    pygame.draw.rect(screen, black, Values.pause_rect, 5)
    screen.blit(pause_button_text, pause_button_textRect)

    pygame.draw.rect(screen, white, Values.restart_rect)
    pygame.draw.rect(screen, black, Values.restart_rect, 5)
    screen.blit(restart_button_text, restart_button_textRect)

    pygame.draw.rect(screen, now_white_dev, Values.dev_rect)
    pygame.draw.rect(screen, black, Values.dev_rect, 5)
    screen.blit(dev_button_text, dev_button_textRect)

    pygame.draw.rect(screen, red, Values.exit_rect)
    pygame.draw.rect(screen, black, Values.exit_rect, 5)
    screen.blit(exit_button_text, exit_button_textRect)

    life_text = font1.render('Life: ' + str(Functions.player.life), True, black, None)
    pygame.draw.rect(screen, green, Values.life_rect)
    pygame.draw.rect(screen, black, Values.life_rect, 5)
    screen.blit(life_text, life_textRect)

    pygame.draw.line(screen, black, (0, 100), (Values.screen_width, 100), 5)

def text_paint():
    # pause menu display
    if Values.paused:
        screen.blit(pause_text, pause_textRect)

    # death text
    if not Functions.player.alive:
        screen.blit(dead_text, dead_textRect)

def start_paint():
    screen.fill(blue)

    pygame.draw.rect(screen, white, Values.start_button_rect)
    pygame.draw.rect(screen, black, Values.start_button_rect, 20)

    screen.blit(title1_text, title1_textRect)
    screen.blit(title2_text, title2_textRect)
    screen.blit(start_button_text, start_button_textRect)

def paint_flip():
    pygame.display.flip()
