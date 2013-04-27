import pygame
from pygame.locals import *

import math

import spritesheet
from utils import Asset

from utils import Constant

import pvector
from pvector import PVector

import numpy
from numpy import random # you know, because ordinary random wasn't good enough or something

class Cat(pygame.sprite.Sprite):
    """A cat. Because this game is going to be about a cat... maybe not"""
    
    images = []
    facing = PVector(0,0)
    
    # The "direction" in which the cat is walking.
    direction = None
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        
        self.image = self.images[0]
        self.rect = self.images[0].get_rect()
        
    def position(self):
        # @NOTE: This doesn't work. Too bad. I probably have to transform the 
        # rect as well as the surface, or something.
        # return self.rect.bottomright
        
        if self.facing == Constant.UP:
            return self.rect.bottomright
        elif self.facing == Constant.DOWN:
            return self.rect.topleft
        elif self.facing == Constant.LEFT:
            return self.rect.topright
        elif self.facing == Constant.RIGHT:
            return self.rect.bottomleft
            
    def update(self):
        """Update the image of the cat and the rect."""
        
        if self.facing == Constant.UP:
            self.image = self.images[0]
            
            
        elif self.facing == Constant.LEFT:
            self.image = self.images[0]
            self.image = pygame.transform.rotate(self.image, 90)

        elif self.facing == Constant.DOWN:
            self.image = self.images[0]
            self.image = pygame.transform.rotate(self.image, 180)
        
        elif self.facing == Constant.RIGHT:
            self.image = self.images[0]
            self.image = pygame.transform.rotate(self.image, -90)
        
        # self.rect = self.image.get_rect()
        
    def move(self):
        
        pos = pygame.mouse.get_pos()
        x = pos[0]
        y = pos[1]
        
        # Stick the "origin" to the lower-right corner of the screen for easiness
        angle = math.atan2(Constant.SCREEN_RECT.width/2 - x, y - Constant.SCREEN_RECT.height/2) + math.pi/4
        if angle > 0:
            pass
        else:
            angle = 2 * math.pi + angle
            
        # Bottom
        if math.pi / 4 > angle and angle >= 0:
            self.rect.bottomright = (x, Constant.SCREEN_RECT.bottom)
            #print "bottom-left Sprite on %d,%d" % self.rect.bottomright
            self.facing = Constant.UP
            
        if math.pi/2 > angle and angle >= math.pi/4:
            self.rect.bottomleft = (x, Constant.SCREEN_RECT.bottom)
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
            self.rect.topleft = (x, Constant.SCREEN_RECT.top)
            #print "top-left Sprite on %d,%d" % self.rect.topleft
            self.facing = Constant.DOWN

        if 3 * math.pi / 2 > angle and angle >= 5 * math.pi / 4:
            self.rect.topright = (x, Constant.SCREEN_RECT.top)
            #print "top-right Sprite on %d,%d" % self.rect.topright
            self.facing = Constant.DOWN

        # Right
        if 7 * math.pi / 4 > angle and angle >= 3 * math.pi/2:
            self.rect.topright = (Constant.SCREEN_RECT.right, y)
            #print "right-top Sprite on %d,%d" % self.rect.topright
            self.facing = Constant.LEFT
            
        if 2 * math.pi > angle and angle >= 7 * math.pi/4:
            self.rect.bottomright = (Constant.SCREEN_RECT.right, y)
            #print "right-bottom Sprite on %d,%d" % self.rect.bottomright
            self.facing = Constant.LEFT
        
        self.rect = self.rect.clamp(Constant.SCREEN_RECT)
      
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
    speed = 1
    
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
        # print "Paint: " + str(self.starting_pos)
        
        if self.direction.equals(Constant.UP):
            # self.image = pygame.Surface([self.size, Constant.SCREEN_SIZE]).convert()
            self.image = pygame.Surface([self.size, self.current_height]).convert()
            self.rect = self.image.get_rect(midbottom = self.starting_pos)
            
        elif self.direction.equals(Constant.LEFT):
            self.image = pygame.Surface([self.current_width, self.size]).convert()
            self.rect = self.image.get_rect(midright = self.starting_pos)
            
        elif self.direction.equals(Constant.DOWN):
            self.image = pygame.Surface([self.size, self.current_height]).convert()
            self.rect = self.image.get_rect(midtop = self.starting_pos)
            
        elif self.direction.equals(Constant.RIGHT):
            self.image = pygame.Surface([self.current_width, self.size]).convert()
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

    def __grow(self):
        """Defines how the line grows."""
        
        if self.current_height > Constant.SCREEN_SIZE:
            return
        if self.current_width > Constant.SCREEN_SIZE:
            return
            
        if self.direction.equals(Constant.UP):
            self.current_height += self.speed
            
        elif self.direction.equals(Constant.LEFT):
            self.current_width += self.speed
            
        elif self.direction.equals(Constant.DOWN):
            self.current_height += self.speed
            
        elif self.direction.equals(Constant.RIGHT):
            self.current_width += self.speed
            
        else:
            # Problem!
            raise DirectionException("Paint, invalid direction!")
        
    def update(self):
        self.__set_direction()
        self.__grow()
        
        pygame.draw.rect(self.image, self.color, [self.size/2, self.size/2, self.current_height, self.current_width])
        
        
        

class Square(pygame.sprite.Sprite):
    """A square. All of the enemies in this game are going to be kind of like
    Mondrian-style squares.
    
    """
    
    blue_color = Color("#010CA4")
    red_color = Color("#C80002")
    yellow_color = Color("#FEFE06")
    
    width = 16 # We know the size of the default sprite
    scale = 1.0
    growth = 0.2
    
    def __init__(self, color="red"):
        pygame.sprite.Sprite.__init__(self, self.containers)
        
        x = random.randint(Constant.SCREEN_RECT.left, Constant.SCREEN_RECT.width)
        y = random.randint(Constant.SCREEN_RECT.top, Constant.SCREEN_RECT.height)
        
        self.position = (x,y)
        # print self.position
        
        # Squares are 16x16 and have 5 frames
        rects = [(17 * x, 0, self.width, self.width) for x in range(0,5)]
        
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
        self.rect = self.image.get_rect()
        
        self.scaled_size = int(self.width * self.scale)
    
    def __grow(self):
        if self.rect.top < Constant.SCREEN_RECT.top:
            return
            
        elif self.rect.bottom > Constant.SCREEN_RECT.bottom:
            return
            
        elif self.rect.left < Constant.SCREEN_RECT.left:
            return
            
        elif self.rect.right > Constant.SCREEN_RECT.right:
            return
            
        else:
            self.scale += self.growth
            self.scaled_size = int(self.width * self.scale)
            
            
    def update(self):
        self.__grow()
        
        print "self.scaled_size: " + str(self.scaled_size)
        
        self.image = pygame.transform.scale(self.image,
            (self.scaled_size, self.scaled_size))
        self.rect = self.image.get_rect()
        self.rect = self.rect.clamp(Constant.SCREEN_RECT)
        self.rect.center = self.position
        
        #print "Scale size: " + str(scale_size)
        #print "Image rect: " + str(self.image.get_rect())

        