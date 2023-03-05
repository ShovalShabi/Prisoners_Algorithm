from threading import Thread

class Prisoner(Thread):

    def __init__(self, num_inmate):
        super().__init__()
        self.images=[]
        self.pos_x=0
        self.pos_y=0
        self.number_inmate=num_inmate

    def walk_to_box(self):
        #moving physically to box
        pass

    def movement(self):
        #animating the movement of the prisoner by sprite sheet
        pass

    def is_reached_box(self,target_box):
        #checking if the prisoners reached the box
        pass

