from Model.boxm import BoxM


class PrisonerM:
    """
    A class representing a prisoner in a game.\n

    Attributes:

    prisoner_num: prisoner number -> int.\n
    pos: the position of the prisoner on screen -> tuple of (x,y).\n
    pace: the pace of the prisoner, int.\n
    visited_boxes: all the boxes that the prisoner has opened, dictionary of {box number: value box}.\n
    all_boxes: all the boxes located on screen-> dictionary of {box number:value box}.\n
    trgt_box: the current target box of the prisoner -> BoxM object.\n
    found_number: indicator if the prisoner has found his number -> bool.\n
    updated_pos: flag the represents if the prisoner has been changed position -> bool.
    """

    def __init__(self, num_prisoner: int, position: tuple, pace: int, all_boxes: dict, trgt_box: BoxM):
        """
        Initialize the PrisonerM object.\n
        :param num_prisoner: int , represents prisoner number.
        :param position: tuple of (x,y) according to place of.
        :param pace:int , pace of the prisoner on the screen.
        :param all_boxes:dict, dictionary of BoxM objects located on screen.
        :param trgt_box:BoxM object, represents the target box.
        """
        self.prisoner_num = num_prisoner
        self.pos = position
        self.pace = pace
        self.visited_boxes = dict()  # dictionary of {number box:value box}
        self.all_boxes = all_boxes  # dictionary of {number box:value box}
        self.trgt_box = trgt_box
        self.found_number = False
        self.updated_pos = False

    def set_pos(self, position: tuple) -> None:
        """
        Set position of the prisoner, tuple of (x,y) of pixels on screen.\n
        :return: None.
        """
        self.pos = position

    def get_pos(self) -> tuple:
        """
        Return position of the prisoner image, tuple of (x,y) of pixels on screen.\n
        :return: tuple, (x,y) of pixels.
        """
        return self.pos

    def set_pace(self, pace: int) -> None:
        """
        Set pace of the prisoner.\n
        :return: None.
        """
        self.pace = pace

    def get_pace(self) -> int:
        """
        Return prisoner number.\n
        :return: int.
        """
        return self.pace

    def get_num(self) -> int:
        """
        Return prisoner number.\n
        :return: int.
        """
        return self.prisoner_num

    def is_still_searching(self) -> bool:
        """
        This function check if the prisoner is still searching his target box, and replaces it if there is a need.\n
        As long the prisoner is still searching for his number the output of this function will be True otherwise
        if the prisoner got disqualified or won the game, the function will return False.\n
        :return: bool, indication of relevance participant.
        """
        if self.trgt_box.get_pos()[0] == self.pos[0] and \
                self.trgt_box.get_pos()[1] == self.pos[1]:
            if self.trgt_box.get_nxt_box().get_num() == self.prisoner_num:
                self.found_number = True
                print(f"Prisoner number {self.prisoner_num} found his number at box number {self.trgt_box.box_num} at {self.trgt_box.pos}")
                return False
            if self.trgt_box.get_nxt_box().get_num() in self.visited_boxes.keys():
                print(f"Prisoner number {self.prisoner_num} got disqualified!")
                return False
            else:
                print(f"Prisoner number {self.prisoner_num} going to box number {self.trgt_box.box_num}")
                self.visited_boxes.update({self.trgt_box.get_num: self.trgt_box})
                self.trgt_box = self.trgt_box.get_nxt_box()
        return True

    def move_to_box(self, blocked: bool):
        """
        This function check if a prisoner is blocked, it receives a boolean variable that tells if the prisoner is blocked or not.\n
        :param: blocked: bool, indication if the prisoner is blocked (checked by method check_collision within PrisonerM).
        :return: bool, is the object moving or not.
        """
        if self.trgt_box.get_pos()[1] < self.pos[1] and not self.updated_pos and not blocked:
            self.set_pos((self.pos[0], self.pos[1] - self.pace))  # moving upwards
            self.updated_pos = True
            self.updated_pos = True
        elif self.trgt_box.get_pos()[1] > self.pos[1] and not self.updated_pos and not blocked:  # moving downwards
            self.set_pos((self.pos[0], self.pos[1] + self.pace))
            self.updated_pos = True
        if self.trgt_box.get_pos()[0] < self.pos[0] and not self.updated_pos and not blocked:  # moving left
            self.set_pos((self.pos[0] - self.pace, self.pos[1]))
            self.updated_pos = True
        elif self.trgt_box.get_pos()[0] > self.pos[0] and not self.updated_pos and not blocked:  # moving right
            self.set_pos((self.pos[0] + self.pace, self.pos[1]))
            self.updated_pos = True
        self.updated_pos = False

    def navigate(self, box_width: int, box_height: int) -> None:
        """
        This function swipe all box positions on screen, and check if the prisoner is about to collide box image on screen.\n
        :param box_width: int, represents a box width of an image.
        :param box_height: int, represents a box height of an image.
        :return: None.
        """
        for box_number in self.all_boxes.keys():
            if self.pos[0] >= self.all_boxes[box_number].get_pos()[0] and self.pos[0] <= self.all_boxes[box_number].get_pos()[0] + box_width:  # collision on axis x
                self.move_to_box(blocked=True)
            if self.pos[1] >= self.all_boxes[box_number].get_pos()[1] and self.pos[1] <= self.all_boxes[box_number].get_pos()[1] + box_height:  # collision on axis y
                self.move_to_box(blocked=True)
        self.move_to_box(blocked=False)
