import pygame

'''
Represents the Bird object. An image of the bird is used to create the bird rect.
The bird position is updated according to constants.py and redrawn on the screen. 
'''
class Bird:
    def __init__(self, x, y, scale_factor):
        # convert alpha is used to convert images that have transparent background
        self.image = pygame.transform.scale(pygame.image.load('../assets/bird.png').convert_alpha(),
                                            (int(50 * scale_factor), int(35 * scale_factor)))
        self.rect = self.image.get_rect(center=(x, y))
        self.movement = 0

    def update(self, gravity):
        self.movement += gravity
        # centery represent the y coordinate
        self.rect.centery += int(self.movement)

    def flap(self, power):
        self.movement = -power

    def draw(self, screen):
        rotated_image = pygame.transform.rotozoom(self.image, -self.movement * 3, 1)
        screen.blit(rotated_image, self.rect)
