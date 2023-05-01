import tkinter
import warnings
from View.prisoner_view import PrisonerV
from View.settings import *
import pygame


def suppress_warnings(func):
    def wrapper(*args, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            return func(*args, **kwargs)

    return wrapper


class ScreenOperator:
    """
    Representation of all operations of draw object on screen and config secondary window.\n

    Attributes:\n
    error_prisoner_max: flag that indicates about if there was exception beyond the max number of prisoners.\n
    error_round_max: flag that indicates about if there was exception beyond the max number of rounds.\n
    font: font object to write text.\n
    p_color: prisoners text view color.\n
    r_color: rounds text view color.\n
    s_color: selects check box color.\n
    text_input_n: the actual text input prisoners from user.\n
    text_input_k: the actual text input rounds from user.\n
    pris_succeed: flag of the current prisoner succeeded or failed.\n
    current_round: the current round.\n
    num_succeeded: the number of all number of prisoners that have succeeded.\n
    size_main_screen: the size's main screen.\n
    main_screen: the main screen object of the game.\n
    background_image: the image of the background's game.\n
    start_rect: the rect object of the start button.\n
    start_hover_rect: the hover rect object of the start button.\n
    text_surface_start: the surface object of the text of start button.\n
    stats_rect: the rect object of the probs button.\n
    stats_hover_rect: the hover rect object of the probs button.\n
    text_surface_stats: the surface object of the text of probs button.\n
    reset_rect: the rect object of the reset button.\n
    reset_hover_rect: the hover rect object of the reset button.\n
    text_surface_reset: the surface object of the text of reset button.\n
    text: the text object of the secondary window (tkinter).\n
    """

    def __init__(self) -> None:
        """
        Initializes a ScreenOperator object.
        """
        # Font
        self.current_reach_time = 0
        self.error_prisoner_max = False
        self.error_round_max = False
        self.font = pygame.font.SysFont('monospace', FONT_SIZE, bold=True)

        # Variables
        self.p_color = RED
        self.r_color = BLACK
        self.s_color = BLACK
        self.text_input_n = ""
        self.text_input_k = ""
        self.pris_succeed = None
        self.current_round = -1
        self.num_succeeded = 0
        self.mouse_click = None

        # Screen and background
        self.size_main_screen = (screen_width, screen_height)
        self.main_screen = pygame.display.set_mode(self.size_main_screen)

        self.background_image = pygame.transform.scale(IMG_BACKGROUND, (screen_width, screen_height))
        self.floor_image = pygame.transform.scale(IMG_FLOOR, (floor_width, floor_height))

        # Buttons
        self.start_rect = pygame.Rect(button_x, button_y - 75, button_width, button_height)
        self.start_hover_rect = pygame.Rect(button_x, button_y - 75, button_width, button_height)
        self.text_surface_start = self.font.render("START", True, BLACK)

        self.stats_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        self.stats_hover_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        self.text_surface_stats = self.font.render("PROBS", True, BLACK)

        self.reset_rect = pygame.Rect(button_x, button_y + 75, button_width, button_height)
        self.reset_hover_rect = pygame.Rect(button_x, button_y + 75, button_width, button_height)
        self.text_surface_reset = self.font.render("RESET", True, BLACK)

        # Results
        self.run_only_probs = False
        self.text = None

    def draw_prisoner(self, prisoner: PrisonerV) -> None:
        """
        Draw prisoner on view.\n
        :param prisoner: The prisoner object to print -> PrisonerV object.

        :return: None
        """
        prisoner.draw_prisoner(self.font)

    def draw_failure(self, current_pris_num: int) -> None:
        """
        Draw prisoner on view.\n
        :param current_pris_num: The current prisoner number -> int object.

        :return: None
        """
        txt = 'Prisoner ' + str(current_pris_num) + ' has been failed'
        text_surface_failed = self.font.render(txt, True, RED)
        text_pos_failed = (screen_width // 3, 45)
        self.main_screen.blit(text_surface_failed, text_pos_failed)

    def draw_success(self, current_pris_num: int, num_succeeded: int) -> None:
        """
        Draw prisoner on view.\n
        :param current_pris_num: The current prisoner number -> int object.
        :param num_succeeded: The number of prisoner have been succeeded until now -> int object

        :return: None
        """
        self.num_succeeded = num_succeeded
        txt = 'Prisoner ' + str(current_pris_num) + ' has been succeeded'
        text_surface_succeed = self.font.render(txt, True, GREEN)
        text_pos_succeed = (screen_width // 3, 45)
        self.main_screen.blit(text_surface_succeed, text_pos_succeed)

    def draw_button(self, mouse_click: tuple[int, int, int], mouse_pos: tuple[int, int],
                    rect: pygame.Rect, hover: pygame.Rect, text_surface: pygame.Surface,
                    color: tuple[int, int, int], state: str, type_button: str) -> str:
        """
        Draw a button and handle mouse hover and click events and return the current state.\n

        :param type_button: A type of which button was pressed.
        :param state: A state representing the state of event.
        :param mouse_click: A tuple representing the state of the mouse buttons.
        :param mouse_pos: A tuple representing the position of the mouse cursor.
        :param rect: A pygame.Rect object representing the dimensions of the button.
        :param hover: A pygame.Rect object representing the dimensions of the hover rect of the button.
        :param text_surface: A pygame.Surface object representing the text to be displayed on the button.
        :param color: A tuple representing the color of the button.

        :return: str
        """
        self.mouse_click = mouse_click
        mouse_over_button = rect.collidepoint(mouse_pos)  # Check if mouse is over button

        if mouse_over_button:
            # Draw the hover rect if the mouse is over the button
            pygame.draw.rect(self.main_screen, color, hover)
        else:
            # Draw the normal state if the mouse is not over the button
            pygame.draw.rect(self.main_screen, WHITE, rect)

        # Draw the text surface in the center of the button
        self.main_screen.blit(text_surface, (rect.x + rect.width // 2 - text_surface.get_width() // 2,
                                             rect.y + rect.height // 2 - text_surface.get_height() // 2))

        # Check if mouse is over button and button is clicked

        if self.mouse_click[0] == 1 and not mouse_over_button:
            self.mouse_click = (False, False, False)
        if mouse_over_button and self.mouse_click[0] == 1 and type_button != 'reset':
            if type_button == 'start_button':
                state = 'begin'
            if type_button == 'reset_button':
                state = 'reset'
            if type_button == 'stats_button':
                state = 'stats'
        return state

    def draw_objects(self, boxes_on_screen_obj: dict, prisoner: PrisonerV) -> None:
        """
        Draw prisoner on view.\n
        :param boxes_on_screen_obj: The current prisoner number -> dict object.\n
        :param prisoner: Prisoner object to be printed -> Prisoner object.\n

        :return: None
        """
        self.draw_boxes(boxes_on_screen_obj)
        self.draw_prisoner(prisoner)
        self.draw_round_num()
        self.draw_num_succeeded()
        self.draw_time_reach_box()

    def draw_time_reach_box(self) -> None:
        """
        Draw the time between boxes.\n

        :return: None
        """
        self.draw_label(RED, screen_width // 2 + 250, 45, 'Time: ' + "{:.2f}".format(
            self.current_reach_time) + ' sec')  # Two digits after the decimal presentation

    def draw_round_num(self) -> None:
        """
        Draw the numbers of the current round on view.\n

        :return: None
        """
        txt = 'Current round : ' + str(self.current_round)
        text_surface_round = self.font.render(txt, True, BLACK)
        text_pos_round = (screen_width // 3 + 50, 20)
        self.main_screen.blit(text_surface_round, text_pos_round)

    @suppress_warnings
    def read_from_file(self) -> str:
        """
        Read from 'PrisonersResults.txt' the results to print on the secondary screen (tkinter) .\n

        :return: str
        """
        file = open("PrisonersResults.txt", "r")
        content = file.read()
        return content

    def config_text_window(self, tk: tkinter, root: tkinter.Tk) -> None:
        """
        Config the secondary window with scrollbar.\n
        :param tk: the tkinter object to run the window, text and the scrollbar.\n
        :param root: the secondary window .\n

        :return: None
        """
        # create scrollbar
        scrollbar_y = tk.Scrollbar(root)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_x = tk.Scrollbar(root, orient=tk.HORIZONTAL)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

        # create text widget
        self.text = tk.Text(root, yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set,
                            font=("TkDefaultFont", 14, "bold"), wrap='none', width=80)

        self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # configure scrollbar to scroll with text widget
        scrollbar_y.config(command=self.text.yview)
        scrollbar_x.config(command=self.text.xview)

    def write_text_on_secondary_screen(self, txt: tkinter.Text, tk: tkinter) -> None:
        """
        Write the text on the secondary screen (tkinter).\n
        :param tk: the tkinter object to run the window, text and the scrollbar.\n
        :param txt: the text object for the tkinter window .\n

        :return: None
        """
        self.text.delete("1.0", tk.END)  # delete all text from the widget
        self.text.insert(tk.END, txt)

    def draw_menu(self) -> None:
        """
        Draw all menu's objects.\n

        :return: None
        """
        # Draw the input text
        self.draw_label(self.p_color, 150, (screen_height - 70), 'Number of prisoners:')
        self.draw_label(RED, 150, (screen_height - 50), self.text_input_n)
        if self.error_prisoner_max:
            self.draw_label(RED, 150, (screen_height - 35), 'MAX ' + str(MAX_NO_PRIS) + ' prisoners in view')

        self.draw_label(self.r_color, 430, (screen_height - 70), 'Number of rounds:')
        self.draw_label(RED, 430, (screen_height - 50), self.text_input_k)
        if self.error_round_max:
            self.draw_label(RED, 430, (screen_height - 35), 'MAX ' + str(MAX_NO_ROUND) + ' rounds in view')

        self.draw_label(self.s_color, 680, (screen_height - 70), 'Specified result:')

    def draw_check_box(self, print_specify: bool) -> None:
        """
        Draw the checkbox for printing the result to be specified or not.\n
        :param print_specify: bool object to print specified results .\n

        :return: None
        """
        select_box = pygame.Rect(900, (screen_height - 70), 20, 20)
        if print_specify:
            text = 'X'
        else:
            text = ''
        pygame.draw.rect(self.main_screen, RED, select_box, 2)
        text_surface = self.font.render(text, True, RED)
        self.main_screen.blit(text_surface, (904, (screen_height - 70)))

    def draw_label(self, color: tuple[int, int, int], pos_x: int, pos_y: int, text: str = "") -> None:
        """
        Draws a label on the screen.

        :param color: The color of the label as an RGB tuple.
        :param pos_x: The x position of the top-left corner of the label.
        :param pos_y: The y position of the top-left corner of the label.
        :param text: The text to be displayed in the label. Defaults to an empty string.
        """
        text_surface = self.font.render(text, True, color)
        self.main_screen.blit(text_surface, (pos_x, pos_y))

    @suppress_warnings
    def draw_boxes(self, boxes_on_screen_obj: dict) -> None:
        """
        Draw the all the boxes on the screen.\n
        :param boxes_on_screen_obj: dict object position of all boxes to be drawn on screen .\n

        :return: None
        """
        for box_num in boxes_on_screen_obj.keys():
            boxes_on_screen_obj[box_num].draw_box()

    def draw_screen(self) -> None:
        """
        Draw the main screen.\n

        :return: None
        """
        self.main_screen.blit(self.background_image, (0, 0))
        self.main_screen.blit(self.floor_image, (138, 70))
        self.draw_menu()

    def draw_num_succeeded(self) -> None:
        """
        Draw the number of prisoner that have been succeeded on the screen.\n

        :return: None
        """
        txt_num_succeeded = str(self.num_succeeded) + ' Succeeded'
        text_surface_num_succeed = self.font.render(txt_num_succeeded, True, GREEN)
        text_pos_num_succeed = (screen_width // 2 + 250, 20)
        self.main_screen.blit(text_surface_num_succeed, text_pos_num_succeed)
