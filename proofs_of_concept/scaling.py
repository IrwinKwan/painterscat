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
       self.rect.x = self.position[0]
       self.rect.y = self.position[1]
       self.size = width
       
    def update(self):
        self.image = pygame.transform.scale(self.original, (self.size, self.size))
        self.rect = self.image.get_rect()
        self.rect.move_ip( (self.position[0] - self.size/2, self.position[1] - self.size/2) )
        # self.rect.clamp_ip(pygame.Rect(0,0,SCREEN_SIZE,SCREEN_SIZE))

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

      # Fetch the rectangle object that has the dimensions of the image
      # Update the position of this object by setting the values of rect.x and rect.y
      self.rect = self.image.get_rect()
      self.rect.center = position
              
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
all = pygame.sprite.RenderUpdates()
Block.containers = blocks, all
Red.containers = reds, all

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            quit()
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            quit()
        elif event.type == KEYDOWN and event.key == K_DOWN:
            for b in blocks:
                if b.size > 1:
                    b.size -= 1
                
        elif event.type == KEYDOWN and event.key == K_UP:
            for b in blocks:
                b.size += 10
                    
    
    all.clear(screen, background)
    all.update()
    
    if len(blocks) < 1:
        Block( (random.randint(0, 640), random.randint(0, 640)) )
        
    if len(reds) < 4:
        Red( (random.randint(0, 640), random.randint(0, 640)) )
        
    for b in pygame.sprite.groupcollide(blocks, reds, True, True):
        print "Collision!"
        
    dirty = all.draw(screen)
    pygame.display.update(dirty)
    clock.tick(24)

pygame.quit()