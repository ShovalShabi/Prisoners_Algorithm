import pygame
from settings import *
import os

class BoxV:
    def __init__(self, screen, num):
        self.num = num
        self.next_box_num = -1
        self.screen = screen
        self.location = None
        self.img_box = pygame.image.load(os.path.join('Resources', 'chest_closed.png'))

    def draw_box(self, box_index, inc, font):
        x = 150 + box_index * CELL_SIZE
        y = 80 + inc * CELL_SIZE
        rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
        text_surface = font.render(str(box_index + 1 + inc * MAX_BOX_WIDTH), True, YELLOW)
        text_rect = text_surface.get_rect()
        text_rect.center = self.img_box.get_rect().center
        self.img_box.blit(text_surface, text_rect)
        self.screen.blit(self.img_box, rect)
        return x, y

    def replace(self):
        pass
