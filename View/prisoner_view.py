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
    img_prisoner: transformed image of the prisoner o better dimensions -> Surface object.\n
    """

    def __init__(self, start_pos: tuple[int, int], num: int, screen: Surface, image: Surface) -> None:
        """
        Initializes a PrisonerV object.
        """
        self.pos = start_pos
        self.pris_num = num
        self.img_prisoner = pygame.transform.scale(image, (image.get_width() + 27, image.get_height() + 25))
        self.screen = screen

    def draw_prisoner(self, font: Font) -> None:
        """
        Draw prisoner on view.

        :param font: The font for the prisoner number.\n

        :return: None
        """
        text_surface = font.render(str(self.pris_num), True, BLACK)
        if self.pris_num > 9:
            text_rect = NUMBER_POSITION_ON_PRIS_ABOVE_9
        else:
            text_rect = NUMBER_POSITION_ON_PRIS_BELOW_9

        self.img_prisoner.blit(text_surface, text_rect)
        self.screen.blit(self.img_prisoner, self.pos)

    def set_pris_pos(self, pos: tuple[int, int]) -> None:
        """
        Set position of the prisoner.

        :param pos: The position of the prisoner.\n

        :return: None
        """
        self.pos = pos

    def get_pris_pos(self) -> tuple[int, int]:
        """
        Return position of the prisoner.

        :return: the position's prisoner -> tuple
        """
        return self.pos