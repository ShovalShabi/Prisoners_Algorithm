

class Controller:
    """
    A class representing the connection between the backend and the frontend, is trusted of the connecting both sub-systems messages.
    The class coordinate between the changes that are taking place in the business logic to the UI, the object
    is also works in some functions as threaded methodology for better efficiency to the game.

    :parameter:prisoner_num, prisoner number -> int.
    :parameter:pos, position of the prisoner on screen-> tuple of (x,y).
    :parameter:pace, pace of the prisoner, int.
    :parameter:visited_boxes, all the boxes that the prisoner have opened, dictionary of {number box:value box}.
    :parameter:all_boxes,all the boxes located on screen-> dictionary of {number box:value box}.
    :parameter:trgt_box, the current target box of the prisoner -> BoxM object.
    :parameter:found_number, indicator if the prisoner have found his number -> bool.
    :parameter:updated_pos, flag the represents if the prisoner has been change position -> bool.
    """

    def __init__(self):
        pass