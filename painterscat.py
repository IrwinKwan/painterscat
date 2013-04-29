#!/usr/bin/env python

"""
Ludum Dare 26
A 48 hour compo starting April 26, 2013.

The theme? Minimalism.

Game written by Arcana (c 2013).

Code license: GPL
"""

import os
import sys
import math

import numpy
from numpy import random

import random

import pygame
import pygame._view
from pygame.locals import *
from pygame.compat import geterror

from pvector import PVector

from utils import Asset
from utils import Constant
from utils import Stats


import characters
from characters import Cat
from characters import Paint
from characters import Square
from characters import DeadSquare

from characters import Point # Debugging object

import walls
import messages



def load_staccato_sounds():
    staccatos = []
    staccatos.append(Asset.load_sound('staccato-Bb.ogg'))
    staccatos.append(Asset.load_sound('staccato-D.ogg'))
    staccatos.append(Asset.load_sound('staccato-F.ogg'))
    staccatos.append(Asset.load_sound('staccato-Bb-plus.ogg'))
    
    return staccatos

def load_paint_sounds():
    p = []
    p.append(Asset.load_sound('pizzicato-Bb.ogg'))
    p.append(Asset.load_sound('pizzicato-Bb-plus.ogg'))
    p.append(Asset.load_sound('pizzicato-C.ogg'))
    p.append(Asset.load_sound('pizzicato-Eb.ogg'))
    p.append(Asset.load_sound('pizzicato-G.ogg'))

    return p

def choose_color(green_allowed):
    rcolor = Square.colors[0]
    if not green_allowed:
        rcolor = Square.colors[ random.randint(0, len(Square.colors) - 2) ]
    else:
        rcolor = random.choice(Square.colors)
            
    return rcolor
    
def create_background(screen):
    return walls.Walls()

def mouse_angle(background, pos):
    a = math.atan2(background.get_width()/2 - pos[0], pos[1] - background.get_height()/2) 
    return a

def title_screen(background):
    titleMsg, titleRect = Asset.load_one_alpha_image("title.png", Color("white"))
    titleRect = titleMsg.get_rect(midtop=(Constant.SCREEN_RECT.width/2 + 20, 100))
    background.blit(titleMsg, titleRect)
    
    titleMsg, titleRect = Asset.load_one_alpha_image("instructions.png", Color("white"))
    titleRect = titleMsg.get_rect(midtop=(Constant.SCREEN_RECT.width/2 + 20, 360))
    background.blit(titleMsg, titleRect)

    titleMsg, titleRect = Asset.load_one_alpha_image("credits.png", Color("white"))
    titleRect = titleMsg.get_rect(midtop=(Constant.SCREEN_RECT.width/2 + 20, 600))
    background.blit(titleMsg, titleRect)
    
    return background
    
def score_screen(background, statistics):
    
    titleMsg, titleRect = Asset.load_one_alpha_image("gameover.png", Color("white"))
    titleRect = titleMsg.get_rect(midtop=(Constant.SCREEN_RECT.width/2 + 20, 120))
    background.blit(titleMsg, titleRect)
    
    titleMsg, titleRect = Asset.load_one_alpha_image("credits.png", Color("white"))
    titleRect = titleMsg.get_rect(midtop=(Constant.SCREEN_RECT.width/2 + 20, 600))
    background.blit(titleMsg, titleRect)
    
    if pygame.font:
        font = pygame.font.Font("freesansbold.ttf", 26)
        
        secs = "seconds"
        if statistics["time_played"] == 1:
            secs = "second"
            
        score_string = "Time spent in a dream: %s %s" % (statistics["time_played"], secs)
        text = font.render(score_string, True, (0,0,0))
        textpos = text.get_rect(center=(background.get_width()/2, background.get_height()/2 + 25))
        background.blit(text, textpos)
        
        score_string = "Lines painted: %d" % statistics["lines"]
        text = font.render(score_string, True, (0,0,0))
        textpos = text.get_rect(center=(background.get_width()/2, background.get_height()/2 + 50))
        background.blit(text, textpos)
        
        score_string = "Lines painted across the canvas: %d" % statistics["lines_end"]
        text = font.render(score_string, True, (0,0,0))
        textpos = text.get_rect(center=(background.get_width()/2, background.get_height()/2 + 75))
        background.blit(text, textpos)
        
        score_string = "Rectangular forms dreamt up: %d" % statistics["squares_appeared"]
        text = font.render(score_string, True, (0,0,0))
        textpos = text.get_rect(center=(background.get_width()/2, background.get_height()/2 + 100))
        background.blit(text, textpos)
        
        score_string = "Rectangular forms painted over: %d" % statistics["squares"]
        text = font.render(score_string, True, (0,0,0))
        textpos = text.get_rect(center=(background.get_width()/2, background.get_height()/2 + 125))
        background.blit(text, textpos)
        
        score_string = "Rectangular forms bounded: %d" % statistics["squares_bounded"]
        text = font.render(score_string, True, (0,0,0))
        textpos = text.get_rect(center=(background.get_width()/2, background.get_height()/2 + 150))
        background.blit(text, textpos)

        score_string = "Rectangular form bonus! %d" % statistics["squares_erased"]
        text = font.render(score_string, True, (0,0,0))
        textpos = text.get_rect(center=(background.get_width()/2, background.get_height()/2 + 175))
        background.blit(text, textpos)
        
        
    return background
       
def main(winstyle = 0):
    pygame.mixer.quit()
    pygame.init()
    if not pygame.font:
        print ('Warning, fonts disabled')
        
    if not pygame.mixer:
        print ('Warning, sound disabled')
        
    statistics = {
            "time_played": 0,
            "lines": 0,
            "lines_end": 0,
            "squares": 0,
            "squares_appeared": 0,
            "squares_erased": 0,
            "squares_bounded": 0
    }
    
    # global stats = Statistics()
    
    # winstyle = 0  # |FULLSCREEN
    screen_rect = pygame.Rect(0, 0, Constant.SCREEN_SIZE, Constant.SCREEN_SIZE)
    # bestdepth = pygame.display.mode_ok(screen_rect.size, winstyle, 32)
    # screen = pygame.display.set_mode(screen_rect.size, winstyle, bestdepth)
    screen = pygame.display.set_mode(screen_rect.size)
    pygame.mouse.set_visible(False)
    pygame.display.set_caption("The Painter's Cat")
    
    # Assign images to the sprites. Wonder why you don't do this at initialization?
    Cat.images = Asset.load_image("cat_new.png", [(0,0,32,32),(32,0,32,32)], -1)
    Cat.images.append(pygame.transform.flip(Cat.images[0], 1, 0))
    Cat.images.append(pygame.transform.flip(Cat.images[1], 1, 0))
    
    # Background
    levelWalls = walls.Walls(screen)
    background = levelWalls.background 
    # screen.blit(self.background, (0,0))
    # pygame.display.flip()
    
    # Title Screen
    background = title_screen(background)
    screen.blit(background, (0,0))
    
    pygame.display.flip()
    
    # instructionsMsg = messages.TitleMessage("instructions.png", (Constant.SCREEN_RECT.width / 2, 380))
    #     background.blit(instructionsMsg.image, instructionsMsg.rect)
    #     
    #     creditsMsg = messages.TitleMessage("credits.png", (Constant.SCREEN_RECT.width / 2, 550))
    #     background.blit(creditsMsg.image, creditsMsg.rect)
    
    
    # pygame.mixer.init(44100, -16, 2, 65535)
    pygame.mixer.init(44100, -16, 2, 1024)
    
    Asset.play_music("introduction.ogg")
    
    
    on_title = True
    while on_title:
        
        event = pygame.event.wait()
        if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
            return
        elif event.type == MOUSEBUTTONDOWN or (event.type == KEYDOWN and event.key == K_SPACE):
            on_title = False
                
    pygame.mixer.music.fadeout(1000)
    pygame.event.clear()
    keystate = pygame.key.get_pressed()
    pygame.event.wait()
    
    
    staccato_sounds = load_staccato_sounds()
    paint_sounds = load_paint_sounds()
    meow_sound = Asset.load_sound("meow.ogg")
    hit_sound = Asset.load_sound("big_hit.ogg")
        
    # Redraw the background to wipe the screen.
    levelWalls = walls.Walls(screen)
    background = levelWalls.background
    screen.blit(background, (0,0))
    pygame.display.flip()
    
    # Game groups
    deadsquares = pygame.sprite.Group()
    squares = pygame.sprite.Group()
    paints = pygame.sprite.Group()
    boundedsquares = pygame.sprite.Group()

    debug = pygame.sprite.Group()
    
    all = pygame.sprite.LayeredUpdates()
    
    
    # Assign groups to each sprite class
    DeadSquare.containers = deadsquares, all
    Square.containers = squares, all
    Paint.containers = paints, all
    Cat.containers = all
    
    Point.containers = debug, all
    
    angleTextMessage = 0
    angle = 0
    
    Asset.play_music('game.ogg')
    if pygame.mixer:
        pygame.mixer.music.set_volume(0.5)
        
    clock = pygame.time.Clock()
    
    # Initialize starting sprites
    cat = Cat()
    
    start_time = pygame.time.get_ticks()
    
    last_respawn = 0
    respawn_time = 0
    squares_to_spawn = 1
    green_allowed = False
    spawn_buffer = True
    time_to_remove_spawn_buffer = 20000
    global_paint_cooldown = 800 # ms
    last_cooldown = 0
    paint_cooldown = 0
    old_paint_value = 0
    prev_mouse_position = pygame.mouse.get_pos()
    
    going = True
    while cat.alive() and going == True:
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                going = False
            
            #elif event.type == MOUSEBUTTONDOWN:
            #    laser_sounds[random.randint(0,1)].play()
        keystate = pygame.key.get_pressed()

        all.clear(screen, background)
        all.update()
        
        # Player input
        painting = keystate[K_SPACE]
        if painting:
            if global_paint_cooldown - paint_cooldown <= 0:
                paint_cooldown = 0
                last_cooldown = pygame.time.get_ticks()
                random.choice(paint_sounds).play()
                Paint(cat.position(), cat.facing)
                statistics["lines"] += 1
        
        cat.move(prev_mouse_position)
        
        paint_cooldown = pygame.time.get_ticks() - last_cooldown
        respawn_time = pygame.time.get_ticks() - last_respawn
        
        # Spawn squares
        
        # @TODO I want to eventually do "levels" and wipe the screen
        # but we'll see if I can actually get that far
        if len(squares) == 0:
            last_respawn = pygame.time.get_ticks()
            
            for n in range(squares_to_spawn):
                Square(choose_color(green_allowed), spawn_buffer)
                statistics["squares_appeared"] += 1
            
            if squares_to_spawn > 6:
                green_allowed = True
            
            if statistics["squares"] % random.randint(3,4) == 0:
                squares_to_spawn += random.randint(1,2)
                
                
        # Magic Numbers dictating respawn times
        if respawn_time > random.randint(1500,5000):
            last_respawn = pygame.time.get_ticks()
            
            for n in range(random.randint(1,2)):
                Square(choose_color(green_allowed), spawn_buffer)
                statistics["squares_appeared"] += 1
                
        if pygame.time.get_ticks() - start_time > 20000:
            spawn_buffer = False
        
        # Remove all bounded squares and put them into a special group
        for sq in iter(squares):
            if sq.bounded():
                
                statistics["squares_bounded"] += 1
                squares.remove(sq)
                boundedsquares.add(sq)
                
                bounding_paints = sq.get_bounding_paints(paints)
                
                for bounding in bounding_paints:
                    paints.remove(bounding)
                    boundedsquares.add(bounding)
                
                for p in paints:
                    p.kill()
                for s in squares:
                    s.kill()
                    statistics["squares_erased"] += 1
                    
                hit_sound.play()
                
        # Collision detection
        
            
        # @TODO temporarily disabled while I figure out rect badness
        for square in pygame.sprite.spritecollide(cat, squares, False):
            meow_sound.play()
            cat.kill()
        
        
        # Paint hits square.
        for square, paint_list in pygame.sprite.groupcollide(squares, paints, False, False).items():
            statistics["squares"] += 1
            random.choice(staccato_sounds).play()
            square.cut(paint_list)
            
                
        # Square hits square. Both stop growing.
        for square1, square_list in pygame.sprite.groupcollide(squares, squares, False, False).items():
            for square2 in square_list:
                if square1 == square2:
                    pass
                else:
                    square1.growth = 0
                    square2.growth = 0
                    
                    if square1.rect.contains(square2.rect):
                            square2.kill()
                    elif square2.rect.contains(square1.rect):
                            square1.kill()
            
        
        dirty = all.draw(screen)
        pygame.display.update(dirty)
        
        clock.tick(60)
        prev_mouse_position = pygame.mouse.get_pos()
        
    if pygame.mixer:
        pygame.mixer.music.fadeout(1000)
    
    end_time = pygame.time.get_ticks()
    
    statistics["time_played"] = (end_time - start_time)/1000
    
    pygame.event.clear()
    pygame.time.wait(1000)
    
    for sounds in staccato_sounds:
        sounds.fadeout(500)
        
    for sounds in paint_sounds:
        sounds.fadeout(500)

    meow_sound.fadeout(500)
    
    levelWalls = walls.Walls(screen)
    background = levelWalls.background
    
    # @TODO, this is an inconsistent hack
    statistics["lines_end"] = Paint.lines_across
    
    score = score_screen(background, statistics)
    background.blit(score, (0,0))
    screen.blit(background, (0,0))
    pygame.display.flip()
    
    # Play the score music
    Asset.play_music("end.ogg")
    on_score = True
    while on_score:
        event = pygame.event.wait()
        if event.type == QUIT:
            pygame.quit()
        elif event.type == KEYDOWN and event.key == K_ESCAPE or event.type == MOUSEBUTTONDOWN or (event.type == KEYDOWN and event.key == K_SPACE):
            on_score = False
     
    if pygame.mixer:       
        pygame.mixer.music.fadeout(2000)
    pygame.event.clear()
    pygame.quit()

if __name__ == '__main__':
    main()
