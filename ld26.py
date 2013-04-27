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

import pygame
from pygame.locals import *
from pygame.compat import geterror

from pvector import PVector

from utils import Asset
from utils import Constant

import characters
from characters import Cat
from characters import Paint
from characters import Square

import walls
from messages import Console

def load_staccato_sounds():
    staccatos = []
    staccatos.append(Asset.load_sound('staccato-Bb.wav'))
    staccatos.append(Asset.load_sound('staccato-D.wav'))
    staccatos.append(Asset.load_sound('staccato-F.wav'))
    
    return staccatos

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


    
       
def main(winstyle = 0):
    pygame.init()
    if not pygame.font:
        print ('Warning, fonts disabled')
        
    if not pygame.mixer:
        print ('Warning, sound disabled')
    
    winstyle = 0  # |FULLSCREEN
    screen_rect = pygame.Rect(0, 0, Constant.SCREEN_SIZE, Constant.SCREEN_SIZE)
    bestdepth = pygame.display.mode_ok(screen_rect.size, winstyle, 32)
    screen = pygame.display.set_mode(screen_rect.size, winstyle, bestdepth)
    
    pygame.mouse.set_visible(False)
    pygame.display.set_caption("Mondrian Squares")
    
    # Assign images to the sprites. Wonder why you don't do this at initialization?
    Cat.images = Asset.load_image("cat_main.png", [(0,0,32,32),(33,0,32,32)], -1)
    
    # Background
    levelWalls = walls.Walls(screen)
    background = levelWalls.background 
    pygame.display.flip()
    
    
    
    staccato_sounds = load_staccato_sounds()
    meow_sound = Asset.load_sound("meow.wav")
    
    # Game groups
    paints = pygame.sprite.Group()
    squares = pygame.sprite.Group()
    all = pygame.sprite.RenderUpdates()
    
    
    # Assign groups to each sprite class
    Cat.containers = all
    Paint.containers = paints, all
    Square.containers = squares, all
    
    angleText = Console(background, background.get_width()/2, 40)
    
    angleTextMessage = 0
    angle = 0
    
    clock = pygame.time.Clock()
    
    # Initialize starting sprites
    cat = Cat()
    Square()
    
    going = True
    while cat.alive():
        
                
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
            Paint(cat.position(), cat.facing)
            
            # paint_sounds[random.randint(0,1)].play()
        
        cat.move()
        
        # Spawn a square
        # @TODO I want to eventually do "levels" and wipe the screen
        # but we'll see if I can actually get that far
        if len(squares) == 0:
            Square()
            # Square()
            
        # Collision detection.
        for square in pygame.sprite.spritecollide(cat, squares, True, False):
            meow_sound.play()
            cat.kill()
        
        
        # Paint hits square. It should be limited to
        # the end of the paint rather than the body?
        for squares_collision in pygame.sprite.groupcollide(squares, paints, True, True):
            staccato_sounds[0].play()
            squares_collision.cut()
        
        dirty = all.draw(screen)
        pygame.display.update(dirty)
        
        clock.tick(60)
        
    if pygame.mixer:
        pygame.mixer.music.fadeout(1000)
    pygame.time.wait(1000)
    pygame.quit()

if __name__ == '__main__':
    main()
