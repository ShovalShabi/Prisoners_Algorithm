from View.settings import *
from pygame import Surface, image, Rect
from pygame.font import Font
import os

from View.settings import MAX_BOX_WIDTH


class BoxV:
    """
    Representation of the BoxM object by actual images for the user.\n

    Attributes:\n
    box_num: box number -> int.\n
    pos: the position tuple of (x,y) in form -> tuple[int,int].\n
    screen: object that blitting the box image on screen.\n to the next target box -> Surface object.\n
    closed_chest_img: image of closed chest -> Surface object.\n
    open_chest_img: image of open chest -> Surface object.\n
    """
    def __init__(self, screen: Surface, box_num: int) -> None:
        """
        Initializes a BoxV object.\n
        :param screen: The pygame surface to draw the box on -> Surface object.
        :param box_num: The number of the box -> int.
        """
        self.box_num = box_num
        self.pos = None
        self.screen = screen
        self.closed_chest_img = None
        self.open_chest_img = None
        self.load_images()

    def load_images(self) -> None:
        """
        Loads the image resources needed for the BoxV object.\n
        """
        self.closed_chest_img = image.load(os.path.join('View/Resources/chest_closed.png'))

    def draw_box(self, box_index: int, increment: int, font: Font) -> tuple[int, int]:
        """
        Draws the box on the pygame surface.\n

        :param box_index: The index of the box -> int.
        :param increment: The increment value -> int.
        :param font: The font used to render the box index -> Font object.

        :return: A tuple containing the x and y coordinates of the box -> tuple of (x,y).
        """
        x = BOX_START_X + box_index * CELL_SIZE
        y = BOX_START_Y + increment * CELL_SIZE
        rect = Rect(x, y, CELL_SIZE, CELL_SIZE)
        text_surface = font.render(str(box_index + 1 + increment * MAX_BOX_WIDTH), True, YELLOW)
        text_rect = text_surface.get_rect()
        text_rect.center = self.closed_chest_img.get_rect().center
        self.closed_chest_img.blit(text_surface, text_rect)
        self.screen.blit(self.closed_chest_img, rect)
        return x, y

    def set_pos(self, new_pos:tuple[int, int]) -> None:
        """
        Method for setting new position of the box.\n
        :param new_pos: A tuple containing the x and y coordinates of the box -> tuple of (x,y).
        :return: None.
        """
        self.pos=new_pos

    def get_pos(self) -> tuple[int,int]:
        """
        Method for getting new position of the box.\n
        :return: A tuple containing the x and y coordinates of the box -> tuple of (x,y).
        """
        return self.pos
