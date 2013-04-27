import os
import pygame
from pygame.locals import *
from pygame.compat import geterror

import spritesheet

class Asset(object):
    
    main_dir = os.path.split(os.path.abspath(__file__))[0]
    images_dir = os.path.join(main_dir, 'images')
    sounds_dir = os.path.join(main_dir, 'sounds')

    @classmethod
    def load_one_image(cls, name, colorkey=None):
        fullname = os.path.join(Asset.images_dir, name)
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
    def load_image(cls, name, rects, colorkey=None):
        if type(name) is not str:
            raise TypeError
            
        fullname = os.path.join(Asset.images_dir, name)
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
        fullname = os.path.join(Asset.sounds_dir, name)
        try:
            sound = pygame.mixer.Sound(fullname)
        except pygame.error:
            print ('Cannot load sound: %s' % fullname)
            raise SystemExit(str(geterror()))
        return sound