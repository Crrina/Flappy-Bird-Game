import pygame
from constants import SCREEN_HEIGHT

'''
The Pipe object. There is a top and a bottom pipe on the same x coordinate.
'''
class Pipe:
    def __init__(self, x, y, is_top):
        self.image = pygame.Surface((100, SCREEN_HEIGHT))
        self.image.fill((123, 63, 0))  # Brown color for pipes
        if is_top:
            self.rect = self.image.get_rect(midbottom=(x, y))
            self.image = pygame.transform.flip(self.image, False, True)
        else:
            self.rect = self.image.get_rect(midtop=(x, y))

    def move(self):
        self.rect.centerx -= 5

    def draw(self, screen):
        screen.blit(self.image, self.rect)
