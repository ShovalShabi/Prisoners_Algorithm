from Model.controller import Controller
from Model.model_manger import ModelManger
from viewmanager import *

if __name__ == '__main__':
    model = ModelManger()
    view = ViewManager()
    controller = Controller(model=model, view=view)

    model.set_listener(controller)
    view.set_listener(controller)

    view.run()
