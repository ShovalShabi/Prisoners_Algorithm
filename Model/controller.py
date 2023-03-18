from Model.modelmanager import ModelManger
from View.viewmanager import ViewManager


class Controller:
    """
    A class representing the connection between the backend and the frontend, is trusted of the connecting both sub-systems messages.\n
    The class coordinate between the changes that are taking place in the business logic to the UI.\n

    Attributes:/n

    model: representation of the model manager class -> ModelManger object.\n
    view: representation of the view manager class -> ViewManger object.\n
    """

    def __init__(self, model: ModelManger, view: ViewManager):
        self.model = model
        self.view = view

    def get_view(self):
        return self.view

    def set_view(self, view):
        self.view = view

    def get_model(self):
        return self.model

    def set_model(self, model):
        self.model = model

    #******************************* Model related methods *******************************#
    def model_need_box(self, box_num):
        self.cnt_ntfy_view_handle_box_req(box_num)

    def model_need_box_dimensions(self):
        return self.cnt_ntfy_to_view_get_box_dimension()

    def model_need_pris_dimensions(self):
        return self.cnt_ntfy_to_view_get_pris_dimension()

    def model_need_all_boxes_on_screen_pos(self):  # will return dict of {num_box:position}
        return self.cnt_ntfy_to_view_get_all_boxes_location()

    def model_need_to_open_box(self,current_box_num):
        self.cnt_ntfy_view_open_box(current_box_num)

    def model_need_to_report_success(self,current_pris_num,num_succeeded):
        self.cnt_ntfy_view_on_success(current_pris_num,num_succeeded)

    def model_need_to_report_failure(self,current_pris_num):
        self.cnt_ntfy_view_on_failure(current_pris_num)

    def cnt_ntfy_to_view_pris_pos(self):
        return self.model.get_current_pris_pos()

    def cnt_ntfy_to_model_init_game(self, num_prisoners, num_round, initial_pos, print_specifically) -> dict:
        return self.model.setup_game(num_prisoners, num_round, initial_pos, print_specifically)

    def cnt_ntfy_to_model_run_game(self):
        self.model.run_game()

    def cnt_ntfy_to_model_stop_game(self, flag):
        self.model.is_running_game = flag

    def cnt_ntfy_to_view_pris_changed(self):
        return self.model.get_current_pris_num()

    def cnt_ntfy_to_view_round_num(self):
        return self.model.current_round

    def cnt_update_boxes_pos(self):
        self.model.set_all_boxes_pos()

    def get_from_model_game_status(self):
        return self.model.get_game_status()

    #************************************************************************************#
    #****************************** View related methods ********************************#

    def view_need_pris_pos(self):
        return self.cnt_ntfy_to_view_pris_pos()

    def view_need_to_init_game(self, num_of_prisoners, num_of_rounds, initial_pos, print_specifically) -> dict:
        return self.cnt_ntfy_to_model_init_game(num_of_prisoners, num_of_rounds, initial_pos, print_specifically)

    def view_need_round_num(self):
        return self.cnt_ntfy_to_view_round_num()

    def view_need_pris_num(self):
        return self.cnt_ntfy_to_view_pris_changed()

    def view_need_to_run_game(self):
        self.cnt_ntfy_to_model_run_game()

    def view_need_know_game_status(self):
        return self.get_from_model_game_status()

    def view_need_model_stop_running(self,flag):
        self.cnt_ntfy_to_model_stop_game(flag=flag)

    def view_need_update_boxes_pos(self):
        self.cnt_update_boxes_pos()

    def cnt_ntfy_view_handle_box_req(self, box_num):
        self.view.handle_box_request(box_num)

    def cnt_ntfy_to_view_get_box_dimension(self) -> None:
        """
        Sends the dimensions of the box image to the listener.
        """
        return self.view.get_box_dimensions()

    def cnt_ntfy_to_view_get_pris_dimension(self) -> None:
        """
        Sends the dimensions of the prisoner image to the listener.
        """
        return self.view.get_pris_dimensions()

    def cnt_ntfy_to_view_get_all_boxes_location(self) -> None:
        """
        Sends the current locations of all the boxes to the listener.
        """
        return self.view.get_boxes_locations()

    def cnt_ntfy_view_open_box(self,current_box_num):
        self.view.open_box(current_box_num)

    def cnt_ntfy_view_on_success(self,current_pris_num,num_succeeded):
        self.view_handle_with_success(current_pris_num,num_succeeded)

    def cnt_ntfy_view_on_failure(self,current_pris_num):
        self.view_handle_with_failure(current_pris_num)