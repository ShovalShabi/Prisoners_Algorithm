
from View.box_view import BoxV
from View.prisoner_view import PrisonerV
from View.settings import *
import pygame


class ScreenOperator:
    """
    A class that designated for handling blitting to screen and draw the objects of the frontend part of the game.
    """

    def __init__(self) -> None:
        # Font
        self.font = pygame.font.SysFont('monospace', FONT_SIZE, bold=True)

        # Variables
        self.p_color = RED
        self.r_color = BLACK
        self.s_color = BLACK
        self.text_input_n = ""
        self.text_input_k = ""
        self.pris_succeed = None
        self.current_round = -1

        # Screen and background
        self.size_main_screen = (screen_width, screen_height)
        self.main_screen = pygame.display.set_mode(self.size_main_screen)

        self.image_background = IMG_BACKGROUND
        self.background_image = pygame.transform.scale(self.image_background, (screen_width, screen_height))

        # Buttons
        self.start_rect = pygame.Rect(button_x, button_y + 75, button_width, button_height)
        self.start_hover_rect = pygame.Rect(button_x, button_y + 75, button_width, button_height)
        self.text_surface_start = self.font.render("START", True, BLACK)
        self.reset_rect = pygame.Rect(button_x, button_y + 150, button_width, button_height)
        self.reset_hover_rect = pygame.Rect(button_x, button_y + 150, button_width, button_height)
        self.text_surface_reset = self.font.render("RESET", True, BLACK)

        # Results
        self.scrollbar = None
        self.text = None

    def draw_prisoner(self, prisoner: PrisonerV) -> None:
        """
        Draws the prisoner on the screen.
        """
        prisoner.draw_prisoner(self.font, self.pris_succeed)

    def draw_button(self, mouse_click: tuple[int, int, int], mouse_pos: tuple[int, int],
                    rect: pygame.Rect, hover: pygame.Rect, text_surface: pygame.Surface,
                    color: tuple[int, int, int], state: str, type_button: str, check_exist_input) -> str:
        """
        Draw a button and handle mouse hover and click events.\n

        :param type_button: A type of which button was pressed.
        :param state: A state representing the state of event.
        :param mouse_click: A tuple representing the state of the mouse buttons.
        :param mouse_pos: A tuple representing the position of the mouse cursor.
        :param rect: A pygame.Rect object representing the dimensions of the button.
        :param hover: A pygame.Rect object representing the dimensions of the hover rect of the button.
        :param text_surface: A pygame.Surface object representing the text to be displayed on the button.
        :param color: A tuple representing the color of the button.

        Args:
            check_exist_input:
            check_exist_input:
        """
        if rect.collidepoint(mouse_pos):
            # Draw the hover rect if the mouse is over the button
            pygame.draw.rect(self.main_screen, color, hover)
            if mouse_click[0] == 1 and check_exist_input():
                if type_button == 'start_button':
                    state = 'begin'
                if type_button == 'reset_button':
                    state = 'reset'
        else:
            # Draw the normal state if the mouse is not over the button
            pygame.draw.rect(self.main_screen, WHITE, rect)

        # Draw the text surface in the center of the button
        self.main_screen.blit(text_surface, (rect.x + rect.width // 2 - text_surface.get_width() // 2,
                                             rect.y + rect.height // 2 - text_surface.get_height() // 2))
        return state

    def draw_objects(self, boxes_on_screen_obj, prisoner) -> None:
        """
        Function that draws the game elements on the screen.
        """
        self.draw_boxes(boxes_on_screen_obj)
        # self.draw_boxes_temp(boxes_on_screen_obj)  <------- Added this
        self.draw_prisoner(prisoner)
        self.draw_round_num()

    def draw_round_num(self):
        txt = 'Current round : ' + str(self.current_round)
        text_surface_round = self.font.render(txt, True, BLACK)
        text_pos_round = (screen_width // 3 + 50, 20)
        self.main_screen.blit(text_surface_round, text_pos_round)

    def config_text_window(self, tk, root):

        # Create a Text widget and pack it in the window
        # create scrollbar
        self.scrollbar = tk.Scrollbar(root)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        # create text widget
        self.text = tk.Text(root, yscrollcommand=self.scrollbar.set)
        self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # configure scrollbar to scroll with text widget
        self.scrollbar.config(command=self.text.yview)

    def write_text_on_secondary_screen(self, txt, tk):
        self.text.delete("1.0", tk.END)  # delete all text from the widget
        self.text.insert(tk.END, txt)

    def draw_menu(self) -> None:
        """
        Draws the menu on the screen.
        """
        # Draw the input text
        self.draw_label(self.p_color, 150, 770, 'Number of prisoners:')
        self.draw_label(RED, 150, 790, self.text_input_n)
        self.draw_label(self.r_color, 430, 770, 'Number of rounds:')
        self.draw_label(RED, 430, 790, self.text_input_k)
        self.draw_label(self.s_color, 680, 770, 'Specified result:')

    def draw_check_box(self, print_specify) -> None:
        select_box = pygame.Rect(900, 770, 20, 20)
        if print_specify:
            text = 'X'
        else:
            text = ''
        pygame.draw.rect(self.main_screen, RED, select_box, 2)
        text_surface = self.font.render(text, True, RED)
        self.main_screen.blit(text_surface, (904, 770))

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

    def draw_boxes(self, boxes) -> None:
        """
        Draws the boxes on the screen.
        """

        num_of_boxes_view = len(boxes)

        if num_of_boxes_view <= MAX_BOX_WIDTH:
            for box_index, location in enumerate(boxes):
                box = BoxV(self.main_screen, box_index)
                box.pos = box.draw_box(box.box_num, 0, self.font)

        else:
            rows = num_of_boxes_view // MAX_BOX_WIDTH
            remainder = num_of_boxes_view % MAX_BOX_WIDTH

            for row in range(rows):
                for box_index in range(MAX_BOX_WIDTH):
                    box = BoxV(self.main_screen, row * MAX_BOX_WIDTH + box_index)
                    box.pos = box.draw_box(box_index, row, self.font)

            for rem in range(remainder):
                box = BoxV(self.main_screen, rows * MAX_BOX_WIDTH + rem)
                box.pos = box.draw_box(rem, rows, self.font)

    #*******************Added This************************#
    def draw_boxes_temp(self,boxes_on_screen_obj:dict):
        for box_num in boxes_on_screen_obj.keys():
            boxes_on_screen_obj[box_num].draw_box_temp()
    #*****************************************************#

    def draw_screen(self):
        self.main_screen.blit(self.background_image, (0, 0))
        self.draw_menu()
