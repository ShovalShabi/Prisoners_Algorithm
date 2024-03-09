import pygame.draw
from View.settings import *  # Importing constants and settings
from pygame import Surface, image, Rect
from pygame.font import SysFont
import os

class BoxV:
    """ Representation of the BoxM object by actual images for the user.

    Attributes:
    text_surface: Text surface for view texts.
    box_num: Box number -> int.
    print_num: The number that prints on the view.
    pos: The position tuple of (x,y) in form -> tuple[int,int].
    screen: Object that blitting the box image on screen.
    chest_img: Surface object to the next target box.
    color_num: The color of the number presented in view -> Color object.
    open: If the box is open or closed -> boolean.
    """

    def __init__(self, screen: Surface, box_num: int) -> None:
        """ Initializes a BoxV object. """
        self.box_num = box_num
        self.print_num = self.box_num
        self.pos = None
        self.screen = screen
        self.open = False

        # Create font objects once
        self.font = pygame.font.SysFont('monospace', FONT_SIZE, bold=True)
        self.font_prev_num = pygame.font.SysFont('monospace', FONT_SIZE, bold=True)

        # Load the initial image
        self.chest_img = image.load(os.path.join('View/Resources/chest_closed.png'))
        self.chest_img = self.chest_img.convert_alpha()  # Convert the image to have per-pixel alphas
        self.rect = self.chest_img.get_rect()

        # Create the text surface and blit it onto the chest_img
        self.color_num = YELLOW
        self.text_surface = self.font.render(str(self.print_num), True, self.color_num)
        text_rect = self.text_surface.get_rect()
        text_rect.center = self.rect.center
        self.chest_img.blit(self.text_surface, text_rect)

    def load_images(self, new_name_img: str) -> None:
        """ Loads the new image.
        :param new_name_img: The name of the new image to be load -> str object.
        :return: None
        """
        self.chest_img = image.load(os.path.join('View/Resources/' + new_name_img))
        self.chest_img = self.chest_img.convert_alpha()  # Convert the image to have per-pixel alphas
        self.rect = self.chest_img.get_rect()

    def draw_box(self) -> None:
        """ Draw the box on view.
        :return: None
        """
        self.screen.blit(self.chest_img, self.rect.topleft)
        if self.open:
            text_surface_prev_num = self.font_prev_num.render(str(self.box_num), True, BLACK)
            prev_num_rect = text_surface_prev_num.get_rect()
            prev_num_rect.midtop = self.rect.move(IMG_BOX_WIDTH // 2, -15).midtop
            self.screen.blit(text_surface_prev_num, prev_num_rect)

    def open_box(self, new_name_img: str, pointing_num_box: int, color_num: tuple[int,int,int]) -> None:
        """Opens the box, switches the image, and adds the pointing number to it.
        The actual box_num will be displayed in the upper right corner and the pointing_num_box will be displayed at the center of the image.
        :param new_name_img: The new name of the image to be loaded -> str object.
        :param pointing_num_box: The number to be displayed on the box -> int.
        :param color_num: The color of the number to be displayed -> tuple[int,int,int].
        :return: None
        """
        print(f"box:{self.box_num} before switching image pos:{self.rect.x,self.rect.y}")
        self.load_images(new_name_img=new_name_img)
        self.blit_number_on_box(num=pointing_num_box,color_num=color_num)
        self.open = True
        self.set_pos(self.get_pos())
        print(f"box:{self.box_num} after switching image pos:{self.rect.x,self.rect.y}")


    def close_box(self, new_name_img: str, color:tuple[int,int,int]) -> None:
        """Closes the box, switches the image, and adds the original box number to it.
        :param new_name_img: The new name of the image to be loaded -> str object.
        :param color: The color of the number to be displayed -> tuple[int,int,int].
        :return: None
        """
        self.load_images(new_name_img=new_name_img)
        self.blit_number_on_box(num=self.box_num,color_num=color)
        self.open = False
        self.set_pos(self.get_pos())

    def blit_number_on_box(self, num:int ,color_num: tuple[int,int,int]) ->None:
        """Blits the given number on the box with specified color.
        :param num: The number to be displayed on the box -> int.
        :param color_num: The color of the number to be displayed -> tuple[int,int,int].
        :return: None
        """
        self.text_surface = self.font.render(str(num), True, color_num)
        text_rect = self.text_surface.get_rect()
        text_rect.center = self.rect.center
        self.chest_img.blit(self.text_surface, text_rect)

    def set_pos(self, new_pos: tuple[int, int]) -> None:
        """ Set the boxV position.
        :param new_pos: The new position of the box -> tuple object.
        :return: None
        """
        self.pos = new_pos
        self.rect.topleft = new_pos

    def get_pos(self) -> tuple[int, int]:
        """ Return the boxV position.
        :return: position's box -> tuple
        """
        return self.pos
