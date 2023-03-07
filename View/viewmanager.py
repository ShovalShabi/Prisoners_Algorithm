import math
from pygame import KEYDOWN, K_BACKSPACE
import sys
from box_view import *
from prisoner_view import *


class ViewManager:
    def __init__(self):
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
        self.image_background = IMG_BACKGROUND
        self.background_image = pygame.transform.scale(self.image_background, (screen_width, screen_height))
        self.text_input_n = ""
        self.text_input_k = ""
        self.status = 'Prisoner'
        self.p_color = RED
        self.r_color = BLACK
        self.num_of_rounds = 0
        self.actual_num_of_boxes = 0
        self.start_rect = pygame.Rect(50, 800, button_width, button_height)
        self.start_hover_rect = pygame.Rect(50, 800, button_width, button_height)
        self.text_surface_start = self.font.render("START", True, BLACK)
        self.reset_rect = pygame.Rect(200, 800, button_width, button_height)
        self.reset_hover_rect = pygame.Rect(200, 800, button_width, button_height)
        self.text_surface_reset = self.font.render("RESET", True, BLACK)
        self.prisoner = None
        self.boxes = {}
        self.listener = None

    #  listener
    def replace_prisoner(self, prisoner_num):
        self.create_prisoner(prisoner_num)

    def send_boxes_locations(self):
        self.listener.send_boxes_locationV(self.boxes)

    def send_box_dimension(self):
        self.listener.send_box_dimension(IMG_BOX_WIDTH, IMG_BOX_HEIGHT)

    def set_listener(self, listener):
        self.listener = listener

    def update_prisoner_location(self, location):
        self.prisoner.update_prisoner_location(location)

    def draw_prisoner(self):
        self.prisoner.draw_prisoner()

    # # # # # # #

    def run(self):
        # self.send_box_dimension()
        while self.running:
            # draw board
            self.start_events()
            self.start_draw()
            self.button_events()

            # start pressed
            if self.state == 'begin':
                self.create_boxes()  # create boxes with number and locations
                # self.create_prisoner(5)  # ????
                #
                # # send boxes location via listener to model
                # # self.send_boxes_locations()
                #
                # # move
                # self.draw_prisoner()

            pygame.display.update()
        pygame.quit()
        sys.exit()

    def button_events(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        self.draw_button(mouse_click, mouse_pos, self.start_rect, self.start_hover_rect, self.text_surface_start, GREEN)
        self.draw_button(mouse_click, mouse_pos, self.reset_rect, self.reset_hover_rect, self.text_surface_reset, RED)

    def draw_button(self, mouse_click, mouse_pos, rect, hover, text_surface, color):
        # Check if the mouse is over the button
        if rect.collidepoint(mouse_pos):
            # Draw the hover state
            pygame.draw.rect(self.screen, color, hover)
            if mouse_click[0] == 1:
                self.state = 'begin'
                print("Button clicked!")
        else:
            # Draw the normal state
            pygame.draw.rect(self.screen, WHITE, rect)
        self.screen.blit(text_surface, (rect.x + 23, rect.y + 17))

    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == KEYDOWN and self.state != 'begin':
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
                    self.convert_input_round_to_num()
                if self.status == 'Prisoner':  # prisoner
                    self.text_input_n = self.handle_input(event, self.text_input_n)
                    self.convert_input_prisoner_to_num()

    def start_draw(self):
        self.screen.blit(self.background_image, (0, 0))
        self.draw_menu()
        self.draw_boxes()
        # self.draw_prisoners()

    def draw_menu(self):
        # Draw the input text
        self.draw_label(self.p_color, 350, 800, 'Number of prisoners:')
        self.draw_label(RED, 350, 820, self.text_input_n)
        self.draw_label(self.r_color, 600, 800, 'Number of rounds:')
        self.draw_label(RED, 600, 820, self.text_input_k)

    def draw_label(self, color, x, y, text):
        text_surface = self.font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))

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

    def convert_input_round_to_num(self):
        if self.text_input_k != "" and str.isdigit(self.text_input_k):
            num = int(str(self.text_input_k))
            if num <= MAX_NO_ROUND:
                self.num_of_rounds = num
            else:
                self.num_of_rounds = MAX_NO_ROUND
            self.num_of_rounds = num
        else:
            self.text_input_k = ""
            self.num_of_rounds = 0

    def convert_input_prisoner_to_num(self):

        if self.text_input_n != "" and str.isdigit(self.text_input_n):
            num = int(str(self.text_input_n))
            if num <= MAX_NO_PRISONER_BOX:
                self.num_of_boxes_view = num
            else:
                self.num_of_boxes_view = MAX_NO_PRISONER_BOX
            self.actual_num_of_boxes = num
            self.num_of_prisoners = num
        else:
            self.text_input_n = ""
            self.num_of_boxes_view = 0
            self.num_of_prisoners = 0

    def handle_input(self, event_input, text):
        if event_input.key == K_BACKSPACE:
            if len(text) > 0:
                text = text[:-1]
        else:
            text += event_input.unicode
        return text

    def create_boxes(self):
        if self.num_of_boxes_view <= MAX_BOX_WIDTH:
            for box_index in range(self.num_of_boxes_view):
                box = BoxV(self.screen, box_index + 1)
                self.boxes[box.num] = self.get_box_location(box.num, 0)
        else:
            rows = int(math.floor(self.num_of_boxes_view / MAX_BOX_WIDTH))
            remainder = self.num_of_boxes_view - rows * MAX_BOX_WIDTH
            for row in range(rows):
                for box_index in range(MAX_BOX_WIDTH):
                    box = BoxV(self.screen, box_index + 1 + row * MAX_BOX_WIDTH)
                    self.boxes[box.num] = self.get_box_location(box.num, row)
            for rem in range(remainder):
                box = BoxV(self.screen, rows * MAX_BOX_WIDTH + rem + 1)
                self.boxes[box.num] = self.get_box_location(box.num, rows)

    def get_box_location(self, box_index, inc):
        x = 150 + box_index * CELL_SIZE
        y = 80 + inc * CELL_SIZE
        return x, y

    def create_prisoner(self, num_prisoner):
        self.prisoner = PrisonerV(DOOR_WAY, num_prisoner, self.screen)
