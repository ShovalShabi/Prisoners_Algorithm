import math
import sys
from typing import Tuple

import pygame
from pygame.locals import KEYDOWN, K_BACKSPACE
from screen_operator import ScreenOperator
from Prisoners_Algorithm.View.prisoner_view import PrisonerV
from Prisoners_Algorithm.View.settings import *
from box_view import BoxV
import warnings


def suppress_warnings(func):
    def wrapper(*args, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            return func(*args, **kwargs)

    return wrapper


class ViewManager:

    def __init__(self) -> None:
        """
        Initialize the ViewManager Object and initializing various game variables.
        """
        # Game state
        self.state = 'start'
        self.running = True

        # Variables
        self.num_of_boxes_view = 0
        self.num_of_prisoners = 0
        self.status = 'Prisoner'
        self.num_of_rounds = 0
        self.actual_num_of_boxes = 0

        # Objects
        self.prisoner = None
        self.boxes = {}
        self.listener = None

        # Screen Operations
        self.screen_operator = ScreenOperator()

    @suppress_warnings
    def pygame_initialize(self):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("Prisoners")

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

    # Game functions
    def run(self) -> None:
        """
        Main loop of the game. Runs until self.running is False.
        """
        # Initialize the game
        self.pygame_initialize()
        while self.running:

            # Create and draw the boxes, handle events, and update the button states
            self.create_boxes()
            self.screen_operator.start_draw(self.boxes)
            self.start_events()
            self.button_events()

            # Handle the 'begin' state
            if self.state == 'begin':
                self.create_boxes()

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
        self.state = self.screen_operator.draw_button(mouse_click, mouse_pos, self.screen_operator.start_rect,
                                                      self.screen_operator.start_hover_rect,
                                                      self.screen_operator.text_surface_start, GREEN, self.state)
        self.state = self.screen_operator.draw_button(mouse_click, mouse_pos, self.screen_operator.reset_rect,
                                                      self.screen_operator.reset_hover_rect,
                                                      self.screen_operator.text_surface_reset, RED, self.state)

    def start_events(self) -> None:
        """
        Function that handles the events that happen in the game.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == KEYDOWN and self.state != 'begin':
                self.decide_input_type(event)

                if self.status == 'Round':  # rounds
                    self.screen_operator.text_input_k = self.handle_input(event, self.screen_operator.text_input_k)
                    self.convert_input_round_to_num()
                if self.status == 'Prisoner':  # prisoner
                    self.screen_operator.text_input_n = self.handle_input(event, self.screen_operator.text_input_n)
                    self.convert_input_prisoner_to_num()

    def decide_input_type(self, event):
        if event.key == pygame.K_LEFT:
            self.status = 'Prisoner'
            self.screen_operator.p_color = RED
            self.screen_operator.r_color = BLACK
        if event.key == pygame.K_RIGHT:
            self.status = 'Round'
            self.screen_operator.p_color = BLACK
            self.screen_operator.r_color = RED

    def convert_input_round_to_num(self) -> None:
        """
        Converts the text input for the number of rounds to an integer.
        """
        if self.screen_operator.text_input_k != "" and str.isdigit(self.screen_operator.text_input_k):
            num = int(self.screen_operator.text_input_k)
            if num <= MAX_NO_ROUND:
                self.num_of_rounds = num
            else:
                self.num_of_rounds = MAX_NO_ROUND
        else:
            self.screen_operator.text_input_k = ""
            self.num_of_rounds = 0

    def convert_input_prisoner_to_num(self) -> None:
        """
        Converts the text input for the number of prisoners to an integer.
        """
        if self.screen_operator.text_input_n != "" and str.isdigit(self.screen_operator.text_input_n):
            num = int(self.screen_operator.text_input_n)
            if num <= MAX_NO_PRISONER_BOX:
                self.num_of_boxes_view = num
            else:
                self.num_of_boxes_view = MAX_NO_PRISONER_BOX
            self.actual_num_of_boxes = num
            self.num_of_prisoners = num
        else:
            self.screen_operator.text_input_n = ""
            self.num_of_boxes_view = 0
            self.num_of_prisoners = 0

    @suppress_warnings
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
        self.boxes.clear()
        if self.num_of_boxes_view <= MAX_BOX_WIDTH:
            for box_index in range(self.num_of_boxes_view):
                box = BoxV(self.screen_operator.screen, box_index + 1)
                self.boxes[box.box_number] = self.get_box_location(box.box_number, 0)
        else:
            rows = int(math.floor(self.num_of_boxes_view / MAX_BOX_WIDTH))
            remainder = self.num_of_boxes_view - rows * MAX_BOX_WIDTH
            for row in range(rows):
                for box_index in range(MAX_BOX_WIDTH):
                    box = BoxV(self.screen_operator.screen, box_index + 1 + row * MAX_BOX_WIDTH)
                    self.boxes[box.box_number] = self.get_box_location(box.box_number, row)
            for rem in range(remainder):
                box = BoxV(self.screen_operator.screen, rows * MAX_BOX_WIDTH + rem + 1)
                self.boxes[box.box_number] = self.get_box_location(box.box_number, rows)

    @suppress_warnings
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
        self.prisoner = PrisonerV(DOOR_WAY, num_prisoner, self.screen_operator.screen)
