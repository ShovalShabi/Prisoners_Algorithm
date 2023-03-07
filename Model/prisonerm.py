class PrisonerM:

    def __init__(self,num_prisoner,position,pace,all_boxes,trgt_box):
        self.prisoner_num=num_prisoner
        self.pos = position
        self.pace=pace
        self.visited_boxes=dict()  # key number box , value box
        self.all_boxes=all_boxes  # is a dict, key number box , value box
        self.trgt_box = trgt_box
        self.found_number=False
        self.updated_pos=False

    def set_pos(self, position):
        self.pos=position

    def get_pos(self):
        return self.pos

    def set_pace(self,pace):
        self.pace=pace

    def get_pace(self):
        return self.pace

    def get_num(self):
        return self.prisoner_num

    def is_still_searching(self):
        if self.trgt_box.get_pos()[0] == self.pos[0] and \
                self.trgt_box.get_pos()[1] == self.pos[1]:
            if self.trgt_box.get_nxt_box().get_num == self.prisoner_num:
                self.found_number = True
                print("got the number")
                return False
            if self.trgt_box.get_nxt_box().get_num in self.visited_boxes.keys():
                print("disqualified")
                return False
            else:
                print("searching")
                self.visited_boxes.update({self.trgt_box.get_num: self.trgt_box})
                self.trgt_box= self.trgt_box.get_nxt_box()
        return True

    def move_to_box(self,blocked):
        if self.trgt_box.get_pos()[1] < self.pos[1] and not self.updated_pos and not blocked:
            self.set_pos((self.pos[0], self.pos[1] - self.pace))  #moving upwards
            self.updated_pos = True
            self.updated_pos=True
        elif self.trgt_box.get_pos()[1] > self.pos[1] and not self.updated_pos and not blocked:  #moving downwards
            self.set_pos((self.pos[0], self.pos[1] + self.pace))
            self.updated_pos = True
        if self.trgt_box.get_pos()[0] < self.pos[0] and not self.updated_pos and not blocked:  #moving left
            self.set_pos((self.pos[0] - self.pace, self.pos[1]))
            self.updated_pos = True
        elif self.trgt_box.get_pos()[0] > self.pos[0] and not self.updated_pos and not blocked:  #moving right
            self.set_pos((self.pos[0] + self.pace, self.pos[1]))
            self.updated_pos = True
        self.updated_pos=False

    def check_collision(self,box_width,box_height):
        for box_number in self.all_boxes.keys():
            if self.pos[0] >= self.all_boxes[box_number].get_pos()[0] and self.pos[0] <= self.all_boxes[box_number].get_pos()[0] + box_width:  #collison on axis x
                self.move_to_box(blocked=True)
            if self.pos[1] >= self.all_boxes[box_number].get_pos()[1] and self.pos[1] <= self.all_boxes[box_number].get_pos()[1] + box_height:  #collison on axis y
                self.move_to_box(blocked=True)
            self.move_to_box(blocked=False)







