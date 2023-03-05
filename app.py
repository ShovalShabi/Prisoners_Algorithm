import math
import os
from settings import *
import sys
import pygame


class App:
    def __init__(self) -> None:
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.SysFont('monospace', FONT_SIZE, bold=True)
        self.button_y = None
        self.button_x = None
        self.clock = pygame.time.Clock()
        self.state = 'start'
        self.running = True
        self.num_of_boxes = 286
        self.num_of_prisoners = 1
        self.size = (screen_width, screen_height)
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Prisoners")

    def run(self):
        while self.running:
            if self.state == 'start':
                self.start_events()
                self.start_draw()
        pygame.quit()
        sys.exit()

    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def start_draw(self):
        self.screen.fill(BLACK)
        # self.draw_menu()
        self.draw_boxes()
        # self.draw_prisoners()
        pygame.display.update()

    def draw_menu(self):
        # Draw the screen
        self.button_x = (screen_width - button_width) // 2
        self.button_y = (screen_height - button_height) // 2
        self.draw_button(RED, self.button_x, self.button_y, button_width, button_height, "Start")
        self.draw_button(GREEN, self.button_x, self.button_y + 100, button_width, button_height, "Reset")
        pygame.display.flip()

    def draw_button(self, color, x, y, width, height, text):
        pygame.draw.rect(self.screen, color, (x, y, width, height))
        text_surface = self.font.render(text, True, BLACK)
        text_rect = text_surface.get_rect()
        text_rect.center = ((x + width // 2), (y + height // 2))
        self.screen.blit(text_surface, text_rect)

    def draw_prisoners(self):
        pass

    def draw_box(self, col, inc):
        box = pygame.image.load("Resources/chest_closed.png")
        rect = pygame.Rect(col * BOX_SIZE, BOX_SIZE + inc * BOX_SIZE, BOX_SIZE, BOX_SIZE)
        pygame.draw.rect(self.screen, BLACK, rect, 1)
        text_surface = self.font.render(str(col + 1 + inc * MAX_BOX_WIDTH), True, PURPLE)
        text_rect = text_surface.get_rect()
        text_rect.center = box.get_rect().center
        box.blit(text_surface, text_rect)
        self.screen.blit(box, rect)

    def draw_boxes(self):
        if self.num_of_boxes <= MAX_BOX_WIDTH:
            for box in range(0, self.num_of_boxes, BOX_SIZE):
                self.draw_box(box, 0)
        else:
            rows = int(math.floor(self.num_of_boxes / MAX_BOX_WIDTH))
            remainder = self.num_of_boxes - rows * MAX_BOX_WIDTH
            for row in range(rows):
                for box in range(MAX_BOX_WIDTH):
                    self.draw_box(box, row)
            for rem in range(remainder):
                self.draw_box(rem, rows)
        pygame.display.update()
