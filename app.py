import math
from pygame import KEYDOWN, K_BACKSPACE
import sys
from settings import BLACK
from box_view import *


class App:
    def __init__(self) -> None:
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("Prisoners")
        self.font = pygame.font.SysFont('monospace', FONT_SIZE, bold=True)
        self.clock = pygame.time.Clock()
        self.state = 'start'
        self.running = True
        self.num_of_boxes_view = 0
        self.num_of_prisoners = 0
        self.size = (screen_width, screen_height)
        self.screen = pygame.display.set_mode(self.size)
        self.image = pygame.image.load(IMG_BACKGROUND)
        self.background_image = pygame.transform.scale(self.image, (screen_width, screen_height))
        self.text_input_n = ""
        self.text_input_k = ""
        self.status = 'Prisoner'
        self.p_color = RED
        self.r_color = BLACK
        self.boxes = {}
        self.actual_num_of_boxes = 0

    def run(self):
        while self.running:
            if self.state == 'start':
                self.start_events()
                self.start_draw()
            elif self.state == 'begin':
                self.create_boxes()  # create boxes with number and locations
            pygame.display.update()
        pygame.quit()
        sys.exit()

    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.status = 'Prisoner'
                    self.p_color = RED
                    self.r_color = BLACK
                if event.key == pygame.K_RIGHT:
                    self.status = 'Round'
                    self.p_color = BLACK
                    self.r_color = RED

                if self.status == 'Round':  # rounds
                    self.text_input_k = self.handle_input(event, self.text_input_k)
                if self.status == 'Prisoner':  # prisoner
                    self.text_input_n = self.handle_input(event, self.text_input_n)
                    self.convert_input_to_num_of_box()

    def start_draw(self):
        self.screen.blit(self.background_image, (0, 0))
        self.draw_menu()
        self.draw_boxes()
        print(len(self.boxes))

        # self.draw_prisoners()

    def draw_menu(self):
        # Draw the screen
        self.draw_button(GREEN, 50, 800, button_width, button_height, "Start")
        self.draw_button(RED, 200, 800, button_width, button_height, "Reset")
        self.draw_label(self.p_color, 350, 800, 'Number of prisoners:')
        self.draw_label(RED, 350, 820, self.text_input_n)
        self.draw_label(self.r_color, 600, 800, 'Number of rounds:')
        self.draw_label(RED, 600, 820, self.text_input_k)

    def draw_label(self, color, x, y, text):
        text_surface = self.font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))

    def draw_button(self, color, x, y, width, height, text):
        pygame.draw.rect(self.screen, color, (x, y, width, height))
        text_surface = self.font.render(text, True, BLACK)
        text_rect = text_surface.get_rect()
        text_rect.center = ((x + width // 2), (y + height // 2))
        self.screen.blit(text_surface, text_rect)

    def draw_boxes(self):

        if self.num_of_boxes_view <= MAX_BOX_WIDTH:
            for box_index in range(self.num_of_boxes_view):
                box = BoxV(self.screen, box_index + 1)
                box.location = box.draw_box(box_index, 0, self.font)

        else:

            rows = int(math.floor(self.num_of_boxes_view / MAX_BOX_WIDTH))
            remainder = self.num_of_boxes_view - rows * MAX_BOX_WIDTH
            for row in range(rows):
                for box_index in range(MAX_BOX_WIDTH):
                    box = BoxV(self.screen, box_index + 1)
                    box.location = box.draw_box(box_index, row, self.font)

            for rem in range(remainder):
                box = BoxV(self.screen, rem + 1)
                box.location = box.draw_box(rem, rows, self.font)

    def convert_input_to_num_of_box(self):
        if self.text_input_n != "":
            num = int(str(self.text_input_n))
            if num <= MAX_NO_PRISONER_BOX:
                self.num_of_boxes_view = num
            else:
                self.num_of_boxes_view = MAX_NO_PRISONER_BOX
            self.actual_num_of_boxes = num
        else:
            self.num_of_boxes_view = 0

    def handle_input(self, event_input, text):
        if event_input.key == K_BACKSPACE:
            if len(text) > 0:
                text = text[:-1]
        else:
            text += event_input.unicode
        return text

    def create_boxes(self):
        pass
