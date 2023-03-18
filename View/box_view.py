from View.settings import *
from pygame import Surface, image, Rect
from pygame.font import SysFont
import os


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
        self.text_surface = None
        self.box_num = box_num
        self.print_num = self.box_num
        self.pos = None
        self.screen = screen
        self.chest_img = None
        self.load_images('chest_closed.png')
        self.color_num = YELLOW

    def clear_image(self, next_num):
        self.print_num = next_num
        self.text_surface = None

    def close_box(self, num):
        self.print_num = num
        self.replace_box_image('chest_closed.png', YELLOW)

    def replace_box_image(self, new_name_img, color) -> None:
        self.load_images(new_name_img)
        self.color_num = color
        self.draw_box()

    def load_images(self, new_name_img) -> None:
        """
        Loads the image resources needed for the BoxV object.\n
        """
        self.chest_img = image.load(os.path.join('View/Resources/' + new_name_img))

    def draw_box(self):
        font = SysFont('monospace', FONT_SIZE, bold=True)
        rect = Rect(self.pos[0], self.pos[1], CELL_SIZE, CELL_SIZE)
        self.text_surface = font.render(str(self.print_num), True, self.color_num)
        text_rect = self.text_surface.get_rect()
        text_rect.center = self.chest_img.get_rect().center
        self.chest_img.blit(self.text_surface, text_rect)
        self.screen.blit(self.chest_img, rect)

    def set_pos(self, new_pos: tuple[int, int]) -> None:
        """
        Method for setting new position of the box.\n
        :param new_pos: A tuple containing the x and y coordinates of the box -> tuple of (x,y).
        :return: None.
        """
        self.pos = new_pos

    def get_pos(self) -> tuple[int, int]:
        """
        Method for getting new position of the box.\n
        :return: A tuple containing the x and y coordinates of the box -> tuple of (x,y).
        """
        return self.pos
