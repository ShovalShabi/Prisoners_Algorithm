import pygame
import os


class PrisonerV:
    def __init__(self, start_location, num, screen):
        self.location = start_location
        self.num = num
        self.img_prisoner = pygame.image.load(os.path.join('Resources', 'SP1_front.png'))
        self.screen = screen

    def draw_prisoner(self):
        self.screen.blit(self.img_prisoner, self.location)

    def rotate_prisoner(self):
        pass
