import math
from pygame import KEYDOWN, K_BACKSPACE
from settings import *
import sys
import pygame


class App:
    def __init__(self) -> None:
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.SysFont('monospace', FONT_SIZE)
        self.clock = pygame.time.Clock()
        self.state = 'start'
        self.running = True
        self.num_of_boxes = MAX_NO_BOX
        self.num_of_prisoners = 1
        self.size = (screen_width, screen_height)
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Prisoners")
        self.colors = SETTINGS.get('COLORS')
        self.text_input = ""

    def run(self):
        while self.running:
            if self.state == 'start':
                self.start_events()
                self.start_draw()
            pygame.display.update()
        pygame.quit()
        sys.exit()

    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == KEYDOWN:
                if event.key == K_BACKSPACE:
                    if len(self.text_input) > 0:
                        self.text_input = self.text_input[:-1]
                else:
                    self.text_input += event.unicode

    def start_draw(self):
        self.screen.fill(self.colors.get('BLACK'))
        self.draw_boxes()
        self.draw_menu()
        # self.draw_prisoners()

    def draw_menu(self):
        # Draw the screen
        self.draw_button(self.colors.get('GREEN'), 50, 800, button_width, button_height, "Start")
        self.draw_button(self.colors.get('RED'), 200, 800, button_width, button_height, "Reset")
        self.draw_label(self.colors.get('WHITE'), 350, 800, 'Enter number of boxes:')
        self.draw_label(self.colors.get('WHITE'), 400, 820, self.text_input)

    def draw_label(self, color, x, y, text):
        text_surface = self.font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))

    def draw_button(self, color, x, y, width, height, text):
        pygame.draw.rect(self.screen, color, (x, y, width, height))
        text_surface = self.font.render(text, True, self.colors.get('BLACK'))
        text_rect = text_surface.get_rect()
        text_rect.center = ((x + width // 2), (y + height // 2))
        self.screen.blit(text_surface, text_rect)

    def draw_prisoners(self):
        pass

    def draw_box(self, col, inc):
        box = pygame.image.load("Resources/chest_closed.png")
        rect = pygame.Rect(CELL_SIZE + col * CELL_SIZE, CELL_SIZE + inc * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(self.screen, self.colors.get('RED'), rect, 1)
        text_surface = self.font.render(str(col + 1 + inc * MAX_BOX_WIDTH), True, self.colors.get('YELLOW'))
        text_rect = text_surface.get_rect()
        text_rect.center = box.get_rect().center
        box.blit(text_surface, text_rect)
        self.screen.blit(box, rect)

    def draw_boxes(self):
        if self.num_of_boxes <= MAX_BOX_WIDTH:
            for box in range(0, self.num_of_boxes, CELL_SIZE):
                self.draw_box(box, 0)
        else:
            rows = int(math.floor(self.num_of_boxes / MAX_BOX_WIDTH))
            remainder = self.num_of_boxes - rows * MAX_BOX_WIDTH
            for row in range(rows):
                for box in range(MAX_BOX_WIDTH):
                    self.draw_box(box, row)
            for rem in range(remainder):
                self.draw_box(rem, rows)
