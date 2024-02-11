from abc import ABC, abstractmethod

class AbstractProbabilitiesHandler(ABC):
    @abstractmethod
    def run_probabilities(self) -> dict:
        """
        Method that run the probability calculation concurrently by threads and afterwards return the relation between each round and its
        dependencies list of boxes.\n
        :return: dict, each round has a dependencies for the boxes, dictionary of {round number:list of box number dependencies}.
        """
        pass