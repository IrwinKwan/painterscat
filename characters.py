import pygame
from pygame.locals import *

import math

import spritesheet
from utils import Asset

from utils import Constant

import pvector
from pvector import PVector


class Cat(pygame.sprite.Sprite):
    """A cat. Because this game is going to be about a cat... maybe not"""
    
    images = []
    facing = PVector(0,0)
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        
        self.image = self.images[0]
        self.rect = self.images[0].get_rect()
        
        self.game_rect = pygame.Rect(Constant.WALL_SIZE, Constant.WALL_SIZE, Constant.BACKGROUND_WIDTH, Constant.BACKGROUND_WIDTH)
        
    def position(self):
        if self.facing == Constant.UP:
            return self.rect.bottomright
        
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
            
        # Bottom
        if math.pi / 4 > angle and angle >= 0:
            self.rect.bottomright = (x, self.game_rect.bottom)
            #print "bottom-left Sprite on %d,%d" % self.rect.bottomright
            self.facing = Constant.UP
            
        if math.pi/2 > angle and angle >= math.pi/4:
            self.rect.bottomleft = (x, self.game_rect.bottom)
            #print "bottom-right Sprite on %d,%d" % self.rect.bottomleft
            self.facing = Constant.UP
            
        # Left
        if 3 * math.pi / 4 > angle and angle > math.pi/2:
            self.rect.bottomleft = (16, y)
            #print "left-bottom Sprite on %d,%d" % self.rect.bottomleft
            self.facing = Constant.RIGHT

        if math.pi > angle and angle > math.pi/2:
            self.rect.topleft = (16, y)
            #print "left-top Sprite on %d,%d" % self.rect.topleft
            self.facing = Constant.RIGHT
              
        # Top
        if 5 * math.pi / 4 > angle and angle >= math.pi:
            self.rect.topleft = (x, self.game_rect.top)
            #print "top-left Sprite on %d,%d" % self.rect.topleft
            self.facing = Constant.DOWN

        if 3 * math.pi / 2 > angle and angle >= 5 * math.pi / 4:
            self.rect.topright = (x, self.game_rect.top)
            #print "top-right Sprite on %d,%d" % self.rect.topright
            self.facing = Constant.DOWN

        # Right
        if 7 * math.pi / 4 > angle and angle >= 3 * math.pi/2:
            self.rect.topright = (self.game_rect.right, y)
            #print "right-top Sprite on %d,%d" % self.rect.topright
            self.facing = Constant.LEFT
            
        if 2 * math.pi > angle and angle >= 7 * math.pi/4:
            self.rect.bottomright = (self.game_rect.right, y)
            #print "right-bottom Sprite on %d,%d" % self.rect.bottomright
            self.facing = Constant.LEFT
            
        self.rect = self.rect.clamp(self.game_rect)
      
class DirectionException(Exception):
    pass

class Paint(pygame.sprite.Sprite):
    """Paint comes out of your character and moves to the other side of the screen, leaving a
    black border. It's deadly while it's painting.
    
    Ideally, the logic also is that if you put down a paint line, you can't put
    another one down close to an existing one."""
    
    images = []
    size = 8
    color = Color("black")
    speed = 10
    
    def __init__(self, pos, direction):
        pygame.sprite.Sprite.__init__(self, self.containers)
        
        self.image = None
        self.rect = None
        self.direction = direction
        self.starting_pos = pos
        self.current_height = self.size
        self.current_width = self.size
        
        self.__set_direction()
        
        # self.image.fill(self.color)
        
        
        # pygame.draw.rect(self.image, self.color, [self.size/2, self.size/2, self.size, self.size])
        
        
    
    def __set_direction(self):
        if self.direction.equals(Constant.UP):
            # self.image = pygame.Surface([self.size, Constant.SCREEN_SIZE]).convert()
            self.image = pygame.Surface([self.size, self.current_height]).convert()
            self.rect = self.image.get_rect(midbottom = self.starting_pos)
            
        elif self.direction.equals(Constant.LEFT):
            self.image = pygame.Surface([Constant.SCREEN_SIZE, self.size]).convert()
            self.rect = self.image.get_rect(midright = self.starting_pos)
            
        elif self.direction.equals(Constant.DOWN):
            self.image = pygame.Surface([self.size, Constant.SCREEN_SIZE]).convert()
            self.rect = self.image.get_rect(midtop = self.starting_pos)
            
        elif self.direction.equals(Constant.RIGHT):
            self.image = pygame.Surface([Constant.SCREEN_SIZE, self.size]).convert()
            self.rect = self.image.get_rect(midleft = self.starting_pos)
            
        else:
            # Problem!
            raise DirectionException("Paint: You're not up down left or right.")

    def __grow_up(self):
        if self.rect.height < Constant.SCREEN_SIZE:
            
            # This is supposed to grow.
            self.image = pygame.Surface([self.size, self.size]).convert()
            self.rect = self.__set_rect()
            pygame.draw.rect(self.image, self.color, [self.size/2, self.size/2, self.current_width, self.current_height])

        
    def update(self):
        self.__set_direction()
        pygame.draw.rect(self.image, self.color, [self.size/2, self.size/2, self.current_height, self.size])
        self.current_height += 1
        print "Paint: height = " + str(self.current_height)
        # self.image.fill(self.color)
        

class Square(pygame.sprite.Sprite):
    """A square. All of the enemies in this game are going to be kind of like
    Mondrian-style squares.
    
    """
    
    def __init__(self, color):
        pygame.sprite.Sprite.__init__(self, self.containers)
        
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

        