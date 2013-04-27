import pygame
from pygame.locals import *

import math

import spritesheet
from utils import Asset
from utils import Constant

class Cat(pygame.sprite.Sprite):
    """A cat. Because this game is going to be about a cat... maybe not"""
    
    images = []
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        
        self.image = self.images[0]
        self.rect = self.images[0].get_rect()
        
        self.game_rect = pygame.Rect(Constant.WALL_SIZE, Constant.WALL_SIZE, Constant.BACKGROUND_WIDTH, Constant.BACKGROUND_WIDTH)
        
    def move(self):
        
        pos = pygame.mouse.get_pos()
        x = pos[0]
        y = pos[1]
        
        # Stick the "origin" to the lower-right corner of the screen for easiness
        angle = math.atan2(self.game_rect.width/2 - x, y - self.game_rect.height/2) + math.pi/4
        if angle > 0:
            pass
        else:
            angle = 2 * math.pi + angle
            
        if math.pi / 4 > angle and angle >= 0:
            self.rect.bottomright = (x, self.game_rect.bottom)
            print "bottom-left Sprite on %d,%d" % self.rect.bottomright
            
        if math.pi/2 > angle and angle >= math.pi/4:
            self.rect.bottomleft = (x, self.game_rect.bottom)
            print "bottom-right Sprite on %d,%d" % self.rect.bottomleft
            
        if 3 * math.pi / 4 > angle and angle > math.pi/2:
            self.rect.bottomleft = (16, y)
            print "left-bottom Sprite on %d,%d" % self.rect.bottomleft

        if math.pi > angle and angle > math.pi/2:
            self.rect.topleft = (16, y)
            print "left-top Sprite on %d,%d" % self.rect.topleft
                
        if 5 * math.pi / 4 > angle and angle >= math.pi:
            self.rect.topleft = (x, self.game_rect.top)
            print "top-left Sprite on %d,%d" % self.rect.topleft

        if 3 * math.pi / 2 > angle and angle >= 5 * math.pi / 4:
            self.rect.topright = (x, self.game_rect.top)
            print "top-right Sprite on %d,%d" % self.rect.topright

        if 7 * math.pi / 4 > angle and angle >= 3 * math.pi/2:
            self.rect.topright = (self.game_rect.right, y)
            print "right-top Sprite on %d,%d" % self.rect.topright
            
        if 2 * math.pi > angle and angle >= 7 * math.pi/4:
            self.rect.bottomright = (self.game_rect.right, y)
            print "right-bottom Sprite on %d,%d" % self.rect.bottomright
            
        self.rect = self.rect.clamp(self.game_rect)
      
class Square(pygame.sprite.Sprite):
    """A square. All of the enemies in this game are going to be kind of like
    Mondrian-style squares.
    
    """
    
    def __init__(self, color):
        pygame.sprite.Sprite.__init__(self)
        
        width = 16
        # Squares are 16x16 and have 5 frames
        rects = [(17 * x, 0, 16,16) for x in range(0,5)]
        
        if color == "red":
            pass
        elif color == "blue":
            pass
        elif color == "yellow":
            pass
        elif color == "white":
            pass
        else:
            color = "white"
            
        self.images = Asset.load_image("square_" + color + ".png", rects, -1)
        self.image = self.images[0]
        self.rect = self.images[0].get_rect()
        
    def update(self):
        pos = pygame.mouse.get_pos()
        self.rect.midtop = pos
        
class OuterWall(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = Asset.load_image("cat_main.png", [(0,0,32,32),(33,0,32,32)], -1)
        self.image = self.images[0]
        self.rect = self.images[0].get_rect()
        
    def update(self):
        pass
        