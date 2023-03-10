from Prisoners_Algorithm.Model.boxm import BoxM
from Prisoners_Algorithm.Model.controller import Controller
from Prisoners_Algorithm.Model.prisonerm import PrisonerM
from Prisoners_Algorithm.Model.probabilities_handler import ProbabilitiesHandler


class ModelManger:
    """
    A class representing the managing object that is trusted of the backend part of the game.\n
    The class coordinate between the changes that are taking place in the business logic, the object
    is also handle different events that come from the UI and respond according to the event.\n

    Attributes:\n

    dict_rounds: all rounds and its relational list representation -> dictionary of {round number: list of box numbers}.\n
    dict_prisoners: all prisoners mapped by their number-> dictionary of {prisoner number: PrisonerM object}.\n
    dict_boxes:  all boxes mapped by their number-> dictionary of {box number: BoxM object}.\n
    listener: coordinates the activity between the backend and the frontend -> Controller object.\n
    current_round: the number of the current round-> int.\n
    current_prisoner: the current prisoner number-> int.\n
    succeeded: the number of succeeded prisoners in the current game-> int.\n
    num_prisoners: the total number of prisoners -> int.\n
    num_rounds: the total number of rounds -> int.\n
    print_specifically: user choice if he/she wants to print to file "PrisonersResults.txt" the specific route of each prisoner or not -> bool.\n
    prob_handler: a probability handler object, handles with probability calculations of each round and the total success rate -> ProbabilitiesHandler object.
    """

    def __init__(self,num_prisoners:int,num_rounds:int,print_specifically:bool,listener:Controller):
        """
        Initialize ModelManger Object.\n
        :param num_prisoners: int, the number of prisoners.
        :param num_rounds: int, the number of rounds.
        :param print_specifically: bool, indication if the user want full description of each prisoner and round
        :param listener: Controller object, coordinator class between backend and frontend
        """
        self.dict_rounds={}  #dict of {round_num:list dependencies of boxes}
        self.dict_prisoners={}   #dict of {num_pris:prisoner}
        self.dict_boxes= {}  #dict of {num_box:box}
        self.listener=listener
        self.current_round = 1
        self.current_prisoner = 1
        self.succeeded=0
        self.num_prisoners = num_prisoners
        self.num_rounds = num_rounds
        self.print_specifically = print_specifically
        self.prob_handler=None

    ############# Listener Methods ###################################

    def ntfy_pris_pos(self):
        self.listener.ntfy_view_pris_pos(self.dict_prisoners[self.current_prisoner].get_pos())

    def ntfy_pris_need_box(self):
        self.listener.notify_model_need_box(self.dict_prisoners[self.current_prisoner].trgt_box.box_num)

    def ntfy_pris_changed(self):
        self.listener.ntfy_pris_changed(self.current_prisoner.get_num())

    def ntfy_model_need_boxes_pos(self):
        return self.listener.ntfy_model_need_boxes_pos()  #will return dict of {num_box:position}

    ######################################################################

    def init_boxes(self) -> None:
        """
        Initialization method for creating new BoxM objects according the round requirements and screen placing.\n
        :return: None
        """
        for index_box in range(self.num_prisoners):
            box=BoxM(box_num=index_box + 1)
            self.dict_boxes[index_box+1]=box
        for box_num in self.dict_boxes.keys():  #box num starts from 1 to n+1
            self.dict_boxes[box_num].set_next_box(self.dict_boxes[self.dict_rounds[self.current_round][box_num-1]])  #redirecting each box to current next box
        self.set_all_boxes_pos()

    def set_all_boxes_pos(self) -> None:
        """
        Set method for ll boxes position, the method requests the controller to hand over the box locations on the screen.\n
        :return: None
        """
        positions = self.ntfy_model_need_boxes_pos()
        for box_num in self.dict_boxes.keys():
            self.dict_boxes[box_num].set_pos = positions[box_num]

    def init_prisoners(self) -> None:
        """
        Initialization method for creating new PrisonerM objects according the round requirements.\n
        :return: None
        """
        for index_pris in range(self.num_prisoners):
            self.dict_prisoners[index_pris+1]=PrisonerM(num_prisoner=index_pris + 1, position=(0, 0), pace=5, all_boxes=self.dict_rounds[self.current_round], trgt_box=self.dict_boxes[index_pris + 1])

    def run_game(self) -> None:
        """
        The actual method that responsible for the game functionality.\n
        At first the function run the ProbabilityManager calculations and let the priosners move by its requirements.\n
        :return: None
        """
        self.prob_handler=ProbabilitiesHandler(num_prisoners=self.num_prisoners,num_rounds=self.num_rounds,print_specifically=self.print_specifically)
        self.dict_rounds=self.prob_handler.run_probabilities()
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
                pass
                self.ntfy_pris_need_box()
                self.dict_prisoners[self.current_prisoner].move_to_box()
                self.ntfy_pris_pos()
            self.current_prisoner+=1



