import pygame.transform
from pygame.font import Font
from View.settings import *


class PrisonerV:
    def __init__(self, start_location: tuple[int, int], num: int, screen: pygame.Surface) -> None:
        """
        Initializes a PrisonerV object.

        :param start_location: A tuple containing the x and y coordinates of the starting location of the prisoner.
        :param num: The number of the prisoner.
        :param screen: The pygame surface to draw the prisoner on.
        """
        self.location = start_location
        self.num = num
        self.image = pygame.image.load(os.path.join('View/Resources', 'SP1_front.png')).convert_alpha()
        self.img_prisoner = pygame.transform.scale(self.image, (self.image.get_width()+10, self.image.get_height()+20))

        self.screen = screen

    def draw_prisoner(self, font: Font) -> None:
        """
        Draws the prisoner on the pygame surface.
        """
        text_surface = font.render(str(self.num), True, BLACK)
        text_rect = NUMBER_POSITION_ON_PRIS
        self.img_prisoner.blit(text_surface, text_rect)
        self.screen.blit(self.img_prisoner, self.location)

    def rotate_prisoner(self) -> None:
        """
        Rotates the prisoner.
        """
        pass

    def update_prisoner_location(self, location: tuple[int, int]) -> None:
        """
        Updates the location of the prisoner.

        :param location: A tuple containing the x and y coordinates of the new location of the prisoner.
        """
        self.location = location

    def get_prisoner_location(self) -> tuple[int, int]:
        """
        Returns the location of the prisoner.

        :returns: A tuple containing the x and y coordinates of the prisoner.
        """
        return self.location
