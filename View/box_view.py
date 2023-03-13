from View.settings import *
from pygame import Surface, image, Rect
from pygame.font import Font
import os

from View.settings import MAX_BOX_WIDTH


class BoxV:
    def __init__(self, screen: Surface, box_number: int) -> None:
        """
        Initializes a BoxV object.

        :param screen: The pygame surface to draw the box on.
        :param box_number: The number of the box.
        """
        self.box_number = box_number
        self.next_box_number = -1
        self.screen = screen
        self.location = None
        self.closed_chest_image = None
        self.load_images()

    def load_images(self) -> None:
        """
        Loads the image resources needed for the BoxV object.
        """
        self.closed_chest_image = image.load(os.path.join('View/Resources/chest_closed.png'))

    def draw_box(self, box_index: int, increment: int, font: Font) -> tuple[int, int]:
        """
        Draws the box on the pygame surface.

        :param box_index: The index of the box.
        :param increment: The increment value.
        :param font: The font used to render the box index.

        :returns: A tuple containing the x and y coordinates of the box.
        """
        x = BOX_START_X + box_index * CELL_SIZE
        y = BOX_START_Y + increment * CELL_SIZE
        rect = Rect(x, y, CELL_SIZE, CELL_SIZE)
        text_surface = font.render(str(box_index + 1 + increment * MAX_BOX_WIDTH), True, YELLOW)
        text_rect = text_surface.get_rect()
        text_rect.center = self.closed_chest_image.get_rect().center
        self.closed_chest_image.blit(text_surface, text_rect)
        self.screen.blit(self.closed_chest_image, rect)
        return x, y

    def replace_box(self) -> None:
        """
        Replaces the current box with the next one.
        """
        pass
