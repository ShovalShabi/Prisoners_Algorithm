from threading import Lock,Thread

from Model.model_manger import ModelManger
from View.viewmanager import ViewManager


class Controller:
    """
    A class representing the connection between the backend and the frontend, is trusted of the connecting both sub-systems messages.\n
    The class coordinate between the changes that are taking place in the business logic to the UI.\n

    Attributes:/n

    model: representation of the model manager class -> ModelManger object.\n
    view: representation of the view manager class -> ViewManger object.\n
    lock: mutex lock for threads -> Lock object.\n
    """

    def __init__(self, model: ModelManger, view: ViewManager):
        self.model = model
        self.view = view
        self.lock=Lock()
        self.tasks = []

    def get_view(self):
        return self.view

    def set_view(self, view):
        self.view = view

    def get_model(self):
        return self.model

    def set_model(self, model):
        self.model = model

    #################### Model related methods #####################################
    def ntfy_to_view_pris_pos(self):
        return self.model.get_current_pris_pos()

    def model_need_box(self, box_num):
        self.ntfy_view_handle_box_request(box_num)

    def ntfy_to_view_pris_changed(self):
        return self.model.get_current_pris_num()

    def model_need_box_dimensions(self):
        return self.ntfy_to_view_get_box_dimension()

    def ntfy_view_get_all_boxes_on_screen_pos(self):  # will return dict of {num_box:position}
        return self.ntfy_to_view_get_all_boxes_locationV()

    def ntfy_to_model_init_game(self, num_prisoners, num_round, initial_pos, print_specifically):
        self.model.setup_game(num_prisoners, num_round, initial_pos, print_specifically)

    def ntfy_to_model_run_game(self):
        self.model.run_game()

    ###################################################################################
    ######################## View related methods #####################################

    def view_need_pris_pos(self):
        return self.ntfy_to_view_pris_pos()

    def ntfy_view_handle_box_request(self, box_num):
        self.view.handle_box_request(box_num)

    def ntfy_view_to_replace_pris(self, new_pris_num):
        self.view.replace_prisoner(new_pris_num)

    def ntfy_to_view_get_box_dimension(self) -> None:
        """
        Sends the dimensions of the box image to the listener.
        """
        return self.view.get_box_dimensions()

    def ntfy_to_view_get_all_boxes_locationV(self) -> None:
        """
        Sends the current locations of all the boxes to the listener.
        """
        return self.view.get_boxes_locations()

    def view_need_to_init_game(self, num_of_prisoners, num_of_rounds, initial_pos, print_specifically) -> None:
        """
        Send the input data to model object.

        :param print_specifically:
        :param initial_pos:
        :param num_of_rounds: The numbers of input rounds
        :param num_of_prisoners: The numbers of input prisoners
        """
        self.ntfy_to_model_init_game(num_of_prisoners, num_of_rounds, initial_pos, print_specifically)

    def view_need_to_run_game(self):
        self.ntfy_to_model_run_game()

    def view_need_pris_num(self):
        return self.ntfy_to_view_pris_changed()

    def view_request_method(self,trgt_func):
        thread = Thread(trgt_func)
        thread.start()


