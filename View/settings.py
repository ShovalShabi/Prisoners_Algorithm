import pygame
import os

# Color
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
PURPLE = (255, 0, 255)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# SCREEN & BUTTONS
screen_width = 1100
screen_height = 750
floor_width = screen_width - 275
floor_height = screen_height - 137
button_width = 100
button_height = 50
BUTTON_COLOR = WHITE
button_x = 38
button_y = 550

# FONT
FONT_SIZE = 20

# PRISONER
NUMBER_POSITION_ON_PRIS_ABOVE_9 = (13, 35)
NUMBER_POSITION_ON_PRIS_BELOW_9 = (20, 35)

# BOX
CELL_SIZE = 80
MAX_BOX_WIDTH = 10
MAX_NO_PRISONER_BOX = 80
MAX_NO_ROUND = 100
MAX_NO_PRIS = 200
DOOR_WAY = (120, 400)
EXIT_POINT = (940, 460)
BOX_START_X = 150
BOX_START_Y = 80

# IMAGES BOX
IMG_BOX = pygame.image.load(os.path.join('View/Resources', 'chest_closed.png'))
IMG_BOX_WIDTH = IMG_BOX.get_width()
IMG_BOX_HEIGHT = IMG_BOX.get_height()

# IMAGES' PRISONERS
IMG_SP1_F = pygame.image.load(os.path.join('View/Resources', 'SP1_front.png'))
IMG_SP2_F = pygame.image.load(os.path.join('View/Resources', 'SP2_front.png'))
IMG_SP3_F = pygame.image.load(os.path.join('View/Resources', 'SP3_front.png'))
IMG_SP4_F = pygame.image.load(os.path.join('View/Resources', 'SP4_front.png'))
IMG_FP1_F = pygame.image.load(os.path.join('View/Resources', 'FP1_front.png'))
IMG_FP2_F = pygame.image.load(os.path.join('View/Resources', 'FP2_front.png'))

# IMAGE BACKGROUND
IMG_BACKGROUND = pygame.image.load(os.path.join('View/Resources', 'Lunatic_Room.jpg'))
IMG_FLOOR = pygame.image.load(os.path.join('View/Resources', 'floor.jpg'))

# SOUNDS
pygame.mixer.init()
OPEN_CHEST_SOUND = pygame.mixer.Sound(os.path.join('View/Resources', 'open_chest_sound.mp3'))
SUCCESS_SOUND = pygame.mixer.Sound(os.path.join('View/Resources', 'success_sound.mp3'))
SUCCESS_SOUND.set_volume(0.2)
FAILURE_SOUND = pygame.mixer.Sound(os.path.join('View/Resources', 'failure_sound.mp3'))
# FAILURE_SOUND.set_volume(0.2)

# USER GUIDE TEXT
USER_GUIDE = 'USER GUIDE:\n' + \
             '---------------------------------------' + \
             '\n\n' + 'LEFT ARROW: Select prisoner text input' + \
             '\n' + 'RIGHT ARROW: Select specify print check box' + \
             '\n' + 'X - Select/Unselect check box' + '\n\n' + \
             '---------------------------------------' + \
             '\n' + 'Press START to run the game after' + '\n' + \
             '---------------------------------------' + \
             '\n' + 'Press PROBS to view the game statistics' + '\n' + \
             '---------------------------------------' + \
             '\n' + 'Press RESET to clear the screen'

# FRAME CLOCK RATE
FRAME_RATE = 25
WAIT_FRAME_RATE = 1
