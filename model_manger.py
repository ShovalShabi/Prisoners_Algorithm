

class ModelManger:

    def __init__(self,num_prisoners,num_rounds,listener):
        self.dict_prisoners={}
        self.dict_boxes= {}
        self.listener=listener
        self.num_prisoners=num_prisoners
        self.num_rounds= num_rounds
        self.current_round = 1
        self.succeeded=0
        self.current_prisoners=None

    def ntfy_pris_pos(self, num_prisoner):
        return self.dict_prisoners[num_prisoner].get_pos()

    def ntfy_pris_need_box(self, box_number):
        self.listener.notify_model_need_box(box_number)

    def ntfy_model_need_boxes_pos(self):
        return self.listener.ntfy_model_need_boxes_pos()  #will return dict of {num_box:position}

    def init_boxes(self):
        positions=self.ntfy_model_need_boxes_pos()
        for num_box in self.dict_boxes.keys():
            self.dict_boxes[num_box].set_pos(positions[num_box])

    def set_all_boxes_location(self,list_pos):
        pass

    def set_boxes_to_prisoners(self):
        pass

    def set_listener(self):
        pass

    def run_prob(self):
        pass






