import os, sys
import pygame
from pygame.locals import *
from pygame.compat import geterror

import spritesheet

from pvector import PVector

class Stats():
    lines_across = 0
        
        
class Constant():
    WALL_SIZE = 16
    SCREEN_SIZE = 640
    PAINT_SIZE = 8
    BACKGROUND_WIDTH = 608
    
    LEFT = PVector(-1,0)
    RIGHT = PVector(1,0)
    DOWN = PVector(0,1)
    UP = PVector(0,-1)
    
    #SCREEN_RECT = pygame.Rect(Constant.WALL_SIZE, Constant.WALL_SIZE, Constant.BACKGROUND_WIDTH, Constant.BACKGROUND_WIDTH)
    SCREEN_RECT = Rect(16, 16, 608, 608)
    
class Asset(object):
    
    # main_dir = os.path.split(os.path.abspath(__file__))[0]
    data_dir = os.path.join('data')

    @classmethod
    def resource_path(cls, relative):
        if hasattr(sys, "_MEIPASS"):
            return os.path.join(sys._MEIPASS, relative)
        return os.path.join(relative)
    
    @classmethod
    def load_font(cls,name):
        fullname = Asset.resource_path(os.path.join(Asset.data_dir, name))
        font = None
        try:
            font = pygame.font.Font(fontfile, 26)
        except pygame.error:
            print ('Cannot load font:', fullname)
            raise SystemExit(str(geterror()))
        return font
        
    @classmethod
    def load_one_image(cls, name, colorkey=None):
        fullname = Asset.resource_path(os.path.join(Asset.data_dir, name))
        try:
            image = pygame.image.load(fullname)
        except pygame.error:
            print ('Cannot load image:', fullname)
            raise SystemExit(str(geterror()))
        image = image.convert()
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, RLEACCEL)
        return image, image.get_rect()
        
    @classmethod
    def load_one_alpha_image(cls, name, colorkey=None):
        fullname = Asset.resource_path(os.path.join(Asset.data_dir, name))
        try:
            image = pygame.image.load(fullname)
        except pygame.error:
            print ('Cannot load image:', fullname)
            raise SystemExit(str(geterror()))
        image = image.convert_alpha()
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, RLEACCEL)
        return image, image.get_rect()
                
    @classmethod
    def load_image(cls, name, rects, colorkey=None):
        if type(name) is not str:
            raise TypeError
            
        fullname = Asset.resource_path(os.path.join(Asset.data_dir, name))
        ss = spritesheet.spritesheet(fullname)
        images = None
        try:
            images = ss.images_at(rects, colorkey=colorkey)
        except pygame.error:
            print ('Cannot load image:', fullname)
            raise SystemExit(str(geterror()))

        return images
    
    @classmethod
    def load_sound(cls, name):
        class NoneSound:
            def play(self): pass
        if not pygame.mixer or not pygame.mixer.get_init():
            return NoneSound()
        fullname = Asset.resource_path(os.path.join(Asset.data_dir, name))
        try:
            sound = pygame.mixer.Sound(fullname)
        except pygame.error:
            print ('Cannot load sound: %s' % fullname)
            raise SystemExit(str(geterror()))
        return sound
    
    @classmethod
    def play_music(cls, name):    
        music = Asset.resource_path(os.path.join(Asset.data_dir, name))
        pygame.mixer.music.load(music)
        pygame.mixer.music.play(-1)
        