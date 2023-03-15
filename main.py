from Model.controller import Controller
from Model.modelmanager import ModelManger
from View.viewmanager import ViewManager

if __name__ == '__main__':
    model = ModelManger()
    view = ViewManager()
    controller = Controller(model=model, view=view)

    model.set_listener(controller)
    view.set_listener(controller)

    view.run()
