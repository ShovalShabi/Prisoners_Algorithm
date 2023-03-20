import math
import sys
import pygame.time
import tkinter as tk
from random import randint

from pygame import Surface
from pygame.event import Event
from pygame.locals import KEYDOWN, K_BACKSPACE
from View.screen_operator import ScreenOperator, suppress_warnings
from View.prisoner_view import PrisonerV
from View.settings import *
from View.box_view import BoxV
from pygame.time import Clock
import pygame.mixer


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
    current_round: the current round in the game -> int object.\n
    num_of_rounds: the number of rounds -> int.\n
    actual_num_of_boxes: the number of boxes that view handle,can be more than the screen can represent -> int.\n
    print_specify: the flag if the results would be specify or not.\n
    prisoner: the prisoner that is currently searching for his number -> PrisonerV object.\n
    listener: coordinates the activity between the backend and the frontend -> Controller object.\n
    boxes_on_screen_obj: dictionary of BoxV objects that are currently on screen mapped by their
     number -> dict of {int:BoxV object}.\n
    boxes_on_screen_pos: dictionary of tuple of position of each BoxV object, mapped by their
     number -> dict of {int: tuple (x,y)}.\n
    boxes_off_screen_obj: dictionary of BoxV objects that are not currently on screen mapped by their
     number -> dict of {int:BoxV object}.\n
    list_depend: list of box dependencies number from zero to num of prisoners - 1.\n
    root: tkinter window (secondary screen).\n
    screen_operator: object that organizes the drawing of the objects on screen, fonts and
     buttons -> ScreenOpreator object.\n
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
        self.current_round = 0
        self.num_of_rounds = 0
        self.actual_num_of_boxes = 0
        self.print_specify = False

        # Objects
        self.prisoner = None
        self.listener = None
        self.boxes_on_screen_obj = {}
        self.boxes_on_screen_pos = {}
        self.boxes_off_screen_obj = {}
        self.list_depend = {}  # Dictionary of {num round : list of dependencies}

        # Screen Operations
        self.root = None
        self.screen_operator = None
        self.clock = Clock()

    @suppress_warnings
    def pygame_setup(self) -> None:
        """
        Setup all pygame init functions.\n

        :return: None
        """
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("Prisoners Riddle")
        self.screen_operator = ScreenOperator()

    def run(self) -> None:
        """
        Main loop of the game. Runs until self.running is False.\n

        :returns: None.
        """

        # Initialize the game
        self.pygame_setup()
        self.set_secondary_window()
        self.screen_operator.config_text_window(tk, self.root)
        self.screen_operator.write_text_on_secondary_screen(USER_GUIDE, tk)

        while self.running:

            # draw the main screen
            self.screen_operator.draw_screen()

            # listens to event
            if self.state != 'running':
                self.screen_operator.draw_boxes(boxes_on_screen_obj=self.boxes_on_screen_obj)
            self.listen_to_events()
            self.button_events()

            # Occurs when reset button is clicked
            if self.state == 'reset':
                self.reset_input_view()
                self.ntfy_to_model_stop_running()

            if self.state == 'not running':
                # Create and draw the boxes, handle events, and update the button states
                self.create_boxes()

            # Occurs when start button is clicked
            if self.state == 'stats' and self.check_exist_input():
                print(self.actual_num_of_boxes, self.num_of_prisoners)
                self.listener.view_need_to_init_statistics(self.actual_num_of_boxes, self.num_of_rounds, DOOR_WAY,
                                                           self.print_specify)

                # prints result to tk
                self.tk_print_results()

                pris_num = self.view_request_pris_num()
                self.create_prisoner(pris_num)
                self.state = "not running"

            # Occurs when start button is clicked
            if self.state == 'begin' and self.check_exist_input():
                self.list_depend = self.listener. \
                    view_need_to_init_game(self.num_of_prisoners, self.num_of_rounds, DOOR_WAY, self.print_specify)

                # prints result to tk
                self.tk_print_results()

                pris_num = self.view_request_pris_num()
                self.create_prisoner(pris_num)
                self.state = "running"

            if self.state == "running":
                pris_num = self.view_request_pris_num()
                self.current_round = self.view_request_round_num()

                if pris_num != self.prisoner.pris_num:
                    self.replace_prisoner(prisoner_num=pris_num)

                self.screen_operator.current_round = self.current_round

                if self.view_request_is_running_game():
                    self.view_request_run_game()

                    pos = self.view_request_pris_pos()
                    self.prisoner.set_pris_pos(pos=pos)

                    self.screen_operator.draw_objects(self.boxes_on_screen_obj, self.prisoner)
                else:
                    self.state = 'reset'
                self.clock.tick(FRAME_RATE)

            # Update the display
            pygame.display.update()
            self.root.update()

        # Quit the game
        pygame.quit()
        self.root.quit()
        sys.exit()

    def tk_print_results(self) -> None:
        """
        Print the results from the file into the secondary results (tkinter).

        :return: None
        """
        result = self.screen_operator.read_from_file()
        self.screen_operator.write_text_on_secondary_screen(result, tk)

    def set_secondary_window(self) -> None:
        """
        Set up the secondary screen with specific size and disable resizable

        :return: None
        """
        self.root = tk.Tk()
        self.root.geometry('500x500')
        self.root.resizable(width=True, height=False)  # disable diagonal resize

    def reset_input_view(self) -> None:
        """
        Method that resets all the view controls and screen.\n

        :return: None
        """

        # Variables
        self.num_of_boxes_view = 0
        self.num_of_prisoners = 0
        self.status = 'Prisoner'
        self.num_of_rounds = 0
        self.actual_num_of_boxes = 0
        self.print_specify = False
        self.screen_operator.current_round = -1
        self.screen_operator.num_succeeded = 0

        # Objects
        self.boxes_on_screen_pos.clear()
        self.boxes_off_screen_obj.clear()
        self.boxes_on_screen_obj.clear()

        # Screen
        self.screen_operator.text_input_n = ""
        self.screen_operator.text_input_k = ""
        self.print_specify = False

        # State
        self.state = 'not running'

    def check_exist_input(self) -> bool:
        """
        Checks if the input is not empty and valid.

        :return: valid or invalid -> bool
        """
        if self.screen_operator.text_input_k == '' or self.screen_operator.text_input_n == '':
            return False
        elif int(self.screen_operator.text_input_n) < 2:
            return False
        return True

    def button_events(self) -> None:
        """
        Method that handles with button events, mouse events and checkbox event.\n

        :return: None.
        """
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        self.screen_operator.draw_check_box(self.print_specify)
        if self.state != 'running' and self.check_exist_input() and not self.screen_operator.error_round_max and not self.screen_operator.error_prisoner_max:
            self.state = self.screen_operator.draw_button(mouse_click, mouse_pos, self.screen_operator.start_rect,
                                                          self.screen_operator.start_hover_rect,
                                                          self.screen_operator.text_surface_start,
                                                          GREEN, self.state, 'start_button')
        if self.state != 'running' and self.check_exist_input():
            self.state = self.screen_operator.draw_button(mouse_click, mouse_pos, self.screen_operator.stats_rect,
                                                          self.screen_operator.stats_hover_rect,
                                                          self.screen_operator.text_surface_stats,
                                                          ORANGE, self.state, 'stats_button')
        self.state = self.screen_operator.draw_button(mouse_click, mouse_pos, self.screen_operator.reset_rect,
                                                      self.screen_operator.reset_hover_rect,
                                                      self.screen_operator.text_surface_reset,
                                                      RED, self.state, 'reset_button')

    def listen_to_events(self) -> None:
        """
        Method that listening to events that happen in the game \n
        and handle the input from the GUI.\n

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
                if self.status == 'X_pressed':
                    if event.key == pygame.K_SPACE:
                        self.print_specify = not self.print_specify

    def decide_input_type(self, event: Event) -> None:
        """
        Method that decide on the input type and make the color selected input text to RED and others BLACK.\n
        :param event: event that triggered by the user -> Event object.\n

        :return: None.
        """
        if event.key == pygame.K_LEFT:
            self.status = 'Prisoner'
            self.screen_operator.p_color = RED
            self.screen_operator.r_color = BLACK
            self.screen_operator.s_color = BLACK
        if event.key == pygame.K_RIGHT:
            self.status = 'Round'
            self.screen_operator.p_color = BLACK
            self.screen_operator.r_color = RED
            self.screen_operator.s_color = BLACK
        if event.key == pygame.K_x:
            self.status = 'X_pressed'
            self.screen_operator.p_color = BLACK
            self.screen_operator.r_color = BLACK
            self.screen_operator.s_color = RED
            self.print_specify = not self.print_specify

    def convert_input_round_to_num(self) -> None:
        """
        Method that converts the text input for the number of rounds to an integer.\n

        :return: None.
        """
        if self.screen_operator.text_input_k != "" and str.isdigit(self.screen_operator.text_input_k):
            num = int(self.screen_operator.text_input_k)
            if num <= MAX_NO_ROUND:
                self.num_of_rounds = num
                self.screen_operator.error_round_max = False
            else:
                self.num_of_rounds = MAX_NO_ROUND
                self.screen_operator.error_round_max = True
        else:
            self.screen_operator.text_input_k = ""
            self.num_of_rounds = 0

    def update_prisoner_location(self, pos: tuple[int, int]) -> None:
        """
        Updates the location of the prisoner.\n
        :param pos: The new location of the prisoner as a tuple of integers (x, y).\n

        :return: None.
        """
        self.prisoner.set_pris_pos(pos)

    def convert_input_prisoner_to_num(self) -> None:
        """
        Converts the text input for the number of prisoners to an integer.
        """
        if self.screen_operator.text_input_n != "" and str.isdigit(self.screen_operator.text_input_n):
            num = int(self.screen_operator.text_input_n)

            if num > MAX_NO_PRIS:  # occurs when the input is above the max num of prisoners
                self.screen_operator.error_prisoner_max = True
                self.screen_operator.run_only_probs = True
            else:  # occurs when the input is below the max num of prisoners
                self.screen_operator.error_prisoner_max = False

                if num <= MAX_NO_PRISONER_BOX:
                    self.num_of_boxes_view = num
                else:  # occurs when the input is valid and there are boxes more than the displayed
                    self.num_of_boxes_view = MAX_NO_PRISONER_BOX

                self.num_of_prisoners = num
            self.actual_num_of_boxes = num
        else:
            self.screen_operator.text_input_n = ""
            self.num_of_boxes_view = 0
            self.num_of_prisoners = 0

    @suppress_warnings
    def handle_input(self, event_input: Event, text: str = "") -> str:
        """
        Method that updates the text based on the given input event.\n

        :param event_input: the input event to handle -> Event object.\n
        :param text: the current text -> str object.\n

        :return: the updated text -> str object.
        """
        if event_input.key == K_BACKSPACE:
            if len(text) > 0:
                self.boxes_on_screen_obj.clear()
                self.boxes_on_screen_pos.clear()
                text = text[:-1]
        else:
            text += event_input.unicode
        return text

    def create_boxes(self) -> None:
        """
        Method that creates boxes on screen and determines which boxes are on
        screen in case of overflow and also in charge of the position of each box.\n

        :return: None
        """
        rows = int(math.floor(self.num_of_boxes_view / MAX_BOX_WIDTH))
        remainder = self.num_of_boxes_view - rows * MAX_BOX_WIDTH

        # create the boxes the complete a row of boxes
        for row in range(rows):
            for col in range(MAX_BOX_WIDTH):
                box = BoxV(screen=self.screen_operator.main_screen, box_num=row * MAX_BOX_WIDTH + col + 1)
                box.set_pos(new_pos=(BOX_START_X + col * CELL_SIZE, BOX_START_Y + row * CELL_SIZE))
                self.boxes_on_screen_obj[box.box_num] = box  # Mapping objects of BoxV by their number
                self.boxes_on_screen_pos[
                    box.box_num] = box.get_pos()  # Mapping positions of BoxV objects by their number

        # create the remained boxes
        for rem in range(remainder):
            box = BoxV(screen=self.screen_operator.main_screen, box_num=rows * MAX_BOX_WIDTH + rem + 1)
            box.set_pos(new_pos=(BOX_START_X + rem * CELL_SIZE, BOX_START_Y + rows * CELL_SIZE))
            self.boxes_on_screen_obj[box.box_num] = box
            self.boxes_on_screen_pos[box.box_num] = box.get_pos()

        # occurs when there boxes the overflow the screen and the amount of the boxes inputted is valid
        if self.actual_num_of_boxes - MAX_NO_PRISONER_BOX > 0:
            for box_index in range(MAX_NO_PRISONER_BOX + 1, self.actual_num_of_boxes + 1):
                box = BoxV(screen=self.screen_operator.main_screen, box_num=box_index)
                self.boxes_off_screen_obj[box.box_num] = box

        # update boxes positions
        self.view_request_update_boxes_pos()

    def create_prisoner(self, num_prisoner: int) -> None:
        """
        Method that creates a new PrisonerV object.
        :param num_prisoner: An integer representing the number of the prisoner.\n

        :return: None.
        """
        self.prisoner = PrisonerV(DOOR_WAY, num_prisoner, self.screen_operator.main_screen,
                                  self.generate_random_image().convert_alpha())

    @suppress_warnings
    def generate_random_image(self) -> Surface:
        """
        Method that generate random image's prisoner to load.

        :return: The image itself -> Surface.
        """
        images = [IMG_SP1_F, IMG_SP2_F, IMG_SP3_F, IMG_SP4_F, IMG_FP1_F, IMG_FP2_F]
        image_name = images[randint(0, len(images) - 1)]
        return image_name

    def replace_prisoner(self, prisoner_num: int) -> None:
        """
        Method that replaces the current prisoner with a new one and close all boxes when prisoner replaces.\n
        :param prisoner_num: An integer representing the number of the new prisoner.\n

        :return: None.
        """
        for box in self.boxes_on_screen_obj.values():
            box.close_box(box.box_num)
        self.create_prisoner(prisoner_num)

    def handle_box_request(self, box_number: int) -> None:
        """
        Method that gets a new box number that overflows the screen and replaces an existing box in the screen
        :param box_number: An integer representing the number of the box would be display on the screen.\n

        :return: None.
        """

        # check if the overflow box num is not in the view box on the screen
        if box_number in self.boxes_on_screen_pos.keys():
            return
        else:
            replaced_num_box = 0
            while replaced_num_box not in self.boxes_on_screen_pos or box_number == replaced_num_box:
                replaced_num_box = randint(1, self.num_of_prisoners)
            print(f"replaced {replaced_num_box} with box {box_number}")

            pos = self.boxes_on_screen_pos.pop(
                replaced_num_box)  # The value position of the replaced box is moved to a local variable
            self.boxes_on_screen_obj.pop(replaced_num_box)

            # Putting the new box on the other bo position on screen
            self.boxes_off_screen_obj.pop(box_number)  # Removing the target box from self.boxes_off_screen_obj
            target_box = BoxV(screen=self.screen_operator.main_screen, box_num=box_number)
            self.boxes_on_screen_pos.update({box_number: pos})
            self.boxes_on_screen_obj.update({box_number: target_box})
            target_box.set_pos(pos)

            # Putting the replaced box in self.boxes_off_screen_obj
            replaced_box = BoxV(screen=self.screen_operator.main_screen,
                                box_num=replaced_num_box)  # Creating new object of the replaced box
            self.boxes_off_screen_obj.update({replaced_num_box: replaced_box})
            self.view_request_update_boxes_pos()

    def open_box(self, box_num: int) -> None:
        """
        Method that opens the box according the box number.
        :param box_num: An integer representing the number of the box to be opened.\n

        :return: None.
        """
        # clear the current box image
        if not self.boxes_on_screen_obj[box_num].open:
            self.boxes_on_screen_obj[box_num].clear_image(self.list_depend[self.current_round][box_num - 1])

            # replace the image
            self.boxes_on_screen_obj[box_num].open_box(new_name_img="chest_open.png", color=RED)
            # list of dependencies starting from 0

            OPEN_CHEST_SOUND.play()  # plays the open chest sound
            self.clock.tick(WAIT_FRAME_RATE)  # waits 1 frame rate

    def get_boxes_locations(self) -> dict:
        """
        Method returns the dictionary of the boxes on the screen

        :return:  boxes on the screen -> dict.
        """
        return self.boxes_on_screen_pos

    @suppress_warnings
    def get_box_dimensions(self) -> tuple:
        """
        Method that returns the box dimensions on the screen.

        :return: box dimension -> tuple.
        """
        return IMG_BOX_WIDTH, IMG_BOX_HEIGHT

    def get_pris_dimensions(self) -> tuple:
        """
        Method that returns the prisoner dimensions on the screen.

        :return: box dimension -> tuple.
        """
        return self.prisoner.img_prisoner.get_rect().width, self.prisoner.img_prisoner.get_rect().height

    @suppress_warnings
    def handle_with_success(self, current_pris_num, num_succeeded) -> None:
        """
        Method that plays success sound and text of success on the screen and how many succeeded until now.
        :param current_pris_num: the current prisoner number.\n
        :param num_succeeded: the number of the successes of the prisoner until now.\n

        :return: None.
        """
        SUCCESS_SOUND.play()
        self.screen_operator.draw_success(current_pris_num, num_succeeded)
        pygame.display.update()
        self.clock.tick(1)

    @suppress_warnings
    def handle_with_failure(self, current_pris_num) -> None:
        """
        Method that plays failure sound and text of failure on the screen.
        :param current_pris_num: the current prisoner number.\n

        :return: None
        """
        FAILURE_SOUND.play()
        self.screen_operator.draw_failure(current_pris_num)
        pygame.display.update()
        self.clock.tick(1)

    """*******************************************MVC Methods******************************************************"""

    def view_request_pris_pos(self) -> tuple[int, int]:
        """
        Method that requests from the model the current prisoner position.\n

        :return: the position of prisoner -> tuple (x,y).
        """
        return self.listener.view_need_pris_pos()

    def view_request_to_start_game(self, num_of_prisoners: int, num_of_rounds: int, initial_pos: tuple[int, int],
                                   print_specifically: bool) -> dict:
        """
        Method that send the data to model object.

        :param print_specifically: indication for amount of the specification in PrisonersResults.txt -> bool.\n
        :param initial_pos: tuple of position on screen -> tuple (x,y).\n
        :param num_of_rounds: The numbers of input rounds -> int.\n
        :param num_of_prisoners: The numbers of input prisoners -> int.\n

        :return: The round dict of list dependencies.
        """
        return self.listener.view_need_to_init_game(num_of_prisoners, num_of_rounds, initial_pos, print_specifically)

    def view_request_round_num(self) -> int:
        """
        Method that requests from the model the current prisoner number.\n

        :return: the number of prisoner -> int.
        """
        return self.listener.view_need_round_num()

    def view_request_pris_num(self) -> int:
        """
        Method that requests from the model the current prisoner number.\n

        :return: the number of prisoner -> int.
        """
        return self.listener.view_need_pris_num()

    def view_request_run_game(self) -> None:
        """
        Method that requests from the model to start the game.\n

        :return: None.
        """
        self.listener.view_need_to_run_game()

    def view_request_is_running_game(self) -> None:
        """
        Method that checks the game status in the back.\n

        :return: None.
        """
        return self.listener.view_need_know_game_status()

    def view_request_update_boxes_pos(self) -> None:
        """
        Method that needs update of the boxes positions from the back.\n

        :return: None.
        """
        self.listener.view_need_update_boxes_pos()

    #### Shoval need to create #####
    def view_request_update_time_boxes(self) -> None:
        """
        Method that needs update of the time between one box to other box.\n

        :return: None.
        """
        self.screen_operator.current_reach_time = self.listener.view_request_update_time_boxes()

    ################################

    def ntfy_to_model_stop_running(self) -> None:
        """
        Method that notifies to model to stop the running game.\n

        :return: None.
        """
        self.listener.view_need_model_stop_running()

    def set_listener(self, listener) -> None:
        """
        Sets the listener for the ViewManager object.
        :param listener: The listener object to be set -> Controller object.\n

        :return: None.
        """
        self.listener = listener
