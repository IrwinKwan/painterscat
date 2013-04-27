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
import characters
import walls
from messages import Console

if not pygame.font: print ('Warning, fonts disabled')
if not pygame.mixer: print ('Warning, sound disabled')

# @TODO: This is going to have to become a class later
def create_laser_sounds():
    lasers = []
    lasers.append(Asset.load_sound('laser_01.wav'))
    lasers.append(Asset.load_sound('laser_02.wav'))
    
    return lasers

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


    
       
def main():
    pygame.init()
    screen = pygame.display.set_mode((640,640))
    
    
    pygame.mouse.set_visible(True)
    
    pygame.display.set_caption("Squares")
    
    levelWalls = walls.Walls(screen)
    background = levelWalls.background
    pygame.display.flip()
    
    screen_rect = screen.get_rect()
    
    clock = pygame.time.Clock()
    laser_sounds = create_laser_sounds()
    cat = characters.Cat(screen_rect, [levelWalls.wall_width,levelWalls.wall_height])
    
    allsprites = pygame.sprite.RenderPlain((cat))
    angleText = Console(background, background.get_width()/2, 40)
    
    angleTextMessage = 0
    angle = 0
    
    screen_rect = screen.get_size()

    
    going = True
    while going:
        clock.tick(60)
                
        for event in pygame.event.get():
            if event.type == QUIT:
                going = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                going = False
            elif event.type == MOUSEBUTTONDOWN:
                laser_sounds[random.randint(0,1)].play()
            elif event.type == MOUSEMOTION:
                cat.move()
                mousex, mousey = event.pos
                
                # Do some angle calculations
                angle = mouse_angle(background, event.pos)
                angleTextMessage = angle
                
        
        allsprites.update()
        screen.blit(background, (0,0))
        allsprites.draw(screen)
        # angleText.render(angleTextMessage)
        pygame.display.flip()
        
    pygame.quit()

if __name__ == '__main__':
    main()
