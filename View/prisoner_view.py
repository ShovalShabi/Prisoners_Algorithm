import pygame.transform
from pygame.font import Font
from pygame import Surface
from View.settings import *


class PrisonerV:
    """
    Representation of the PrisonerM object by actual images for the user.\n

    Attributes:\n
    pos: the position tuple of (x,y) in form -> tuple[int,int].\n
    pris_num: the number of the prisoner.\n
    screen: object that blitting the box image on screen.\n to the next target box -> Surface object.\n
    img: image of the prisoner -> Surface object.\n
    img_prisoner: transformed image of the prisoner o better dimensions -> Surface object.\n
    """
    def __init__(self, start_pos: tuple[int, int], num: int, screen: Surface) -> None:
        """
        Initializes a PrisonerV object.

        :param start_pos: A tuple containing the x and y coordinates of the starting location of the prisoner.
        :param num: The number of the prisoner.
        :param screen: The pygame surface to draw the prisoner on.
        """
        self.pos = start_pos
        self.pris_num = num
        self.img = pygame.image.load(os.path.join('View/Resources', 'SP1_front.png')).convert_alpha()
        self.img_prisoner = pygame.transform.scale(self.img, (self.img.get_width() + 10, self.img.get_height() + 20))

        self.screen = screen

    def draw_prisoner(self, font: Font) -> None:
        """
        Draws the prisoner on the pygame surface.\n

        :param font: Font object.
        :return: None.
        """
        text_surface = font.render(str(self.pris_num), True, BLACK)
        text_rect = NUMBER_POSITION_ON_PRIS
        self.img_prisoner.blit(text_surface, text_rect)
        self.screen.blit(self.img_prisoner, self.pos)

    def rotate_prisoner(self) -> None:
        """
        Method that rotate the prisoner on the screen.\n
        """
        pass

    def set_pris_pos(self, pos: tuple[int, int]) -> None:
        """
        Updates the position of the prisoner.\n

        :param pos: A tuple containing the x and y coordinates of the new location of the prisoner -> tuple (x,y).
        :return: None.
        """
        self.pos = pos

    def get_pris_pos(self) -> tuple[int, int]:
        """
        Returns the position of the prisoner.\n

        :return: A tuple containing the x and y coordinates of the prisoner -> tuple (x,y).
        """
        return self.pos
