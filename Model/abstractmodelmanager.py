from abc import ABC, abstractmethod

class AbstractModelManager(ABC):
    @abstractmethod
    def get_current_pris_pos(self) -> tuple[int, int]:
        """
        Method for Controller notifying the model the position of a prisoner on screen.\n
        :return: position tuple of (x,y).
        """
        pass

    @abstractmethod
    def setup_game(self, num_prisoners, num_round, initial_pos, print_specifically) -> dict:
        """
        Method for Controller notifying the model to initialize a new game.\n
        :param num_prisoners: int, represents the number of prisoners.
        :param num_round: int, represents the number of rounds.
        :param initial_pos: tuple of (x,y), represents the initial positions of the prisoner.
        :param print_specifically: bool, indicator for specification level.
        :return: dict of {round:list of dependencies of boxes numbered from zero to the number of prisoners -1}.
        """
        pass

    @abstractmethod
    def run_game(self) -> None:
        """
        Method for Controller notifying the model to run game.\n
        :return: None
        """
        pass

    @abstractmethod
    def stop_game(self) -> None:
        """
        Method for Controller notifying the model to run game.\n
        :return: None.
        """
        pass

    @abstractmethod
    def get_current_pris_num(self) -> int:
        """
        Method for Controller notifying the model that the view need prisoner number.\n
        :return: int, prisoner number.
        """
        pass

    @abstractmethod
    def get_current_round(self) -> int:
        """
        Method for Controller notifying the model that the view need prisoner number.\n
        :return: int, the current round number.
        """
        pass

    @abstractmethod
    def set_all_boxes_pos(self) -> None:
        """
        Method for Controller notifying the model to update boxes position on screen.\n
        :return:: None
        """
        pass

    @abstractmethod
    def run_statistics(self, num_prisoners, num_rounds, print_specify) -> None:
        """
        Method that tells the model to calculate statistics.\n
        :param num_prisoners: int, the number of prisoners.
        :param num_rounds: int, the number of rounds.
        :param print_specify: bool, indication to print specified results.
        :return: None.
        """
        pass

    @abstractmethod
    def get_game_status(self):
        """
        Method for Controller to retrieve from the model to its running status.\n
        :return: bool, an indicator of game status in ModelManager.
        """
        pass
