import pygame
from utils import Constant
from utils import Asset

class TitleMessage(pygame.sprite.Sprite):
    def __init__(self, filename, position):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = Asset.load_one_image(filename)
        self.rect = \
            self.image.get_rect(centerx = Constant.SCREEN_RECT.width/2).move(position)

        print self.image
        print self.rect
        
class Console:
    def __init__(self, background, xposition, yposition):
        if pygame.font.Font:
            self.font = pygame.font.Font(None, 18)
            self.background = background
            self.xposition = xposition
            self.yposition = yposition
            
            
    def render(self, msg):
        text = self.font.render(str(msg), True, (148,0,211))
        textpos = text.get_rect(centerx=self.xposition, centery=self.yposition)
        self.background.blit(text, textpos)
        