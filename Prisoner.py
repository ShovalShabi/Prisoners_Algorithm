from Prisoners_Algorithm.Box import Box

import os
import pygame

class Prisoner:

    def __init__(self,box_number,trgt_pos,num_prisoner,position,pace):
        self.prisoner_number=num_prisoner
        self.trgt_box_number=box_number
        self.trgt_pos=trgt_pos
        self.position = position
        self.pace=pace
        self.visited_boxes={int:Box}
        self.found_number=False
        self.updated_pos=False

    def set_position(self,position):
        self.position=position

    def get_position(self):
        return self.position

    def set_pace(self,pace):
        self.pace=pace

    def get_pace(self):
        return self.pace

    def get_number(self):
        return self.prisoner_number

    def is_still_searching(self):
        if self.trgt_pos.get_position[0] == self.position[0] and \
                self.trgt_pos.get_position[1] == self.position[1]:
            if self.trgt_pos.get_nextbox.get_number == self.prisoner_number:
                self.found_number = True
                return False
            if self.trgt_box.get_nextbox.get_number in self.visited_boxes.keys():
                return False
            else:
                self.visited_boxes.update({self.trgt_pos.get_number: self.trgt_pos})
                self.trgt_box = self.trgt_pos.get_nextbox
        return True

    def move_to_box(self):
        if self.trgt_box.get_position[1] < self.position[1] and not self.updated_pos:
            self.set_position((self.position[0], self.position[1]- self.pace))  #moving upwards
            self.updated_pos = True
            self.updated_pos=True
        elif self.trgt_box.get_position[1] > self.position[1] and not self.updated_pos:  #moving downwards
            self.set_position((self.position[0], self.position[1]+ self.pace))
            self.updated_pos = True
        if self.trgt_box.get_position[0] < self.position[0] and not self.updated_pos:  #moving left
            self.set_position((self.position[0] - self.pace, self.position[1]))
            self.updated_pos = True
        elif self.trgt_box.get_position[0] > self.position[0] and not self.updated_pos:  #moving right
            self.set_position((self.position[0] + self.pace,self.position[1]))
            self.updated_pos = True
        self.updated_pos=False

    def run(self):
        while not self.is_still_searching():
            self.move_to_box()



