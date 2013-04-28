import pygame
from pygame.locals import *

import math
import random

import spritesheet
from utils import Asset

from utils import Constant
from utils import Stats

import pvector
from pvector import PVector

# A debugging object.
class Point(pygame.sprite.Sprite):

    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self, position, color = Color("magenta"), width = 4, height = 4):
       # Call the parent class (Sprite) constructor
       pygame.sprite.Sprite.__init__(self, self.containers)

       # Create an image of the block, and fill it with a color.
       # This could also be an image loaded from the disk.
       self.image = pygame.Surface([width, height]).convert()
       
       self.original = self.image
       self.position = position
       # Fetch the rectangle object that has the dimensions of the image
       # Update the position of this object by setting the values of rect.x and rect.y
       self.rect = self.image.get_rect()
       self.rect.x = self.position[0]
       self.rect.y = self.position[1]
       self.size = width
       
       pygame.draw.ellipse(self.image, color, self.rect)
       
    def update(self):
        self.image = pygame.transform.scale(self.original, (self.size, self.size))
        self.rect = self.image.get_rect()
        self.rect.move_ip( (self.position[0] - self.size/2, self.position[1] - self.size/2) )
        # self.rect.clamp_ip(pygame.Rect(0,0,SCREEN_SIZE,SCREEN_SIZE))


class Cat(pygame.sprite.Sprite):
    """A cat. Because this game is going to be about a cat... maybe not"""
    
    animation_cycle = 240
    images = []
    
    # "facing" is the direction the cat paints lines.
    facing = Constant.UP
    
    # "direction" is the way the cat walks, and is either "right" or "left".
    # normal people would have used an integer or boolean but I had to be fancy and use a
    # PVector.
    direction = Constant.RIGHT 
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        
        self.image = self.images[0]
        self.rect = self.images[0].get_rect()
        self.rect.move_ip(Constant.SCREEN_RECT.width/2, Constant.SCREEN_RECT.bottom)
        self.mask = pygame.mask.from_surface(self.image)
        self.frame = 0
        
    def position(self):

        if self.facing == Constant.UP:
            if self.direction == Constant.RIGHT:
                return self.rect.bottomright
            elif self.direction == Constant.LEFT:
                return self.rect.bottomleft
                
        elif self.facing == Constant.DOWN:
            if self.direction == Constant.LEFT:
                return self.rect.topleft
            elif self.direction == Constant.RIGHT:
                return self.rect.topright
                
        elif self.facing == Constant.LEFT:
            if self.direction == Constant.LEFT:
                return self.rect.bottomright
            elif self.direction == Constant.RIGHT:
                return self.rect.topright
                
        elif self.facing == Constant.RIGHT:
            if self.direction == Constant.LEFT:
                return self.rect.topleft
            elif self.direction == Constant.RIGHT:
                return self.rect.bottomleft
            
    def update(self):
        """Update the image of the cat and the rect."""
        
        self.frame = pygame.time.get_ticks()
        # self.image = self.images[self.frame//self.animation_cycle % 2]
        
            
        if self.facing == Constant.UP:
            if self.direction == Constant.RIGHT:
                self.image = self.images[self.frame//self.animation_cycle % 2]
            elif self.direction == Constant.LEFT:
                self.image = self.images[self.frame//self.animation_cycle % 2 + 2]
            
            # self.image = pygame.transform.rotate(self.image, 0)
            
        elif self.facing == Constant.LEFT:
            if self.direction == Constant.RIGHT:
                self.image = self.images[self.frame//self.animation_cycle % 2]
            elif self.direction == Constant.LEFT:
                self.image = self.images[self.frame//self.animation_cycle % 2 + 2]
                
            self.image = pygame.transform.rotate(self.image, 90)
            
            

        elif self.facing == Constant.DOWN:
            if self.direction == Constant.RIGHT:
                self.image = self.images[self.frame//self.animation_cycle % 2 + 2]
            elif self.direction == Constant.LEFT:
                self.image = self.images[self.frame//self.animation_cycle % 2]
            
            self.image = pygame.transform.rotate(self.image, 180)
        
        elif self.facing == Constant.RIGHT:
            if self.direction == Constant.RIGHT:
                self.image = self.images[self.frame//self.animation_cycle % 2]
            elif self.direction == Constant.LEFT:
                self.image = self.images[self.frame//self.animation_cycle % 2 + 2]
                
            self.image = pygame.transform.rotate(self.image, -90)
        
        # self.rect = self.image.get_rect()
        
    def _set_direction(self, current_mouse, prev_mouse):
        if self.facing.equals(Constant.UP) or self.facing.equals(Constant.DOWN):
            if current_mouse[0] == prev_mouse[0]:
                pass
            elif current_mouse[0] > prev_mouse[0]:
                self.direction = Constant.RIGHT
            else:
                self.direction = Constant.LEFT
                
        elif self.facing.equals(Constant.DOWN):
            if current_mouse[0] == prev_mouse[0]:
                pass
            elif current_mouse[0] > prev_mouse[0]:
                self.direction = Constant.LEFT
            else:
                self.direction = Constant.RIGHT
                
        elif self.facing.equals(Constant.LEFT):
            if current_mouse[1] == prev_mouse[1]:
                pass
            elif current_mouse[1] > prev_mouse[1]:
                self.direction = Constant.LEFT
            else:
                self.direction = Constant.RIGHT
                
        elif self.facing.equals(Constant.RIGHT):
            if current_mouse[1] == prev_mouse[1]:
                pass
            elif current_mouse[1] > prev_mouse[1]:
                self.direction = Constant.RIGHT
            else:
                self.direction = Constant.LEFT
        
    def move(self, old_mouse_pos):
        
        pos = pygame.mouse.get_pos()
        x = pos[0]
        y = pos[1]
        
        # Stick the "origin" to the lower-right corner of the screen for easiness
        angle = math.atan2(Constant.SCREEN_RECT.width/2 - x, y - Constant.SCREEN_RECT.height/2) + math.pi/4
        if angle > 0:
            pass
        else:
            angle = 2 * math.pi + angle
            
        oldpos = self.rect.center
            
        # Bottom
        if math.pi / 4 > angle and angle >= 0:
            self.rect.bottomright = (x, Constant.SCREEN_RECT.bottom)
            #print "bottom-left Sprite on %d,%d" % self.rect.bottomright
            self.facing = Constant.UP
            
            
        if math.pi/2 > angle and angle >= math.pi/4:
            self.rect.bottomleft = (x, Constant.SCREEN_RECT.bottom)
            #print "bottom-right Sprite on %d,%d" % self.rect.bottomleft
            self.facing = Constant.UP
            
            # if mouse_moved.equals(Constant.RIGHT):
            #                 self.direction == Constant.RIGHT
            #             else:
            #                 self.direction == Constant.LEFT
            
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
        
        self._set_direction(pos, old_mouse_pos)
      
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
    accel = 0.1
    painting = False
    
    lines_across = 0
    
    def __init__(self, pos, direction):
        pygame.sprite.Sprite.__init__(self, self.containers)
        
        self.image = None
        self.rect = None
        self.direction = direction
        self.starting_pos = pos
        self.current_height = self.size
        self.current_width = self.size
        self.painting = True
        
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

    def __paint_across(self):
        """Defines how the line grows."""
        
        if not self.painting:
            return
            
        if self.current_height >= Constant.SCREEN_SIZE:
            Paint.lines_across += 1
            self.painting = False
            return
        elif self.current_width >= Constant.SCREEN_SIZE:
            Paint.lines_across += 1
            self.painting = False
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
        
        self.speed += self.accel
        
    def update(self):
        self.__set_direction()
        self.__paint_across()
        
        pygame.draw.rect(self.image, self.color, [self.size/2, self.size/2, self.current_height, self.current_width])

# A dead square needs its own class because
# it doesn't collide with anything.
class DeadSquare(pygame.sprite.Sprite):
    def __init__(self, position, color, width, height):
        pygame.sprite.Sprite.__init__(self, self.containers)
        
        self.position = position
        
        if color == "red":
            self.color = random.choice(self.reds)
        elif color == "blue":
            self.color = random.choice(self.blues)
        elif color == "yellow":
            self.color = random.choice(self.yellows)
        elif color == "green":
            self.color = random.choice(self.greens)
        else:
            self.color = self.red_color
            
        # self.images = Asset.load_image("square_" + color + ".png", rects, (120,120,120))
        self.image = pygame.Surface([self.width, self.width]).convert()
        self.original_image = self.image
        self.image.fill(self.color)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]

        self.width = width
        self.height = height
        
    def update(self):
        if self.width <= 0 or self.height <= 0:
            self.kill()
            
        self.image = pygame.transform.scale(self.original_image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.move_ip( (self.position[0] - self.width/2, self.position[1] - self.height/2) )
        
class Square(pygame.sprite.Sprite):
    """A square. All of the enemies in this game are going to be kind of like
    Mondrian-style squares.
    
    """
    
    colors = ["blue", "red", "yellow", "green"]
    
    blues = [ Color("#010CA4"), Color("#0f3aa3"), Color("#0d3ca6")]
    reds = [ Color("#C80002"), Color("#dc1301"), Color("#d21801") ]
    yellows = [ Color("#FEFE06"), Color("#fefe06"), Color("#ccbd00")]
    greens = [Color("#00a501"), Color("#00a800"), Color("#05a600")]
    
    default_width = 16 # We know the size of the default sprite
    default_height = 16
    scale = 1.0
    growth = 0.1
    
    animation_cycle = 240
    
    bound_left = False
    bound_right = False
    bound_top = False
    bound_bottom = False
    
    bounded_paints = []
    
    restricted_width = 32 # places not to spawn to not kill the player
    
    def __choose_random_spawn_point(self, spawn_buffer):
        
        if spawn_buffer:
            x = random.randint(Constant.SCREEN_RECT.left + self.restricted_width, Constant.SCREEN_RECT.width - self.restricted_width)
            y = random.randint(Constant.SCREEN_RECT.top + self.restricted_width, Constant.SCREEN_RECT.height - self.restricted_width)
        
        else:
            x = random.randint(Constant.SCREEN_RECT.left, Constant.SCREEN_RECT.width - self.default_width)
            y = random.randint(Constant.SCREEN_RECT.top, Constant.SCREEN_RECT.height - self.default_width)
        
        self.position = [x,y]
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]
        
    def __choose_spawn_point(self, x, y):

        self.position = [x,y]
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]
        
    # def __check_square_spawn(self):
    #     
    #     invalid_spawn = True
    #     while invalid_spawn:
    #         invalid_spawn = False
    #         for square in pygame.sprite.spritecollide(self, self.containers[0], False):
    #             if square == self:
    #                 print "Self, ignore"
    #             else:
    #                 print "Other blocks hit."
    #                 invalid_spawn = True
    #                 
    #                 # Find out where the nearest empty space is
    #                 if square.rect.x > self.rect.x:
    #                     pass
    #                 if square.rect.y > self.rect.y:
    #                     pass
    #     
    #     print "Done checking self-collision with the group."
            
        
    def __init__(self, color="red", spawn_buffer = True):
        pygame.sprite.Sprite.__init__(self, self.containers)
        
        # Squares are 16x16 and have 5 frames
        # rects = [(17 * x, 0, self.width, self.width) for x in range(0,5)]
        # statistics["squares_appeared"] += 1
        
        if color == "red":
            self.color = random.choice(self.reds)
            self.growth = 0.1
        elif color == "blue":
            self.color = random.choice(self.blues)
            self.growth = 0.15
        elif color == "yellow":
            self.color = random.choice(self.yellows)
            self.growth = 0.20
        elif color == "green":
            self.color = random.choice(self.greens)
            self.growth = 0.24
        else:
            self.color = self.red_color
            self.growth = 0.1
            
        # self.images = Asset.load_image("square_" + color + ".png", rects, (120,120,120))
        self.image = pygame.Surface([self.default_width, self.default_height]).convert()
        self.original_image = self.image
        self.image.fill(self.color)
        
        self.rect = self.image.get_rect()
        
        self.__choose_random_spawn_point(spawn_buffer)
        
        
        # self.__check_square_spawn()
        
        # self.mask = pygame.mask.from_surface(self.image)
        
        self.width = int(self.default_width * self.scale)
        self.height = int(self.default_height * self.scale)
    
    def __grow(self):
        
        if self.rect.top <= Constant.SCREEN_RECT.top:
            self.rect.top = Constant.SCREEN_RECT.top
            self.growth = 0
            self.bound_top = True
            return
            
        elif self.rect.bottom >= Constant.SCREEN_RECT.bottom:
            self.rect.bottom = Constant.SCREEN_RECT.bottom
            self.growth = 0
            self.bound_bottom = True
            return
            
        elif self.rect.left <= Constant.SCREEN_RECT.left:
            self.rect.left == Constant.SCREEN_RECT.left
            self.growth = 0
            self.bound_left = True
            return
            
        elif self.rect.right >= Constant.SCREEN_RECT.right:
            self.rect.right = Constant.SCREEN_RECT.right
            self.bound_right = True
            return
            
        # Don't reset height and width if we're not growing
        if self.growth > 0:
            self.scale += self.growth
            self.width = int(self.default_width * self.scale)
            self.height = int(self.default_height * self.scale)

    def bounded(self):
        return self.bound_left and self.bound_right and self.bound_top and self.bound_bottom

    def update(self):
        self.__grow()
        
        self.image = pygame.transform.scale(self.original_image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.move_ip( (self.position[0] - self.width/2, self.position[1] - self.height/2) )

    def __cut_vertical(self, cutter):
        """Cuts the square vertically on the smaller side."""
        irect = self.rect.clip(cutter.rect)

        # Calculate width on both sides
        leftwidth = cutter.rect.left - self.rect.left
        rightwidth = self.rect.right - cutter.rect.right

        self.width = leftwidth if leftwidth > rightwidth else rightwidth

        if self.width <= 0:
            self.kill()

        if leftwidth > rightwidth:
            self.bound_right = True
            self.position[0] = self.rect.left + self.width/2
            if self.width % 2 == 1:
                print "verticalcut odd keep left"
                self.position[0] += 1
            else:
                print "verticalcut even keep left"
        else:
            self.bound_left = True
            self.position[0] = self.rect.right - self.width/2
            
            
            if self.width % 2 == 1:
                print "verticalcut odd keep right"
                self.position[0] -= 1
            else:
                print "verticalcut even keep right"
                # print "self.rect.right = %d " % self.rect.right
                # print "cutter.rect.left = %d " % cutter.rect.left
                print irect
                # self.position[0] -= 1


    def __cut_horizontal(self, cutter):
        """Cuts the square horizontally on the smaller side."""
        irect = self.rect.clip(cutter.rect)

        # Calculate height on both sides
        topheight = cutter.rect.top - self.rect.top
        bottomheight = self.rect.bottom - cutter.rect.bottom

        self.height = topheight if topheight > bottomheight else bottomheight

        if self.height <= 0:
            self.kill()

        print "topheight: %d ~~ bottomheight: %d" % (topheight, bottomheight)
        if topheight > bottomheight:
            self.bound_bottom = True
            self.position[1] = self.rect.top + self.height/2
            
            if self.height % 2 == 1:
                print "horizontalcut odd keep top"
                # self.position[1] -= 1
            else:
                print "horizontalcut even keep top"
                self.position[1] += 1
                self.width += 1
        else:
            self.bound_top = True
            self.position[1] = self.rect.bottom - self.height/2
            
            if self.height % 2 == 1:
                print "horizontalcut odd keep bottom"
                self.position[1] -= 1
            else:
                print "horizontalcut even keep bottom"
            

    def cut(self, paint_list):
        """Cuts the square where the paint intersects"""
        
        print "Cut at time %d" % pygame.time.get_ticks()
        # Stop growing
        self.growth = 0
        
        for paint in paint_list:
            
            if paint.painting:            
                if paint.direction.equals(Constant.UP) or paint.direction.equals(Constant.DOWN):
                    self.__cut_vertical(paint)
                elif paint.direction.equals(Constant.LEFT) or paint.direction.equals(Constant.RIGHT):
                    self.__cut_horizontal(paint)
            else:
                # Kill both the paint and the square
                self.kill()
                paint.kill()

        
        
        
