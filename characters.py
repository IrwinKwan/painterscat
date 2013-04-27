import pygame
from pygame.locals import *

import math

import spritesheet
from utils import Asset

class Cat(pygame.sprite.Sprite):
    """A cat. Because this game is going to be about a cat."""
    
    def __init__(self, screen_rect, wall_size):
        pygame.sprite.Sprite.__init__(self)
        self.images = Asset.load_image("cat_main.png", [(0,0,32,32),(33,0,32,32)], -1)
        self.image = self.images[0]
        self.rect = self.images[0].get_rect()
        
        self.screen_rect = screen_rect
        
    def move(self):
        self.rect = self.rect.clamp(self.screen_rect)
        pos = pygame.mouse.get_pos()
        x = pos[0]
        y = pos[1]
        
        # Stick the "origin" to the lower-right corner of the screen for easiness
        angle = math.atan2(self.screen_rect.width/2 - x, y - self.screen_rect.height/2) + math.pi/4
        if angle > 0:
            pass
        else:
            angle = 2 * math.pi + angle
            
        # Bottom edge
        if math.pi/2 > angle and angle >= 0:
            self.rect.midbottom = (x, self.screen_rect.height - 16)
            print "bottom Sprite on %d,%d" % self.rect.midbottom
            
        # Left edge
        if math.pi > angle and angle > math.pi/2:
            self.rect.midleft = (16, y)
            print "left Sprite on %d,%d" % self.rect.midleft
                    
        # Top edge
        if 3 * math.pi / 2 > angle and angle >= math.pi:
            self.rect.midtop = (x, 16)
            print "top Sprite on %d,%d" % self.rect.midtop
            
        # Right edge
        if 2 * math.pi > angle and angle >= 3 * math.pi/2:
            self.rect.midright = (self.screen_rect.width - 16, y)
            print "right Sprite on %d,%d" % self.rect.midright
      
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
        