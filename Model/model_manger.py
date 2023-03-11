from Model.boxm import BoxM
from Model.prisonerm import PrisonerM
from Model.probabilities_handler import ProbabilitiesHandler


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

    def __init__(self):
        """
        Initialize ModelManger Object.\n
        :param listener: Controller object, coordinator class between backend and frontend.
        """
        self.dict_rounds = {}  # dict of {round_num:list dependencies of boxes}
        self.dict_prisoners = {}  # dict of {num_pris:prisoner}
        self.dict_boxes = {}  # dict of {num_box:box}
        self.current_round = 1
        self.current_pris_num = 1
        self.succeeded = 0
        self.prob_handler = None
        self.listener = None

    ############################## MVC Methods ###################################

    def ntfy_to_view_pris_pos(self):
        self.listener.ntfy_to_view_pris_pos(self.dict_prisoners[self.current_pris_num].get_pos())

    def pris_request_box(self):
        self.listener.model_need_box(self.dict_prisoners[self.current_pris_num].trgt_box.box_num)

    def ntfy_view_to_replace_pris(self):
        self.listener.ntfy_view_to_replace_pris(self.current_pris_num.get_num())

    def model_request_box_dimensions(self):
        return self.listener.model_request_box_dimensions()

    def ntfy_to_view_get_all_boxes_pos(self):
        return self.listener.ntfy_view_get_all_boxes_on_screen_pos()  # will return dict of {num_box:position}

    def set_listener(self, listener):
        self.listener = listener

    ###############################################################################

    def init_prisoners(self, num_pris: int, initial_pos: tuple) -> None:
        """
        Initialization method for creating new PrisonerM objects according the round requirements.\n
        :param num_pris: int, the number o prisoners.
        :param initial_pos: tuple, initial position of the prisoner on screen (x,y)
        :return: None
        """
        if self.dict_prisoners:
            self.dict_prisoners = {}
        for index_pris in range(num_pris):
            self.dict_prisoners[index_pris + 1] = PrisonerM(num_prisoner=index_pris + 1, position=initial_pos, pace=5,
                                                            all_boxes=self.dict_rounds[self.current_round],
                                                            trgt_box=self.dict_boxes[index_pris + 1])

    def init_boxes(self, num_pris) -> None:
        """
        Initialization method for creating new BoxM objects according the round requirements and screen placing.\n
        :param num_pris: int, the number o prisoners.
        :return: None
        """
        if self.dict_boxes:
            self.dict_boxes = {}
        for index_box in range(num_pris):
            box = BoxM(box_num=index_box + 1)
            self.dict_boxes[index_box + 1] = box
        for box_num in self.dict_boxes.keys():  # box num starts from 1 to n+1
            self.dict_boxes[box_num].set_next_box(self.dict_boxes[self.dict_rounds[self.current_round][
                box_num - 1]])  # redirecting each box to current next box
        self.set_all_boxes_pos()

    def set_all_boxes_pos(self) -> None:
        """
        Set method for ll boxes position, the method requests the controller to hand over the box locations on the screen.\n
        :return: None
        """
        boxes_on_screen = self.ntfy_to_view_get_all_boxes_pos()
        for box_num in self.dict_boxes.keys():
            self.dict_boxes[box_num].set_pos = boxes_on_screen[box_num]

    def run_game(self, num_pris, num_rounds, initial_pos, print_specifically) -> None:
        """
        The actual method that responsible for the game functionality.\n
        At first the function run the ProbabilityManager calculations and let the prisoners move by its requirements.\n
        :param num_pris: int, the number o prisoners.
        :param num_rounds: int, the number of rounds.
        :param initial_pos: tuple, the initial position of the prisoner on screen (x,y)
        :param print_specifically: bool, indication if the user want full description of each prisoner and round
        :return: None
        """
        self.prob_handler = ProbabilitiesHandler(num_prisoners=num_pris, num_rounds=num_rounds,
                                                 print_specifically=print_specifically)
        self.dict_rounds = self.prob_handler.run_probabilities()
        self.current_round = 1
        self.init_boxes(num_pris=num_pris)
        self.init_prisoners(num_pris=num_pris, initial_pos=initial_pos)
        while self.current_round < num_rounds:

            if self.current_pris_num > num_pris:
                self.current_pris_num = 1
                self.current_round += 1
                self.succeeded = 0
                if self.current_round > num_rounds:
                    return
                else:
                    self.current_round += 1
                    self.init_boxes(num_pris=num_pris)
                    self.init_prisoners(num_pris=num_pris, initial_pos=initial_pos)

            while self.dict_prisoners[self.current_pris_num].is_still_searching():
                self.pris_request_box()
                self.dict_prisoners[self.current_pris_num].move_to_box()
                self.ntfy_to_view_pris_pos()

            self.current_pris_num += 1

    def get_current_pris_num(self):
        return self.current_pris_num

    def get_current_pris_pos(self):
        return self.dict_prisoners[self.current_pris_num].get_pos()
