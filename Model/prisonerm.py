from time import time
from Model.boxm import BoxM
from View.settings import EXIT_POINT


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
    all_prisoners:int, represents the number of all prisoners.\n
    on_exit: bool, indicator if the prisoner is on it's to exit point.\n
    time_start: time object, a time measurement tool for measuring each box interval, start point.
    time_start: time object, a time measurement tool for measuring each box interval, end point.
    """

    def __init__(self, num_prisoner: int, position: tuple, pace: int, all_boxes: dict, target_box: BoxM,all_prisoners:int):
        """
        Initialize the PrisonerM object.\n
        :param num_prisoner: int , represents prisoner number.
        :param position: tuple of (x,y) according to place of.
        :param pace:int , pace of the prisoner on the screen.
        :param all_boxes:dict, dictionary of BoxM objects located on screen.
        :param target_box:BoxM object, represents the target box.
        :param all_prisoners:int, represents the number of all prisoners.
        """
        self.prisoner_num = num_prisoner
        self.pos = position
        self.pace = pace
        self.visited_boxes = dict()  # dictionary of {number box:value box}
        self.all_boxes = all_boxes  # dictionary of {number box:value box}
        self.target_box = target_box
        self.found_number = False
        self.updated_pos = False
        self.total_pris_count=all_prisoners
        self.on_exit = False
        self.time = 0.0
        self.time_interval = 0.0

    def set_pos(self, position: tuple[int,int]) -> None:
        """
        Set position of the prisoner, tuple of (x,y) of pixels on screen.\n
        :return: None.
        """
        self.pos = position

    def get_pos(self) -> tuple:
        """
        Return position of the prisoner image, tuple of (x,y) of pixels on screen.\n
        :return: tuple, position tuple of (x,y) in form -> tuple[int,int].
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

    def is_still_searching(self) -> (bool,int):
        """
        This method check if the prisoner is still searching his target box, and replaces it if there is a need.\n
        As long the prisoner is still searching for his number the output of this function will be True otherwise
        if the prisoner got disqualified or won the game, the function will return False.\n
        :return: tuple of (bool,int),the left hand is indication of relevance of the participant the right hand is the current box number.
        """
        if self.target_box.get_pos()[0] == self.pos[0] and \
                self.target_box.get_pos()[1] == self.pos[1]:

            self.measure_time()  #Measuring the time which the prisoner to get to the box

            self.visited_boxes.update({self.target_box.get_num(): self.target_box})  #Updating the visited dictionary boxes with the new box which the prisoner got to
            temp_box_num = self.target_box.get_num()

            if self.on_exit:
                self.found_number= True
                return False, self.prisoner_num

            if self.target_box.get_nxt_box().get_num() == self.prisoner_num and len(self.visited_boxes) <= self.total_pris_count//2:
                self.on_exit = True
                fake_box=BoxM(-1)
                fake_box.set_pos(EXIT_POINT)
                self.target_box=fake_box
                print(f"Prisoner number {self.prisoner_num} found his number at box number {temp_box_num} at {self.target_box.pos}")
                return True,temp_box_num
            if self.target_box.get_nxt_box().get_num() in self.visited_boxes.keys():
                print(f"Prisoner number {self.prisoner_num} got disqualified!")
                return False,self.target_box.get_num()
            else:
                print(f"Prisoner number {self.prisoner_num} visited box number {self.target_box.box_num}")
                self.target_box = self.target_box.get_nxt_box()
                return True, temp_box_num
        return True,self.target_box.get_num()

    def move_to_box(self, blocked: bool) -> None:
        """
        This method check if a prisoner is blocked, it receives a boolean variable that tells if the prisoner is blocked or not.\n
        :param: blocked: bool, indication if the prisoner is blocked (checked by method check_collision within PrisonerM).
        :return: bool, is the object moving or not.
        """
        if self.target_box.get_pos()[1] < self.pos[1] and not self.updated_pos and not blocked:  # moving upwards
            self.set_pos((self.pos[0], self.pos[1] - self.pace))
            self.updated_pos = True
        elif self.target_box.get_pos()[1] > self.pos[1] and not self.updated_pos and not blocked:  # moving downwards
            self.set_pos((self.pos[0], self.pos[1] + self.pace))
            self.updated_pos = True
        if self.target_box.get_pos()[0] < self.pos[0] and not self.updated_pos and not blocked:  # moving left
            self.set_pos((self.pos[0] - self.pace, self.pos[1]))
            self.updated_pos = True
        elif self.target_box.get_pos()[0] > self.pos[0] and not self.updated_pos and not blocked:  # moving right
            self.set_pos((self.pos[0] + self.pace, self.pos[1]))
            self.updated_pos = True
        self.updated_pos = False

    def navigate(self, box_width: int, box_height: int, pris_width:int, pris_height:int) -> None:
        """
        This function swipe all box positions on screen, and check if the prisoner is about to collide box image on screen.\n
        :param box_width: int, represents a box width of an image.
        :param box_height: int, represents a box height of an image.
        :param pris_width: int, represents a prisoner width of an image.
        :param pris_height: int, represents a prisoner height of an image.
        :return: None.
        """
        for box_number in self.all_boxes.keys():
            if not self.all_boxes[box_number].get_pos():
                continue  # There are might more boxes on screen up ahead
            if self.all_boxes[box_number].get_pos()[0] <= self.pos[0] + pris_width <= self.all_boxes[box_number].get_pos()[0] + box_width:  # collision on axis x
                self.move_to_box(blocked=True)
            if self.all_boxes[box_number].get_pos()[1] <= self.pos[1] and self.pos[1]+pris_height <= self.all_boxes[box_number].get_pos()[1] + box_height:  # collision on axis y
                self.move_to_box(blocked=True)
        self.move_to_box(blocked=False)

    def measure_time(self) -> None:
        """
        This method measure the timr that took the prisoner to get to the box in milliseconds, each arrival to box is measured,
        and the current time which the prisoner got to the box is updated.
        :return: None.
        """
        current_time=time()
        self.time_interval = current_time - self.time
        if self.time == 0.0:
            self.time_interval%=9  #Considering only two digits after decimal, only at the first calculation
        self.time = current_time
