

class Box:

    def __init__(self,position,box_number):
        self.position=position
        self.box_number=box_number
        self.next_box=None

    def get_position(self):
        return self.position

    def get_number(self):
        return self.box_number

    def set_next_box(self,box):
        self.next_box=box

    def get_next_box(self):
        return self.next_box

