from threading import Thread
from Prisoners_Algorithm.Box import Box


class Prisoner(Thread):

    def __init__(self, num_prisoner,box):
        super().__init__()
        self.images=[]
        self.pos_x=0
        self.pos_y=0
        self.prisoner_number=num_prisoner
        self.trgt_box=box
        self.visited_boxes={int:Box}
        self.number_found=False

    def walk_to_box(self,box):
        #moving physically to box
        pass

    def movement(self):
        #animating the movement of the prisoner by sprite sheet
        pass

    def is_reached_box(self):
        if self.trgt_box.number_box == self.prisoner_number:
            self.number_found=True

    def run(self):
        while not self.number_found:
            self.walk_to_box()



