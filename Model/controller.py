from threading import Lock, Thread


class Controller:
    """
    A class representing the connection between the backend and the frontend, is trusted of the connecting both sub-systems messages.\n
    The class coordinate between the changes that are taking place in the business logic to the UI, the object
    has also some threaded functions methodology for better efficiency of the game.\n

    Attributes:/n

    model: representation of the model manager class -> ModelManger object.\n
    view: representation of the view manager class -> ViewManger object.\n
    lock: mutex lock for threads -> Lock object.\n
    """

    def __init__(self,model,view):
        self.model=model
        self.view=view
        self.lock=Lock()
        self.tasks=[]

    def get_view(self):
        return self.view

    def set_view(self,view):
        self.view=view

    def get_model(self):
        return self.model

    def set_model(self, model):
        self.model = model


    #################### Model related methods #####################################
    def prepare_thread_to_trgt(self,trgt_func):
        pass

    def ntfy_to_view_pris_pos(self,pos:tuple):
        pass

    def ntfy_to_view_pris_need_box(self,box_num):
        pass

    def ntfy_to_view_pris_changed(self,new_pris_num):
        pass

    def ntfy_to_view_pris_need_boxes_pos(self):#will return dict of {num_box:position}
        pass

    def model_start_game(self,num_prisoners,num_round,print_specifically):
        pass

    def ntfy_to_view_pris_succeeded(self,num_succeeded):
        pass

    ###################################################################################