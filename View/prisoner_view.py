import pygame
import os
from typing import Tuple


class PrisonerV:
    def __init__(self, start_location: Tuple[int, int], num: int, screen: pygame.Surface) -> None:
        """
        Initializes a PrisonerV object.

        :param start_location: A tuple containing the x and y coordinates of the starting location of the prisoner.
        :param num: The number of the prisoner.
        :param screen: The pygame surface to draw the prisoner on.
        """
        self.location = start_location
        self.num = num
        self.img_prisoner = pygame.image.load(os.path.join('Resources', 'SP1_front.png'))
        self.screen = screen

    def draw_prisoner(self, location: Tuple[int, int]) -> None:
        """
        Draws the prisoner on the pygame surface.

        :param location: A tuple containing the x and y coordinates of the location to draw the prisoner at.
        """
        self.screen.blit(self.img_prisoner, location)

    def rotate_prisoner(self) -> None:
        """
        Rotates the prisoner.
        """
        pass

    def update_prisoner_location(self, location: Tuple[int, int]) -> None:
        """
        Updates the location of the prisoner.

        :param location: A tuple containing the x and y coordinates of the new location of the prisoner.
        """
        self.location = location

    def get_prisoner_location(self) -> Tuple[int, int]:
        """
        Returns the location of the prisoner.

        :returns: A tuple containing the x and y coordinates of the prisoner.
        """
        return self.location
