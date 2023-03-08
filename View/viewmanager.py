import math
from typing import Tuple

from pygame.locals import KEYDOWN, K_BACKSPACE
import sys
from box_view import *
from prisoner_view import *


class ViewManager:
    def __init__(self) -> None:
        """
        Initialize the game by setting up Pygame and initializing various game variables.
        """
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("Prisoners")

        # Font
        self.font = pygame.font.SysFont('monospace', FONT_SIZE, bold=True)

        # Game state
        self.state = 'start'
        self.running = True

        # Variables
        self.num_of_boxes_view = 0
        self.num_of_prisoners = 0
        self.status = 'Prisoner'
        self.p_color = RED
        self.r_color = BLACK
        self.num_of_rounds = 0
        self.actual_num_of_boxes = 0
        self.text_input_n = ""
        self.text_input_k = ""

        # Screen and background
        self.size = (screen_width, screen_height)
        self.screen = pygame.display.set_mode(self.size)
        self.image_background = IMG_BACKGROUND
        self.background_image = pygame.transform.scale(self.image_background, (screen_width, screen_height))

        # Buttons
        self.start_rect = pygame.Rect(50, 800, button_width, button_height)
        self.start_hover_rect = pygame.Rect(50, 800, button_width, button_height)
        self.text_surface_start = self.font.render("START", True, BLACK)
        self.reset_rect = pygame.Rect(200, 800, button_width, button_height)
        self.reset_hover_rect = pygame.Rect(200, 800, button_width, button_height)
        self.text_surface_reset = self.font.render("RESET", True, BLACK)

        # Objects
        self.prisoner = None
        self.boxes = {}
        self.listener = None

    #  Listener functions
    def replace_prisoner(self, prisoner_num: int) -> None:
        """
        Replaces the current prisoner with a new one.

        :param prisoner_num: An integer representing the number of the new prisoner.
        """
        self.create_prisoner(prisoner_num)

    def send_boxes_locations(self) -> None:
        """
        Sends the current locations of all the boxes to the listener.
        """
        self.listener.send_boxes_locationV(self.boxes)

    def send_box_dimension(self) -> None:
        """
        Sends the dimensions of the box image to the listener.
        """
        self.listener.send_box_dimension(IMG_BOX_WIDTH, IMG_BOX_HEIGHT)

    def set_listener(self, listener) -> None:
        """
        Sets the listener for this game.

        :param listener: The listener object to be set.
        """
        self.listener = listener

    def update_prisoner_location(self, location: Tuple[int, int]) -> None:
        """
        Updates the location of the prisoner.

        :param location: The new location of the prisoner as a tuple of integers (x, y).
        """
        self.prisoner.update_prisoner_location(location)

    def draw_prisoner(self) -> None:
        """
        Draws the prisoner on the screen.
        """
        self.prisoner.draw_prisoner()

    # Game functions
    def run(self) -> None:
        """
        Main loop of the game. Runs until self.running is False.
        """
        while self.running:
            # Draw the board, handle events, and update the button states
            self.start_draw()
            self.start_events()
            self.button_events()

            # Handle the 'begin' state
            if self.state == 'begin':
                self.create_boxes()
                # self.draw_prisoner()
                # self.send_boxes_locations()

            # Update the display
            pygame.display.update()

        # Quit the game
        pygame.quit()
        sys.exit()

    def button_events(self) -> None:
        """
        Handle button events.
        """
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        self.draw_button(mouse_click, mouse_pos, self.start_rect, self.start_hover_rect, self.text_surface_start, GREEN)
        self.draw_button(mouse_click, mouse_pos, self.reset_rect, self.reset_hover_rect, self.text_surface_reset, RED)

    def draw_button(self, mouse_click: Tuple[int, int, int], mouse_pos: Tuple[int, int],
                    rect: pygame.Rect, hover: pygame.Rect, text_surface: pygame.Surface,
                    color: Tuple[int, int, int]) -> None:
        """
        Draw a button and handle mouse hover and click events.

        :param mouse_click: A tuple representing the state of the mouse buttons.
        :param mouse_pos: A tuple representing the position of the mouse cursor.
        :param rect: A pygame.Rect object representing the dimensions of the button.
        :param hover: A pygame.Rect object representing the dimensions of the hover rect of the button.
        :param text_surface: A pygame.Surface object representing the text to be displayed on the button.
        :param color: A tuple representing the color of the button.
        """
        if rect.collidepoint(mouse_pos):
            # Draw the hover rect if the mouse is over the button
            pygame.draw.rect(self.screen, color, hover)
            if mouse_click[0] == 1:
                self.state = 'begin'
                print("Button clicked!")
        else:
            # Draw the normal state if the mouse is not over the button
            pygame.draw.rect(self.screen, WHITE, rect)

        # Draw the text surface in the center of the button
        self.screen.blit(text_surface, (rect.x + rect.width // 2 - text_surface.get_width() // 2,
                                        rect.y + rect.height // 2 - text_surface.get_height() // 2))

    def start_events(self) -> None:
        """
        Function that handles the events that happen in the game.
        """
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

    def start_draw(self) -> None:
        """
        Function that draws the game elements on the screen.
        """
        self.screen.blit(self.background_image, (0, 0))
        self.draw_menu()
        self.draw_boxes()
        # self.draw_prisoners()

    def draw_menu(self) -> None:
        """
        Draws the menu on the screen.
        """
        # Draw the input text
        self.draw_label(self.p_color, 350, 800, 'Number of prisoners:')
        self.draw_label(RED, 350, 820, self.text_input_n)
        self.draw_label(self.r_color, 600, 800, 'Number of rounds:')
        self.draw_label(RED, 600, 820, self.text_input_k)

    def draw_label(self, color: Tuple[int, int, int], pos_x: int, pos_y: int, text: str = "") -> None:
        """
        Draws a label on the screen.

        :param color: The color of the label as an RGB tuple.
        :param pos_x: The x position of the top-left corner of the label.
        :param pos_y: The y position of the top-left corner of the label.
        :param text: The text to be displayed in the label. Defaults to an empty string.
        """
        text_surface = self.font.render(text, True, color)
        self.screen.blit(text_surface, (pos_x, pos_y))

    def draw_boxes(self) -> None:
        """
        Draws the boxes on the screen.
        """
        boxes = [BoxV(self.screen, box_index + 1) for box_index in range(self.num_of_boxes_view)]

        if self.num_of_boxes_view <= MAX_BOX_WIDTH:
            for box_index, box in enumerate(boxes):
                box.location = box.draw_box(box_index, 0, self.font)
        else:
            rows = self.num_of_boxes_view // MAX_BOX_WIDTH
            remainder = self.num_of_boxes_view % MAX_BOX_WIDTH

            for row in range(rows):
                for box_index in range(MAX_BOX_WIDTH):
                    box = boxes[row * MAX_BOX_WIDTH + box_index]
                    box.location = box.draw_box(box_index, row, self.font)

            for rem in range(remainder):
                box = boxes[rows * MAX_BOX_WIDTH + rem]
                box.location = box.draw_box(rem, rows, self.font)

    def convert_input_round_to_num(self) -> None:
        """
        Converts the text input for the number of rounds to an integer.
        """
        if self.text_input_k != "" and str.isdigit(self.text_input_k):
            num = int(self.text_input_k)
            if num <= MAX_NO_ROUND:
                self.num_of_rounds = num
            else:
                self.num_of_rounds = MAX_NO_ROUND
        else:
            self.text_input_k = ""
            self.num_of_rounds = 0

    def convert_input_prisoner_to_num(self) -> None:
        """
        Converts the text input for the number of prisoners to an integer.
        """
        if self.text_input_n != "" and str.isdigit(self.text_input_n):
            num = int(self.text_input_n)
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

    def handle_input(self, event_input: pygame.event, text: str = "") -> str:
        """
        Updates the text based on the given input event.

        :param event_input: The input event to handle.
        :param text: The current text.
        :return: The updated text.
        """
        if event_input.key == K_BACKSPACE:
            if len(text) > 0:
                text = text[:-1]
        else:
            text += event_input.unicode
        return text

    def create_boxes(self) -> None:
        """
        Creates box objects and adds their locations to the self.boxes dictionary.
        """
        if self.num_of_boxes_view <= MAX_BOX_WIDTH:
            for box_index in range(self.num_of_boxes_view):
                box = BoxV(self.screen, box_index + 1)
                self.boxes[box.box_number] = self.get_box_location(box.box_number, 0)
        else:
            rows = int(math.floor(self.num_of_boxes_view / MAX_BOX_WIDTH))
            remainder = self.num_of_boxes_view - rows * MAX_BOX_WIDTH
            for row in range(rows):
                for box_index in range(MAX_BOX_WIDTH):
                    box = BoxV(self.screen, box_index + 1 + row * MAX_BOX_WIDTH)
                    self.boxes[box.box_number] = self.get_box_location(box.box_number, row)
            for rem in range(remainder):
                box = BoxV(self.screen, rows * MAX_BOX_WIDTH + rem + 1)
                self.boxes[box.box_number] = self.get_box_location(box.box_number, rows)

    def get_box_location(self, box_index: int, inc: int) -> tuple:
        """
        This method calculates the coordinates of a box given its index and the amount to increment.

        :param box_index: An integer representing the index of the box.
        :param inc: An integer representing the amount to increment.
        :return: A tuple containing the x and y coordinates of the box.
        """
        x = BOX_START_X + box_index * CELL_SIZE
        y = BOX_START_Y + inc * CELL_SIZE
        return x, y

    def create_prisoner(self, num_prisoner: int) -> None:
        """
        This method creates a new PrisonerV object and assigns it to the instance variable `self.prisoner`.

        :param num_prisoner: An integer representing the number of the prisoner.
        """
        self.prisoner = PrisonerV(DOOR_WAY, num_prisoner, self.screen)
