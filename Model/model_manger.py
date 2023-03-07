import random

from copy import deepcopy
from threading import Lock
from threading import Thread
from Prisoners_Algorithm.Model.boxm import BoxM
from Prisoners_Algorithm.Model.prisonerm import PrisonerM


class ModelManger:
    filename= "PrisonersResults.txt"
    file=None
    lock_shuffle=Lock()

    def __init__(self,num_prisoners,num_rounds,listener):
        self.dict_rounds={}  #dict of {round_num:list dependencies of boxes}
        self.dict_prisoners={}   #dict of {num_pris:prisoner}
        self.dict_boxes= {}  #dict of {num_box:box}
        self.listener=listener
        self.num_prisoners=num_prisoners
        self.num_rounds= num_rounds
        self.current_round = 1
        self.current_prisoner = 1
        self.succeeded=0

    ############# listener ######################

    def ntfy_pris_pos(self):
        self.listener.ntfy_view_pris_pos(self.dict_prisoners[self.current_prisoner].get_pos())

    def ntfy_pris_need_box(self):
        self.listener.notify_model_need_box(self.dict_prisoners[self.current_prisoner].trgt_box.box_num)

    def ntfy_pris_changed(self):
        self.listener.ntfy_pris_changed(self.current_prisoner.get_num())

    def ntfy_model_need_boxes_pos(self):
        return self.listener.ntfy_model_need_boxes_pos()  #will return dict of {num_box:position}

    ######################

    def init_boxes(self):
        for index_box in range(self.num_prisoners):
            box=BoxM(box_num=index_box + 1)
            self.dict_boxes[index_box+1]=box
        for box_num in self.dict_boxes.keys():  #box num starts from 1 to n+1
            self.dict_boxes[box_num].set_nxt_box=self.dict_boxes[self.dict_rounds[self.current_round][box_num-1]]  #redirecting each box to current next box
        self.set_all_boxes_pos()

    def set_all_boxes_pos(self):
        positions = self.ntfy_model_need_boxes_pos()
        for box_num in self.dict_boxes.keys():
            self.dict_boxes[box_num].set_pos = positions[box_num]

    def init_prisoners(self):
        for index_pris in range(self.num_prisoners):
            self.dict_prisoners[index_pris+1]=PrisonerM(num_prisoner=index_pris + 1, position=(0, 0), pace=5, all_boxes=self.dict_rounds[self.current_round], trgt_box=self.dict_boxes[index_pris + 1])

    def run_game(self):
        while self.current_round < self.num_rounds:

            if self.current_prisoner > self.num_prisoners:
                self.current_prisoner=1
                self.current_round+=1
                if self.current_round > self.num_rounds:
                    return
                else:
                    self.current_round+=1

            self.init_boxes()
            self.init_prisoners()

            while self.dict_prisoners[self.current_prisoner].is_still_searching():
                self.ntfy_pris_need_box()
                self.dict_prisoners[self.current_prisoner].move_to_box()
                self.ntfy_pris_pos()
            self.current_prisoner+=1

    def run_route(self,list_of_boxes, print_route):
        number_of_boxes = len(list_of_boxes)
        list_of_success = number_of_boxes * [0]
        for j in range(number_of_boxes):
            if print_route:
                print("Iteration number", j + 1,file=self.file)
            visited_boxes = []
            pointer_box = list_of_boxes[j]
            visited_boxes.append(pointer_box)
            for attempts in range(number_of_boxes):
                success = False
                if print_route:
                    print("Attempt:", attempts + 1, " is leading to box", pointer_box + 1,file=self.file)
                if pointer_box == j and attempts < (number_of_boxes // 2):
                    success = True
                    list_of_success[j] = 1
                    break
                else:
                    if pointer_box == j:
                        break
                    else:
                        pointer_box = list_of_boxes[pointer_box]
                        visited_boxes.append(pointer_box)
            if print_route:
                print("Total Boxes:", end=" ",file=self.file)
                for o in range(number_of_boxes):
                    print(list_of_boxes[o]+1, end=" ",file=self.file)
                print(file=self.file)
                print("Visited in boxes:", end=" ",file=self.file)
                for g in range(len(visited_boxes)):
                    print(visited_boxes[g]+1, end=" ",file=self.file)
                print(file=self.file)
                if success:
                    print("Prisoner number", j + 1, "has been succeeded,",
                          "the chain length is", (attempts + 1),file=self.file)
                else:
                    print("Prisoner number", j + 1, "has been failed,",
                          "the chain length is", (attempts + 1),file=self.file)
                print(file=self.file)
        if print_route:
            print("The number of prisoners that found their number is:",
                  sum(list_of_success), "\nfrom", number_of_boxes, "prisoners.\n",file=self.file)
        if sum(list_of_success) == number_of_boxes:
            return True
        else:
            return False

    def run_all_rounds(self,print_route):
        self.open_file()
        if not isinstance(self.num_prisoners, int):
            print("The number of prisoners is ", self.num_prisoners, " the number of prisoners must be an integer.",file=self.file)
            return
        if self.num_prisoners < 2:
            print("The number of prisoners is ", self.num_prisoners, " the number of prisoners must be greater than 1.",file=self.file)
            return
        if not isinstance(self.num_rounds, int):
            print("The number of rounds is ", self.num_rounds, " rounds must be an integer.",file=self.file)
            return
        if self.num_rounds <= 0:
            print("The number of rounds is ", self.num_rounds, " rounds must be greater 0.",file=self.file)
        s = 0
        general_lists={} ## {round:list dependencies}
        for i in range(self.num_rounds):
            if print_route:
                print("round number:", (i + 1),file=self.file)
            list_of_boxes = self.num_prisoners * [0]
            for j in range(self.num_prisoners):
                list_of_boxes[j] = j  #naming boxes from 1 to n+1

            self.lock_shuffle.acquire()  #lock shuffling list area
            random.shuffle(list_of_boxes)
            general_lists[i+1]=list_of_boxes  #### need to fix the pointing value of each box to another from 1 to n+1
            self.lock_shuffle.release()  #release shuffling list area
            if i+1 not in self.dict_rounds.keys():
                self.dict_rounds[i+1]=deepcopy(general_lists[i+1])  #matching dependencies of each box to another for each round
            if self.run_route(general_lists[i+1], print_route): ## fix this for one calculation
                s += 1
            self.dict_rounds[i+1]=[box_i+1 for box_i in self.dict_rounds[i+1]] ## making renumbering boxes from 1 to n+1

        print("The number of prisoners is", self.num_prisoners, ",the number of rounds is", self.num_rounds, ",s = ", s,
              "\ns / k in % =", 100 * (s / self.num_rounds),file=self.file)
        s = 0
        hn = self.num_prisoners / 2
        for i in range(self.num_prisoners // 2):
            s += 1 / ((hn) + (i + 1))
        print("Probability by loop calculation of the geometric series:\n",
              "1 - (1/((n/2)+1) + 1/((n/2)+2) + ...) =", 1 - s,file=self.file)
        self.close_file()

    def open_file(self):
        self.file=open(self.filename,"w")

    def close_file(self):
        self.file.close()

    def run_threads(self):
        threads=[]
        for i in range((int(self.num_rounds/2))+1):  #this number could be bigger
            threads.append(Thread(target=self.run_all_rounds(True)))
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()








