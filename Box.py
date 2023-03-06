

class Box:

    def __init__(self,position,box_number,next_box):
        self.position=position
        self.img=None
        self.box_number=box_number
        self.next_box=next_box

    def get_position(self):
        return self.position

    def get_number(self):
        return self.box_number

    def get_next_box(self):
        return self.next_box

