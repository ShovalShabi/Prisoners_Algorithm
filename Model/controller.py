class Controller:
    """
    A class representing the connection between the backend and the frontend, is trusted of the connecting both sub-systems messages.\n
    The class coordinate between the changes that are taking place in the business logic to the UI.\n

    Attributes:/n

    model: representation of the model manager class -> ModelManger object.\n
    view: representation of the view manager class -> ViewManger object.\n
    lock: mutex lock for threads -> Lock object.\n
    """

    def __init__(self, model, view):
        self.model = model
        self.view = view
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
    def ntfy_to_view_pris_pos(self, pos: tuple):
        pass

    def ntfy_to_view_pris_need_box(self, box_num):
        pass

    def ntfy_to_view_pris_changed(self, new_pris_num):
        pass

    def ntfy_to_view_pris_need_boxes_pos(self):  # will return dict of {num_box:position}
        pass

    def model_start_game(self, num_prisoners, num_round, print_specifically):
        pass

    def ntfy_to_view_pris_succeeded(self, num_succeeded):
        pass

    ###################################################################################

    ######################## View related methods ####################################

    def ntfy_to_model_boxes_locationV(self,boxes_on_screen:dict) -> None:
        """
        Sends the current locations of all the boxes to the listener.
        """
        self.listener.send_boxes_locationV(boxes_on_screen)

    def ntfy_to_model_box_dimension(self,box_width:int,box_height:int) -> None:
        """
        Sends the dimensions of the box image to the listener.
        """
        self.listener.send_box_dimension(box_width, box_height)

    def ntfy_to_model_send_start_game(self, num_of_prisoners, num_of_rounds) -> None:
        """
        Send the input data to model object.

        :param num_of_rounds: The numbers of input rounds
        :param num_of_prisoners: The numbers of input prisoners
        """
        self.model_start_game(num_of_prisoners, num_of_rounds,True)
