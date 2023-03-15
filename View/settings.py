import pygame
import os

# Color
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
PURPLE = (255, 0, 255)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

# Screen and button
screen_width = 1100
screen_height = 850
button_width = 100
button_height = 50
BUTTON_COLOR = WHITE
button_x = 50
button_y = 770

# FONT
FONT_SIZE = 20


# PRISONER
NUMBER_POSITION_ON_PRIS_ABOVE_9 = (13, 35)
NUMBER_POSITION_ON_PRIS_BELOW_9 = (20, 35)

# BOX
CELL_SIZE = 80
MAX_BOX_WIDTH = 10
MAX_NO_PRISONER_BOX = 90
MAX_NO_ROUND = 10000
DOOR_WAY = (120, 400)
BOX_START_X = 150
BOX_START_Y = 80

IMG_BOX = pygame.image.load(os.path.join('View/Resources', 'chest_closed.png'))
IMG_PRIS = pygame.image.load(os.path.join('View/Resources', 'SP1_front.png'))
IMG_BOX_WIDTH = IMG_BOX.get_width()
IMG_BOX_HEIGHT = IMG_BOX.get_height()

IMG_BACKGROUND = pygame.image.load(os.path.join('View/Resources', 'Lunetic_Room.jpg'))
