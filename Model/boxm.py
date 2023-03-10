

class BoxM:
    """
    A class representing a box in a game.\n

    Attributes:\n
    box_num: box number -> int.\n
    pos: the position of the box on screen-> tuple of (x,y).\n
    next_box: the pointer to the next target box -> BoxM object.\n
    """
    def __init__(self, box_num:int):
        """
        Initialize the PrisonerM object.
        :param box_num:int, the number of the box
        """
        self.box_num=box_num
        self.pos = None
        self.next_box=None

    def get_pos(self)->tuple:
        """
        Return position of the box image, tuple of (x,y) of pixels on screen
        :return:tuple, (x,y) of pixels.
        """
        return self.pos

    def set_pos(self,pos:tuple)->None:
        """
        Set position of the prisoner, tuple of (x,y) of pixels on screen.\n
        :return: None.
        """
        self.pos=pos

    def get_num(self)->int:
        """
        Return box number.
        :return: int
        """
        return self.box_num

    def set_next_box(self,box)->None:
        """
        Set next box pointer number.\n
        :return: int
        """
        self.next_box=box

    def get_nxt_box(self):
        """
        Return the next box pointer.
        :return: BoxM object, a representation of next box pointer
        """
        return self.next_box

