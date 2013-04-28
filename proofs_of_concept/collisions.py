#!/usr/bin/env python

import os,sys
import math
import random
import pygame
from pygame.locals import *
from pygame.compat import geterror

class Block(pygame.sprite.Sprite):

    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self, position, color = Color("white"), width = 40, height = 40):
       # Call the parent class (Sprite) constructor
       pygame.sprite.Sprite.__init__(self, self.containers)

       # Create an image of the block, and fill it with a color.
       # This could also be an image loaded from the disk.
       self.image = pygame.Surface([width, height])
       self.image.fill(color)
       
       self.original = self.image
       self.position = position
       # Fetch the rectangle object that has the dimensions of the image
       # Update the position of this object by setting the values of rect.x and rect.y
       self.rect = self.image.get_rect()
       self.rect.centerx = self.position[0]
       self.rect.centery = self.position[1]
       self.width = width
       self.height = height
       
    def update(self):
        self.image = pygame.transform.scale(self.original, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.move_ip((self.position[0] - self.width/2, self.position[1] - self.height/2))

class Red(pygame.sprite.Sprite):

    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self, position, color = Color("red"), width = 20, height = 20):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self, self.containers)

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.original = self.image

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()
        self.rect.center = position

        self.width = width
        self.height = height
        self.position = position
      
    def update(self):
        self.image = pygame.transform.scale(self.original, (self.width, self.height))
        self.rect = self.image.get_rect()
        # self.rect.topleft = (self.position[0] - self.width/2, self.position[1] - self.height/2)
        self.rect.move_ip((self.position[0] - self.width/2, self.position[1] - self.height/2))
    
    def __cut_vertical(self, b):
        irect = self.rect.clip(b.rect)
        # Green((irect.center), Color("green"), width = irect.width, height = irect.height)
        
        # Calculate width on both sides
        leftwidth = b.rect.left - self.rect.left
        rightwidth = self.rect.right - b.rect.right
        
        self.width = leftwidth if leftwidth > rightwidth else rightwidth
        
        if self.width <= 0:
            self.kill()
        
        if leftwidth > rightwidth:
            self.position[0] = self.rect.left + self.width/2
        else:
            self.position[0] = self.rect.right - self.width/2

    def __cut_horizontal(self, b):
        irect = self.rect.clip(b.rect)
        # Green((irect.center), Color("green"), width = irect.width, height = irect.height)

        # Calculate height on both sides
        topheight = b.rect.top - self.rect.top
        bottomheight = self.rect.bottom - b.rect.bottom
        
        self.height = topheight if topheight > bottomheight else bottomheight

        print self.height
        
        if self.height <= 0:
            self.kill()

        if topheight > bottomheight:
            self.position[1] = self.rect.top + self.height/2
        else:
            self.position[1] = self.rect.bottom - self.height/2

    def shatter(self, bs):
        for b in bs:
            
            # self.__cut_vertical(b)
            self.__cut_horizontal(b)
            
            

class Green(pygame.sprite.Sprite):

    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self, position, color = Color("green"), width = 3, height = 3):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self, self.containers)

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()
        self.rect.center = position

def main():
    pygame.init()

    SCREEN_SIZE = 640

    screen_rect = pygame.Rect(0,0,SCREEN_SIZE,SCREEN_SIZE)
    screen = pygame.display.set_mode(screen_rect.size)

    pygame.mouse.set_visible(True)

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((50, 50, 50))
    screen.blit(background, (0,0))
    pygame.display.flip()

    blocks = pygame.sprite.Group()
    reds = pygame.sprite.Group()
    greens = pygame.sprite.Group()
    all = pygame.sprite.RenderUpdates()
    Block.containers = blocks, all
    Red.containers = reds, all
    Green.containers = greens, all

    clock = pygame.time.Clock()

    Red( [300, 200], Color("red"), width = 100, height = 200 )

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                quit()
           
        keystate = pygame.key.get_pressed()
        all.clear(screen, background)
        all.update()
        
        if keystate[K_LEFT]:
            for b in blocks:
                b.width -= 1
                if b.width <= 0:
                    b.width = 1
        elif keystate[K_RIGHT]:
            for b in blocks:
                b.width += 1
        elif keystate[K_DOWN]:
            for b in blocks:
                b.position[1] += 1
        elif keystate[K_UP]:
            for b in blocks:
                b.position[1] -= 1
                    
    
    
    
        if len(blocks) < 1:
            # Block( (random.randint(0, 640), random.randint(0, 640)) )
            Block( [200, 450] )
        
        #if len(reds) < 1:
            # Red( (random.randint(0, 640), random.randint(0, 640)) )
            # Red( [300, 400], Color("red"), width = 100, height = 200 )
    
        i = 0
        for r, bs in pygame.sprite.groupcollide(reds, blocks, False, False).items():
            r.shatter(bs)
        
        dirty = all.draw(screen)
        pygame.display.update(dirty)
        clock.tick(120)

    pygame.quit()

if __name__ == "__main__":
    main()