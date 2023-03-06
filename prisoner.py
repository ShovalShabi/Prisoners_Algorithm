from Prisoners_Algorithm.box import Box

import os
import pygame

class Prisoner:

    def __init__(self,num_prisoner,position,pace,all_boxes,trgt_box):
        self.prisoner_number=num_prisoner
        self.position = position
        self.pace=pace
        self.visited_boxes=dict()
        self.all_boxes=all_boxes  #will be a dict
        self.trgt_box = trgt_box
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
        if self.trgt_box.get_position()[0] == self.position[0] and \
                self.trgt_box.get_position()[1] == self.position[1]:
            if self.trgt_box.get_next_box().get_number == self.prisoner_number:
                self.found_number = True
                print("got the number")
                return False
            if self.trgt_box.get_next_box().get_number in self.visited_boxes.keys():
                print("disqualified")
                return False
            else:
                print("searching")
                self.visited_boxes.update({self.trgt_box.get_number: self.trgt_box})
                self.trgt_box=self.trgt_box.get_next_box()
        return True

    def move_to_box(self,blocked):
        if self.trgt_box.get_position()[1] < self.position[1] and not self.updated_pos and not blocked:
            self.set_position((self.position[0], self.position[1]- self.pace))  #moving upwards
            self.updated_pos = True
            self.updated_pos=True
        elif self.trgt_box.get_position()[1] > self.position[1] and not self.updated_pos and not blocked:  #moving downwards
            self.set_position((self.position[0], self.position[1]+ self.pace))
            self.updated_pos = True
        if self.trgt_box.get_position()[0] < self.position[0] and not self.updated_pos and not blocked:  #moving left
            self.set_position((self.position[0] - self.pace, self.position[1]))
            self.updated_pos = True
        elif self.trgt_box.get_position()[0] > self.position[0] and not self.updated_pos and not blocked:  #moving right
            self.set_position((self.position[0] + self.pace,self.position[1]))
            self.updated_pos = True
        self.is_still_searching()
        self.updated_pos=False

    def check_collision(self,box_width,box_height):
        for box_number in self.all_boxes.keys():
            if self.position[0] >= self.all_boxes[box_number].get_position()[0] and self.position[0] <= self.all_boxes[box_number].get_position()[0] + box_width:  #collison on axis x
                self.move_to_box(blocked=True)
            if self.position[1] >= self.all_boxes[box_number].get_position()[1] and self.position[1] <= self.all_boxes[box_number].get_position()[1] + box_height:  #collison on axis y
                self.move_to_box(blocked=True)
            self.move_to_box(blocked=False)







