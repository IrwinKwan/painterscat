import pygame

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
        