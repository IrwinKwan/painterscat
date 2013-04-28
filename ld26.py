#!/usr/bin/env python
"""Ludum Dare 26
A 48 hour compo starting April 26, 2013.

The theme? Minimalism.

Game written by Arcana (2013).
"""

import os
import sys
import math

import numpy
from numpy import random

import random

import pygame
from pygame.locals import *
from pygame.compat import geterror

from pvector import PVector
from pixelperfectcollision import pixel_perfect_collision
from utils import Asset
from utils import Constant


import characters
from characters import Cat
from characters import Paint
from characters import Square

import walls
import messages



def load_staccato_sounds():
    staccatos = []
    staccatos.append(Asset.load_sound('staccato-Bb.wav'))
    staccatos.append(Asset.load_sound('staccato-D.wav'))
    staccatos.append(Asset.load_sound('staccato-F.wav'))
    staccatos.append(Asset.load_sound('staccato-Bb-plus.wav'))
    
    return staccatos

def load_paint_sounds():
    p = []
    p.append(Asset.load_sound('pizzicato-Bb.wav'))
    p.append(Asset.load_sound('pizzicato-Bb-plus.wav'))
    p.append(Asset.load_sound('pizzicato-C.wav'))
    p.append(Asset.load_sound('pizzicato-D.wav'))
    p.append(Asset.load_sound('pizzicato-Eb.wav'))
    # p.append(Asset.load_sound('pizzicato-F.wav'))
    p.append(Asset.load_sound('pizzicato-G.wav'))

    return p
        
def create_background(screen):
    return walls.Walls()

def mouse_angle(background, pos):
    # center = PVector(background.get_width() / 2, background.get_height() / 2)
    # mouse = PVector(pos[0], pos[1])
    # 
    # mouse.sub(center)
    # center.sub(center)
    # center.x = -1
    # 
    # 
    # print center
    # print mouse
    # print center.angle_between(mouse)
    # 
    # return center.angle_between(mouse)
    
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
        font = pygame.font.Font(None, 26)
        
        secs = "seconds"
        if statistics["time_played"] == 1:
            secs = "second"
            
        score_string = "Time spent dreaming: %s %s" % (statistics["time_played"], secs)
        text = font.render(score_string, True, (0,0,0))
        textpos = text.get_rect(center=(background.get_width()/2, background.get_height()/2 + 25))
        background.blit(text, textpos)
        
        score_string = "Lines painted: %d" % statistics["lines"]
        text = font.render(score_string, True, (0,0,0))
        textpos = text.get_rect(center=(background.get_width()/2, background.get_height()/2 + 50))
        background.blit(text, textpos)
        
        score_string = "Lines that reached across the canvas: %d" % statistics["lines_end"]
        text = font.render(score_string, True, (0,0,0))
        textpos = text.get_rect(center=(background.get_width()/2, background.get_height()/2 + 75))
        background.blit(text, textpos)
        
        score_string = "Squares appeared: %d" % statistics["squares_appeared"]
        text = font.render(score_string, True, (0,0,0))
        textpos = text.get_rect(center=(background.get_width()/2, background.get_height()/2 + 100))
        background.blit(text, textpos)
        
        score_string = "Squares painted over: %d" % statistics["squares"]
        text = font.render(score_string, True, (0,0,0))
        textpos = text.get_rect(center=(background.get_width()/2, background.get_height()/2 + 125))
        background.blit(text, textpos)
        

        
        
    return background
       
def main(winstyle = 0):
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
            "squares_appeared": 0
        }
    
    winstyle = 0  # |FULLSCREEN
    screen_rect = pygame.Rect(0, 0, Constant.SCREEN_SIZE, Constant.SCREEN_SIZE)
    bestdepth = pygame.display.mode_ok(screen_rect.size, winstyle, 32)
    screen = pygame.display.set_mode(screen_rect.size, winstyle, bestdepth)
    
    pygame.mouse.set_visible(False)
    pygame.display.set_caption("The Painter's Cat")
    
    # Assign images to the sprites. Wonder why you don't do this at initialization?
    Cat.images = Asset.load_image("cat_main.png", [(0,0,32,32),(33,0,32,32)], -1)
    
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
    
    
    
    on_title = True
    while on_title:
        
        event = pygame.event.wait()
        if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
            return
        elif event.type == MOUSEBUTTONDOWN or (event.type == KEYDOWN and event.key == K_SPACE):
            on_title = False
                
    pygame.event.clear()
    
    staccato_sounds = load_staccato_sounds()
    paint_sounds = load_paint_sounds()
    meow_sound = Asset.load_sound("meow.wav")
    
    # Redraw the background to wipe the screen.
    levelWalls = walls.Walls(screen)
    background = levelWalls.background
    screen.blit(background, (0,0))
    pygame.display.flip()
    
    # Game groups
    paints = pygame.sprite.Group()
    squares = pygame.sprite.Group()
    all = pygame.sprite.RenderUpdates()
    
    
    # Assign groups to each sprite class
    Cat.containers = all
    Paint.containers = paints, all
    Square.containers = squares, all
    
    
    
    angleTextMessage = 0
    angle = 0
    
    clock = pygame.time.Clock()
    
    # Initialize starting sprites
    cat = Cat()
    # Square()
    
    start_time = pygame.time.get_ticks()
    
    last_respawn = 0
    respawn_time = 0
    
    going = True
    while cat.alive() and going == True:
        
                
        for event in pygame.event.get():
            if event.type == QUIT:
                going = False
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
            random.choice(paint_sounds).play()
            Paint(cat.position(), cat.facing)
            statistics["lines"] += 1
        
        cat.move()
        
        respawn_time = pygame.time.get_ticks() - last_respawn
        print respawn_time
        
        # Spawn a square
        # @TODO I want to eventually do "levels" and wipe the screen
        # but we'll see if I can actually get that far
        if len(squares) == 0:
            last_respawn = pygame.time.get_ticks()
            
            rcolor = random.choice(Square.colors)
            
            # Naive way to select a color that's not green
            while rcolor == "green":
                rcolor = random.choice(Square.colors)
                
            Square(rcolor)
            statistics["squares_appeared"] += 1
            
            if statistics["squares"] > random.randint(3,6):
                Square(random.choice(Square.colors))
                statistics["squares_appeared"] += 1
                
            if statistics["squares"] > random.randint(6,10):
                Square(random.choice(Square.colors))
                Square(random.choice(Square.colors))
                statistics["squares_appeared"] += 2
                
        # Magic Numbers dictating respawn times
        if respawn_time > random.randint(3000,5000):
            last_respawn = pygame.time.get_ticks()
            Square()
            statistics["squares_appeared"] += 1
            
            
        # Collision detection.
        # @TODO temporarily disabled while I figure out rect badness
        for square in pygame.sprite.spritecollide(cat, squares, False):
            meow_sound.play()
            # cat.kill()
        
        
        # Paint hits square. It should be limited to
        # the end of the paint rather than the body?
        for square, paints in pygame.sprite.groupcollide(squares, paints, False, False):
            statistics["squares"] += 1
            random.choice(staccato_sounds).play()
            
            
            
            # if spawn_more 
        
        dirty = all.draw(screen)
        pygame.display.update(dirty)
        
        # @TODO: Change this back to 60 after testing
        clock.tick(20)
        
    #if pygame.mixer:
    #    pygame.mixer.music.fadeout(1000)
    
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
    
    score = score_screen(background, statistics)
    background.blit(score, (0,0))
    screen.blit(background, (0,0))
    pygame.display.flip()
    
    # Play the score music
    
    on_score = True
    while on_score:
        event = pygame.event.wait()
        if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE or event.type == MOUSEBUTTONDOWN or (event.type == KEYDOWN and event.key == K_SPACE):
            on_score = False
            
    pygame.event.clear()
    pygame.quit()

if __name__ == '__main__':
    main()
