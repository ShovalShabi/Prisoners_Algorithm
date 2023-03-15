import math
import sys
import warnings

import pygame.time
from pygame.event import Event
from pygame.locals import KEYDOWN, K_BACKSPACE, K_SPACE

from View.screen_operator import ScreenOperator
from View.prisoner_view import PrisonerV
from View.settings import *
from View.box_view import BoxV
from pygame.time import Clock


def suppress_warnings(func):
    def wrapper(*args, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            return func(*args, **kwargs)

    return wrapper


class ViewManager:
    """
    A class representing the managing object that is trusted of the frontend part of the game.\n
    The class main concern is to handle the requests that comes from the user and according to that the object
   responds relatively.\n

    Attributes:\n

    state: the state of the game for the current particular time -> str object.\n
    running: boolean parameter -> bool.\n
    num_of_boxes_view: the number of boxes that view represents -> int.\n
    num_of_prisoners: the number of prisoners -> int.\n
    status: the status of the view -> str object.\n
    num_of_rounds: the number of rounds -> int.\n
    actual_num_of_boxes: the number of boxes that view handle,can be more than the screen can represent -> int.\n
    prisoner: the prisoner that is currently searching for his number -> PrisonerV object.\n
    listener: coordinates the activity between the backend and the frontend -> Controller object.\n
    boxes_on_screen_obj: dictionary of BoxV objects that are currently on screen mapped by their number -> dict of {int:BoxV object}.\n
    boxes_on_screen_pos: dictionary of tuple of position of each BoxV object, mapped by their number -> dict of {int: tuple (x,y)}.\n
    boxes_off_screen_obj: dictionary of BoxV objects that are not currently on screen mapped by their number -> dict of {int:BoxV object}.\n
    screen_operator: object that organizes the drawing of the objects on screen, fonts and buttons -> ScreenOpreator object.\n
    clock: clock the keeps the frame rate reasonable -> Clock object.\n
    """

    def __init__(self) -> None:
        """
        Initialize the ViewManager Object and initializing various game variables.
        """
        # Game state
        self.state = 'not running'
        self.running = True

        # Variables
        self.num_of_boxes_view = 0
        self.num_of_prisoners = 0
        self.status = 'Prisoner'
        self.num_of_rounds = 0
        self.actual_num_of_boxes = 0
        self.print_specify = False

        # Objects
        self.prisoner = None
        self.listener = None
        self.boxes_on_screen_obj = {}
        self.boxes_on_screen_pos = {}
        self.boxes_off_screen_obj = {}

        # Screen Operations
        self.screen_operator = None
        self.clock = Clock()

    @suppress_warnings
    def pygame_setup(self) -> None:
        """
        Method that deals with setup all the configuration of pygame.\n
        :return: None
        """
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("Prisoners Riddle")
        self.screen_operator = ScreenOperator()

    #################################################Listener methods##########################################
    def view_request_to_start_game(self, num_of_prisoners: int, num_of_rounds: int, initial_pos: tuple[int, int],
                                   print_specifically: bool) -> None:
        """
        Method that send the data to model object.

        :param print_specifically: indication for amount of the specification in PrisonersResults.txt -> bool.
        :param initial_pos: tuple of position on screen -> tuple (x,y).
        :param num_of_rounds: The numbers of input rounds -> int.
        :param num_of_prisoners: The numbers of input prisoners -> int.
        :return: None.
        """
        self.listener.view_need_to_init_game(num_of_prisoners, num_of_rounds, initial_pos, print_specifically)

    def view_request_pris_num(self) -> int:
        """
        Method that requests from the model the current prisoner number.\n

        :return: the number of prisoner -> int.
        """
        return self.listener.view_need_pris_num()

    def view_request_pris_pos(self) -> tuple[int, int]:
        """
        Method that requests from the model the current prisoner position.\n

        :return: the position of prisoner -> tuple (x,y).
        """
        return self.listener.view_need_pris_pos()

    def view_request_run_game(self) -> None:
        """
        Method that requests from the model to start the game.\n

        :return: None.
        """
        self.listener.view_need_to_run_game()

    def set_listener(self, listener) -> None:
        """
        Sets the listener for the ViewManager object.\n

        :param listener: The listener object to be set -> Controller object.
        :return: None.
        """
        self.listener = listener

    ########################################################################################################

    # Game functions
    def run(self) -> None:
        """
        Main loop of the game. Runs until self.running is False.\n
        :returns: None.
        """
        # Initialize the game
        self.pygame_setup()
        while self.running:
            self.screen_operator.draw_screen()
            self.screen_operator.draw_boxes(self.boxes_on_screen_pos)
            self.listen_to_events()
            self.button_events()

            if self.state == 'reset':
                self.reset_input_view()

            if self.state == 'not running':
                # Create and draw the boxes, handle events, and update the button states
                # self.create_boxes()
                self.create_boxes_test()

            # Occurs when start button is clicked
            if self.state == 'begin':
                self.listener.view_need_to_init_game(self.num_of_prisoners, self.num_of_rounds, DOOR_WAY,
                                                     self.print_specify)
                pris_num = self.view_request_pris_num()
                self.prisoner = PrisonerV(start_pos=DOOR_WAY, num=pris_num, screen=self.screen_operator.screen)
                self.state = "running"

            if self.state == "running":
                self.view_request_run_game()
                pris_num = self.view_request_pris_num()
                if pris_num <= self.num_of_prisoners:
                    if pris_num != self.prisoner.pris_num:
                        self.prisoner = PrisonerV(start_pos=DOOR_WAY, num=pris_num,
                                                  screen=self.screen_operator.screen)
                    else:
                        pos = self.view_request_pris_pos()
                        self.prisoner.set_pris_pos(pos=pos)
                    self.screen_operator.draw_objects(self.boxes_on_screen_pos, self.prisoner)
                else:
                    self.view_request_run_game()
                    self.state = 'reset'
                self.clock.tick(25)

            # Update the display
            pygame.display.update()

        # Quit the game
        pygame.quit()
        sys.exit()

    def reset_input_view(self) -> None:
        """
        Method that resets all the view controls and screen.\n
        :return: None.
        """
        # Variables
        self.num_of_boxes_view = 0
        self.num_of_prisoners = 0
        self.status = 'Prisoner'
        self.num_of_rounds = 0
        self.actual_num_of_boxes = 0

        # Objects
        self.boxes_on_screen_pos = {}
        self.boxes_off_screen_obj = {}

        # Screen
        self.screen_operator.text_input_n = ""
        self.screen_operator.text_input_k = ""

        self.state = 'not running'

    def button_events(self) -> None:
        """
        Method that handles with button events.\n
        :return: None.
        """
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        self.screen_operator.draw_check_box(self.print_specify)
        self.state = self.screen_operator.draw_button(mouse_click, mouse_pos, self.screen_operator.start_rect,
                                                      self.screen_operator.start_hover_rect,
                                                      self.screen_operator.text_surface_start,
                                                      GREEN, self.state, 'start_button')
        self.state = self.screen_operator.draw_button(mouse_click, mouse_pos, self.screen_operator.reset_rect,
                                                      self.screen_operator.reset_hover_rect,
                                                      self.screen_operator.text_surface_reset,
                                                      RED, self.state, 'reset_button')

    def listen_to_events(self) -> None:
        """
        Method that handles the events that happen in the game.\n
        :return: None.
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
                if self.status == 'Specify':
                    if event.key == pygame.K_SPACE:
                        self.print_specify = not self.print_specify


    def decide_input_type(self, event: Event) -> None:
        """
        Method that decide on the input type.\n
        :param event: event that triggered by the user -> Event object.
        :return: None.
        """
        if event.key == pygame.K_LEFT:
            self.status = 'Prisoner'
            self.screen_operator.p_color = RED
            self.screen_operator.r_color = BLACK
            self.screen_operator.s_color = BLACK
        if event.key == pygame.K_DOWN:
            self.status = 'Round'
            self.screen_operator.p_color = BLACK
            self.screen_operator.r_color = RED
            self.screen_operator.s_color = BLACK
        if event.key == pygame.K_RIGHT:
            self.status = 'Specify'
            self.screen_operator.p_color = BLACK
            self.screen_operator.r_color = BLACK
            self.screen_operator.s_color = RED

    def convert_input_round_to_num(self) -> None:
        """
        Method that converts the text input for the number of rounds to an integer.\n
        :return: None.
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

    def update_prisoner_location(self, pos: tuple[int, int]) -> None:
        """
        Updates the location of the prisoner.\n

        :param pos: The new location of the prisoner as a tuple of integers (x, y).
        :return: None.
        """
        self.prisoner.set_pris_pos(pos)

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
    def handle_input(self, event_input: Event, text: str = "") -> str:
        """
        method that updates the text based on the given input event.\n

        :param event_input: the input event to handle -> Event object.
        :param text: the current text -> str object.
        :return: the updated text -> str object.
        """
        if event_input.key == K_BACKSPACE:
            if len(text) > 0:
                text = text[:-1]
        else:
            text += event_input.unicode
        return text

    def create_boxes_test(self) -> None:
        """
        Method that creates boxes on screen and determines which boxes are on screen in case of overflow and also in charge of
        the position of each box.\n
        :return: None
        """
        self.boxes_on_screen_pos.clear()
        self.boxes_off_screen_obj.clear()
        rows = int(math.floor(self.num_of_boxes_view / MAX_BOX_WIDTH))
        remainder = self.num_of_boxes_view - rows * MAX_BOX_WIDTH
        for row in range(rows):
            for col in range(MAX_BOX_WIDTH):
                box = BoxV(screen=self.screen_operator.screen, box_num=row * MAX_BOX_WIDTH + col + 1)
                box.set_pos(new_pos=(BOX_START_X + col * CELL_SIZE, BOX_START_Y + row * CELL_SIZE))
                self.boxes_on_screen_obj[box.box_num] = box  # Mappinhg objects of BoxV by their number
                self.boxes_on_screen_pos[
                    box.box_num] = box.get_pos()  # Mapping positions of BoxV objects by their number
        for rem in range(remainder):
            box = BoxV(screen=self.screen_operator, box_num=rows * MAX_BOX_WIDTH + rem + 1)
            box.set_pos(new_pos=(BOX_START_X + rem * CELL_SIZE, BOX_START_Y + rows * CELL_SIZE))
            self.boxes_on_screen_pos[box.box_num] = box.get_pos()

        if self.actual_num_of_boxes - MAX_NO_PRISONER_BOX > 0:
            for box_index in range(MAX_NO_PRISONER_BOX + 1, self.actual_num_of_boxes + 1):
                box = BoxV(screen=self.screen_operator.screen, box_num=box_index)
                self.boxes_off_screen_obj[box.box_num] = box

    def create_prisoner(self, num_prisoner: int) -> None:
        """
        Method that creates a new PrisonerV object and assigns it to the instance variable `self.prisoner`.\n

        :param num_prisoner: An integer representing the number of the prisoner.
        :return: None.
        """
        self.prisoner = PrisonerV(DOOR_WAY, num_prisoner, self.screen_operator.screen)

    def replace_prisoner(self, prisoner_num: int) -> None:
        """
        Method that replaces the current prisoner with a new one.\n

        :param prisoner_num: An integer representing the number of the new prisoner.
        :return: None.
        """
        self.create_prisoner(prisoner_num)

    def handle_box_request(self, box_number):
        pass

    def replace_randomly_from_screen(self, target_box_num):
        # target box num is the designated box that will replace the other box
        pass

    def get_boxes_locations(self):
        return self.boxes_on_screen_pos

    @suppress_warnings
    def get_box_dimensions(self):
        return IMG_BOX_WIDTH, IMG_BOX_HEIGHT

    def get_pris_dimensions(self):
        return self.prisoner.img_prisoner.get_rect().width, self.prisoner.img_prisoner.get_rect().height
