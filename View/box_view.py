import pygame.draw

from View.settings import *
from pygame import Surface, image, Rect
from pygame.font import SysFont
import os


class BoxV:
    """
    Representation of the BoxM object by actual images for the user.\n

    Attributes:\n
    text_surface: text surface for view texts.\n
    box_num: box number -> int.\n
    print_num: the number that print on the view.\n
    pos: the position tuple of (x,y) in form -> tuple[int,int].\n
    screen: object that blitting the box image on screen.\n to the next target box -> Surface object.\n
    load_images: load images of chest -> Surface object.\n
    color_num: the color of the number presented in view -> Color object.\n
    open: if the box is open or closed -> boolean.\n
    """

    def __init__(self, screen: Surface, box_num: int) -> None:
        """
        Initializes a BoxV object.\n
        """
        self.text_surface = None
        self.box_num = box_num
        self.print_num = self.box_num
        self.pos = None
        self.screen = screen
        self.chest_img = None
        self.load_images('chest_closed.png')
        self.color_num = YELLOW
        self.open = False

    def clear_image(self, next_num: int) -> None:
        """
        Clear the image in view.\n
        :param next_num: The next number to print -> int object.

        :return: None
        """
        self.print_num = next_num
        self.text_surface = None

    def close_box(self, num: int) -> None:
        """
        Close the box image in view.\n
        :param num: The current number to print -> int object.

        :return: None
        """
        self.print_num = num
        self.open_box('chest_closed.png', YELLOW)
        self.open = False

    def open_box(self, new_name_img: str, color: pygame.Color) -> None:
        """
        Open the box image in view.\n
        :param new_name_img: The name of the new image to be load -> str object.\n
        :param color: the color of the number that presents on view.\n

        :return: None
        """
        self.load_images(new_name_img)
        self.color_num = color
        self.draw_box()
        self.open = True

    def load_images(self, new_name_img: str) -> None:
        """
        Loads the new image.\n
        :param new_name_img: The name of the new image to be load -> str object.\n

        :return: None
        """
        self.chest_img = image.load(os.path.join('View/Resources/' + new_name_img))

    def draw_box(self) -> None:
        """
        Draw the box on view.\n

        :return: None
        """
        font = SysFont('monospace', FONT_SIZE, bold=True)
        rect = Rect(self.pos[0], self.pos[1], CELL_SIZE, CELL_SIZE)
        self.text_surface = font.render(str(self.print_num), True, self.color_num)
        text_rect = self.text_surface.get_rect()
        text_rect.center = self.chest_img.get_rect().center
        self.chest_img.blit(self.text_surface, text_rect)
        self.screen.blit(self.chest_img, rect)

        if self.open:
            font_prev_num = SysFont('monospace', FONT_SIZE, bold=True)
            rect_prev_num = Rect(self.pos[0] + IMG_BOX_WIDTH//2, self.pos[1] - 15, IMG_BOX_WIDTH, 10)
            text_surface_prev_num = font_prev_num.render(str(self.box_num), True, BLACK)
            self.screen.blit(text_surface_prev_num, rect_prev_num.center)




    def set_pos(self, new_pos: tuple[int, int]) -> None:
        """
        Set the boxV position.\n
        :param new_pos: The new position of the box -> tuple object.\n

        :return: None
        """
        self.pos = new_pos

    def get_pos(self) -> tuple[int, int]:
        """
        Return the boxV position.\n

        :return: position's box -> tuple
        """
        return self.pos
