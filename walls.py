import pygame
from utils import Asset

class Walls:
    def __init__(self, screen):
        self.image, self.rect = Asset.load_one_image('wall.png', (255,255,255))
        self.screen_rect = screen.get_size()
        self.background = pygame.Surface(screen.get_size())
        self.background = self.background.convert()
        self.background.fill((255, 255, 255))
        
        self.wall_width = self.image.get_width()
        self.wall_height = self.image.get_height()
        
        self.render(screen)
        
    def render(self, screen):
        # I guess I should repeatedly blit the wall onto the screen
        for xpos in range(0, self.screen_rect[0], self.image.get_width()):
            self.background.blit(self.image, (xpos, 0))
            
        for xpos in range(0, self.screen_rect[0], self.image.get_width()):
            self.background.blit(self.image, (xpos, self.screen_rect[1] - self.image.get_height()))

            
        for ypos in range(0, self.screen_rect[1], self.image.get_height()):
            self.background.blit(self.image, (0, ypos))
            
        for ypos in range(0, self.screen_rect[1], self.image.get_width()):
            self.background.blit(self.image, (self.screen_rect[0] - self.image.get_width(), ypos))
            
        screen.blit(self.background, (0,0))
        