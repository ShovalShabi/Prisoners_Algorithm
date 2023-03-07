

class Box:

    def __init__(self, pos, box_num):
        self.pos=pos
        self.box_num=box_num
        self.next_box=None

    def get_pos(self):
        return self.pos

    def set_pos(self,pos):
        self.pos=pos

    def get_num(self):
        return self.box_num

    def set_next_box(self,box):
        self.next_box=box

    def get_nxt_box(self):
        return self.next_box

