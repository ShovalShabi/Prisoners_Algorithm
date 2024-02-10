from abc import ABC, abstractmethod

class AbstractViewManager(ABC):
    @abstractmethod
    def handle_box_request(self, box_num) -> None:
        """
        Method for Controller notifying the view that the model need a specific box number to be on screen.\n
        :param box_num: int, representing the box number.
        :return: None.
        """
        pass

    @abstractmethod
    def get_box_dimensions(self) -> tuple[int, int]:
        """
        Method for Controller notifying the view that the model need the dimensions of box image for further calculation.\n
        :return: tuple of (x,y) that represents box dimensions.
        """
        pass

    @abstractmethod
    def get_pris_dimensions(self) -> tuple[int, int]:
        """
        Method for Controller notifying the view that the model need the dimensions of prisoner image for further calculation.\n
        :return: tuple of (x,y) that represents box dimensions.
        """
        pass

    @abstractmethod
    def get_boxes_locations(self) -> dict:
        """
        Method for Controller notifying the view that the model need the locations of all the boxes that are on screen.\n
        :return: dict of {number of box : tuple of (x,y) that represents box position}.
        """
        pass

    @abstractmethod
    def open_box(self, current_box_num):
        """
        Method for Controller notifying the view that the model need to open specific box number.\n
        :param current_box_num: int, a number that represents box number.
        :return: None.
        """
        pass

    @abstractmethod
    def handle_with_success(self, current_pris_num, num_succeeded) -> None:
        """
        Method for Controller notifying the view that the model need to open specific box number.\n
        :param current_pris_num: int, a number that represents current prisoner number.
        :param num_succeeded: int, a number that represents the number of prisoners that managed to escape.
        :return: None.
        """
        pass

    @abstractmethod
    def handle_with_failure(self, current_pris_num):
        """
        Method for Controller notifying the view that the model need to open specific box number.\n
        :param current_pris_num: int, a number that represents current prisoner number.
        :return: None.
        """
        pass

    @abstractmethod
    def handle_with_time(self, time: float) -> None:
        """
        Method for Controller notifying the view that the model need to open specific box number.\n
        :param time: float, a number that represents the time that took the prisoner to get his target box.
        :return: None.
        """
        pass
