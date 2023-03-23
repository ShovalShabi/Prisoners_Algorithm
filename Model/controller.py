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

    def __init__(self, model: ModelManger, view: ViewManager) -> None:
        """
        Initialize Controller object.\n
        :param model: ModelManager object, the object that representing the business logic.
        :param view:  ViewManager object, the object that representing the user interface.
        :return: None.
        """
        self.model = model
        self.view = view

    def get_view(self) -> ViewManager:
        """
        Method for getting ViewManager object.\n
        :return: ViewManager object.
        """
        return self.view

    def set_view(self, view) -> None:
        """
        Method for setting ViewManager object.\n
        :return: None.
        """
        self.view = view

    def get_model(self) -> ModelManger:
        """
        Method for getting ModelManager object.\n
        :return: ModelManager object.
        """
        return self.model

    def set_model(self, model) -> None:
        """
        Method for setting ModelManager object.\n
        :return: ModelManager object.
        """
        self.model = model

    # **************************************************************************************************************************************************#
    # *************************************************** Model related methods ************************************************************************#
    def model_need_box(self, box_num) -> None:
        """
        Method for notifying the ViewManager that the ModelManager need a box with specific number on screen.\n
        :param box_num: int, number that representing box number.

        :return: None.
        """
        self.cnt_ntfy_view_handle_box_req(box_num)

    def model_need_box_dimensions(self) -> tuple[int, int]:
        """
        Method for notifying the ViewManager that the ModelManager need a box image dimensions.\n

        :return: tuple[int,int], of box dimensions.
        """
        return self.cnt_ntfy_to_view_get_box_dimension()

    def model_need_pris_dimensions(self) -> tuple[int, int]:
        """
        Method for notifying the ViewManager that the ModelManager need a prisoner image dimensions.\n

        :return: tuple[int,int], of prisoner dimensions.
        """
        return self.cnt_ntfy_to_view_get_pris_dimension()

    def model_need_all_boxes_on_screen_pos(self) -> dict:
        """
        Method for notifying the ViewManager that the ModelManager need the boxes positions on screen.\n

        :return: dict of {box number : position by tuple[int,int]}.
        """
        return self.cnt_ntfy_to_view_get_all_boxes_location()

    def model_need_to_open_box(self, current_box_num) -> None:
        """
        Method for notifying the ViewManager that the ModelManager need to open box with a specific number.\n
        :param current_box_num: int, representing the box number to be open.

        :return: None.
        """
        self.cnt_ntfy_view_open_box(current_box_num)

    def model_need_to_report_success(self, current_pris_num, num_succeeded) -> None:
        """
        Method for notifying the ViewManager that the ModelManager need to show prisoner success.\n

        :param current_pris_num: int, representing the prisoner that manged to escape.
        :param num_succeeded: int, the prisoners that manged to escape so far.

        :return: None.
        """
        self.cnt_ntfy_view_on_success(current_pris_num, num_succeeded)

    def model_need_to_report_failure(self, current_pris_num) -> None:
        """
        Method for notifying the ViewManager that the ModelManager need to show prisoner success.\n
        :param current_pris_num: int, representing the prisoner that failed.

        :return: None.
        """
        self.cnt_ntfy_view_on_failure(current_pris_num)

    def model_need_to_update_time(self, time: float) -> None:
        """
        Method for notifying the ViewManager that the ModelManager need to show prisoner success.\n
        :param time: float, a number that represents the time that took the prisoner to get his target box.

        :return: None.
        """
        self.cnt_ntfy_view_on_time(time)

    def cnt_ntfy_to_view_pris_pos(self) -> tuple[int, int]:
        """
        Method for Controller notifying the model the position of a prisoner on screen.\n

        :return: position tuple of (x,y).
        """
        return self.model.get_current_pris_pos()

    def cnt_ntfy_to_model_init_game(self, num_prisoners, num_round, initial_pos, print_specifically) -> dict:
        """
        Method for Controller notifying the model to initialize a new game.\n
        :param num_prisoners: int, represents the number of prisoners.
        :param num_round: int, represents the number of rounds.
        :param initial_pos: tuple of (x,y), represents the initial positions of the prisoner.
        :param print_specifically: bool, indicator for specification level.

        :return: dict of {round:list of dependencies of boxes numbered from zero to the number of prisoners -1}.
        """
        return self.model.setup_game(num_prisoners, num_round, initial_pos, print_specifically)

    def cnt_ntfy_to_model_run_game(self) -> None:
        """
        Method for Controller notifying the model to run game.\n

        :return: None
        """
        self.model.run_game()

    def cnt_ntfy_to_model_stop_game(self) -> None:
        """
        Method for Controller notifying the model to run game.\n

        :return: None.
        """
        self.model.stop_game()

    def cnt_ntfy_to_view_pris_changed(self) -> int:
        """
        Method for Controller notifying the model that the view need prisoner number.\n

        :return: int, prisoner number.
        """
        return self.model.get_current_pris_num()

    def cnt_ntfy_to_view_round_num(self) -> int:
        """
        Method for Controller notifying the model that the view need prisoner number.\n

        :return: int, the current round number.
        """
        return self.model.current_round

    def cnt_update_boxes_pos(self) -> None:
        """
        Method for Controller notifying the model to update boxes position on screen.\n
        :return:: None
        """
        self.model.set_all_boxes_pos()

    def cnt_ntfy_to_model_init_stat(self, num_prisoners, num_rounds, print_specify) -> None:
        """
        Method that tells the model to calculate statistics.\n
        :param num_prisoners: int, the number of prisoners.
        :param num_rounds: int, the number of rounds.
        :param print_specify: bool, indication to print specified results.

        :return: None.
        """
        self.model.run_statistics(num_prisoners, num_rounds, print_specify)

    def get_from_model_game_status(self):
        """
        Method for Controller to retrieve from the model to its running status.\n

        :return: bool, an indicator of game status in ModelManager.
        """
        return self.model.get_game_status()

    # *************************************************************************************************************************************************#
    # *************************************************** View related methods ************************************************************************#

    def view_need_pris_pos(self) -> tuple[int, int]:
        """
        Method for notifying the ModelManager that the ViewManager need a prisoner with specific number on screen.\n
        :return: tuple of (x,y)
        """
        return self.cnt_ntfy_to_view_pris_pos()

    def view_need_to_init_game(self, num_of_prisoners, num_of_rounds, initial_pos, print_specifically) -> dict:
        """
        Method for notifying the ModelManager that the ViewManager need to initialize game.\n

        :param num_of_prisoners: int, represents the number of prisoners.
        :param num_of_rounds: int, represents the number of rounds.
        :param initial_pos: tuple of (x,y), represents the initial positions of the prisoner.
        :param print_specifically: bool, indicator for specification level.
        :return: dict of {round:list of dependencies of boxes numbered from zero to the number of prisoners -1}.
        """
        return self.cnt_ntfy_to_model_init_game(num_of_prisoners, num_of_rounds, initial_pos, print_specifically)

    def view_need_round_num(self) -> int:
        """
        Method for notifying the ModelManager that the ViewManager need the current round number.\n
        :return: int, representing round number.
        """
        return self.cnt_ntfy_to_view_round_num()

    def view_need_pris_num(self) -> int:
        """
        Method for notifying the ModelManager that the ViewManager need the current prisoner number.\n
        :return: int, representing prisoner number.
        """
        return self.cnt_ntfy_to_view_pris_changed()

    def view_need_to_run_game(self) -> None:
        """
        Method for notifying the ModelManager that the ViewManager need to run the game.\n
        :return: int, representing round number.
        """
        self.cnt_ntfy_to_model_run_game()

    def view_need_know_game_status(self) -> bool:
        """
        Method for notifying the ModelManager that the ViewManager need the status of the game .\n
        :return: bool, representing running game flag.
        """
        return self.get_from_model_game_status()

    def view_need_update_boxes_pos(self) -> None:
        """
        Method for notifying the ModelManager that the ViewManager need to update the positions of the boxes that are on screen .\n
        :return: None
        """
        self.cnt_update_boxes_pos()

    def view_need_model_stop_running(self) -> None:
        """
        Method for notifying the ModelManager that the ViewManager need to stop the game .\n
        Returns: None.
        """
        self.cnt_ntfy_to_model_stop_game()

    def view_need_to_init_statistics(self, num_prisoners, num_rounds, print_specify) -> None:
        """
        Method that tells the controller to calculate statistics.\n
        :param num_prisoners: int, the number of prisoners.
        :param num_rounds: int, the number of rounds.
        :param print_specify: bool, indication to print specified results.

        :return: None.
        """
        self.cnt_ntfy_to_model_init_stat(num_prisoners, num_rounds, print_specify)

    def cnt_ntfy_view_handle_box_req(self, box_num) -> None:
        """
        Method for Controller notifying the view that the model need a specific box number to be on screen.\n
        :param box_num: int, representing the box number.

        :return: None.
        """
        self.view.handle_box_request(box_num)

    def cnt_ntfy_to_view_get_box_dimension(self) -> tuple[int, int]:
        """
        Method for Controller notifying the view that the model need the dimensions of box image for further calculation.\n
        :return: tuple of (x,y) that represents box dimensions.
        """
        return self.view.get_box_dimensions()

    def cnt_ntfy_to_view_get_pris_dimension(self) -> tuple[int, int]:
        """
        Method for Controller notifying the view that the model need the dimensions of prisoner image for further calculation.\n
        :return: tuple of (x,y) that represents box dimensions.
        """
        return self.view.get_pris_dimensions()

    def cnt_ntfy_to_view_get_all_boxes_location(self) -> dict:
        """
        Method for Controller notifying the view that the model need the locations of all the boxes that are on screen.\n
        :return: dict of {number of box : tuple of (x,y) that represents box position}.
        """
        return self.view.get_boxes_locations()

    def cnt_ntfy_view_open_box(self, current_box_num):
        """
        Method for Controller notifying the view that the model need to open specific box number.\n
        :param current_box_num: int, a number that represents box number.
        :return: None.
        """
        self.view.open_box(current_box_num)

    def cnt_ntfy_view_on_success(self, current_pris_num, num_succeeded) -> None:
        """
        Method for Controller notifying the view that the model need to open specific box number.\n
        :param current_pris_num: int, a number that represents current prisoner number.
        :param num_succeeded: int, a number that represents the number of prisoners that managed to escape.
        :return: None.
        """
        self.view.handle_with_success(current_pris_num, num_succeeded)

    def cnt_ntfy_view_on_failure(self, current_pris_num):
        """
        Method for Controller notifying the view that the model need to open specific box number.\n
        :param current_pris_num: int, a number that represents current prisoner number.
        :return: None.
        """
        self.view.handle_with_failure(current_pris_num)

    def cnt_ntfy_view_on_time(self, time: float) -> None:
        """
        Method for Controller notifying the view that the model need to open specific box number.\n
        :param time: float, a number that represents the time that took the prisoner to get his target box.
        :return: None.
        """
        self.view.handle_with_time(time)
