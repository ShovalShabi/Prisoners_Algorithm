import random
from copy import deepcopy
from threading import Thread, Lock


class ProbabilitiesHandler:
    """
    A class representing the probabilities' handler object that is trusted of the details of each round and printing it to file
    "PrisonersResults.txt".\n
    The class creates scenarios for all game rounds and the linkage between the boxes.\n

    Attributes:\n

    filename: The designated file for showing game details.\n
    file: file pointer within file system.\n
    lock_shuffle: mutex lock for protection to critical blocks.\n
    num_prisoners: the total number of prisoners -> int.\n
    num_rounds: the total number of rounds -> int.\n
    print_specifically: user choice if he/she wants to print to file "PrisonersResults.txt" the specific route of each prisoner or not -> bool.\n
    dict_rounds: all rounds and its relational list representation -> dictionary of {round number: list of box numbers}.
    """
    filename = "PrisonersResults.txt"
    file = None
    lock_shuffle = Lock()

    def __init__(self, num_prisoners: int, num_rounds: int, print_specifically: bool):
        """
        Initialization of ProbabilitiesHandler object.\n
        :param num_prisoners: int, the number of prisoners.
        :param num_rounds: int, the number of rounds.
        :param print_specifically: bool, indication of details specification in file "PrisonerResults.txt".
        """
        self.num_prisoners = num_prisoners
        self.num_rounds = num_rounds
        self.print_specifically = print_specifically
        self.dict_rounds = {}
        self.output = ""

    def run_route(self, list_of_boxes: list, print_route: bool) -> bool:
        """
        Method that runs the search route of each prisoner.\n
        :param list_of_boxes: list, list of dependencies between the boxes.
        :param print_route: bool, indication of details specification "PrisonerResults.txt".
        :return: bool, True -> prisoner succeed, False -> prisoner Failed.
        """
        number_of_boxes = len(list_of_boxes)
        list_of_success = number_of_boxes * [0]
        for j in range(number_of_boxes):
            if print_route:
                print("Prisoner number:", j + 1, file=self.file)
                self.output += "--Prisoner number:{}--\n".format(j + 1)

            visited_boxes = []
            pointer_box = list_of_boxes[j]
            current_box = j + 1
            visited_boxes.append(pointer_box)
            for attempts in range(number_of_boxes):
                success = False
                if print_route:
                    print("Box number", current_box, " is leading to box", pointer_box + 1, file=self.file)
                    self.output += "Box number {} is leading to box {}\n".format(current_box, pointer_box + 1)

                if pointer_box == j and attempts < (number_of_boxes // 2):
                    success = True
                    list_of_success[j] = 1
                    break
                else:
                    if pointer_box == j:
                        break
                    else:
                        current_box = pointer_box + 1
                        pointer_box = list_of_boxes[pointer_box]
                        visited_boxes.append(pointer_box)
            if print_route:
                self.output += "\n"
                print("Total Boxes:", end=" ", file=self.file)
                self.output += "Total Boxes: "

                for o in range(number_of_boxes):
                    print(list_of_boxes[o] + 1, end=" ", file=self.file)
                    self.output += "{} ".format(list_of_boxes[o] + 1)

                print(file=self.file)
                self.output += "\n"

                print("Visited in boxes:", end=" ", file=self.file)
                self.output += "Visited in boxes: "

                for g in range(len(visited_boxes)):
                    print(visited_boxes[g] + 1, end=" ", file=self.file)
                    self.output += "{} ".format(list_of_boxes[g] + 1)

                print(file=self.file)
                self.output += "\n"

                if success:
                    print("Prisoner number", j + 1, "has been succeeded,",
                          "the chain length is", (attempts + 1), file=self.file)
                    self.output += "Prisoner number {} has been succeeded, the chain length is {}".format(j + 1, attempts + 1)

                else:
                    print("Prisoner number", j + 1, "has been failed,",
                          "the chain length is", (attempts + 1), file=self.file)
                    self.output += "Prisoner number {} has been failed, the chain length is {}".format(j + 1, attempts + 1)
                self.output += "\n"

                print(file=self.file)
                self.output += "\n"

        if print_route:
            print("The number of prisoners that found their number is",
                  sum(list_of_success), "\nout of", number_of_boxes, "prisoners.\n", file=self.file)
            self.output += "The number of prisoners that found their number is {}\n" \
                           "out of {} prisoners".format(sum(list_of_success), number_of_boxes)

        if sum(list_of_success) == number_of_boxes:
            return True
        else:
            return False

    def run_all_probs(self, print_route) -> None:
        """
        Method that runs the search route of all prisoners of each round.\n
        :param print_route: bool, indication of details specification "PrisonerResults.txt".
        :return: None.
        """
        self.open_file()
        if not isinstance(self.num_prisoners, int):
            print("The number of prisoners is ", self.num_prisoners, " the number of prisoners must be an integer.", file=self.file)
            self.output += "The number of prisoners is {} the number of prisoners must be an integer.".format(self.num_prisoners)
            return

        if self.num_prisoners < 2:
            print("The number of prisoners is ", self.num_prisoners, " the number of prisoners must be greater than 1.", file=self.file)
            self.output += "The number of prisoners is {} the number of prisoners must be greater than 1.".format(self.num_prisoners)
            return

        if not isinstance(self.num_rounds, int):
            print("The number of rounds is ", self.num_rounds, " rounds must be an integer.", file=self.file)
            self.output += "The number of rounds is {} the number of rounds must be an integer.".format(self.num_rounds)
            return

        if self.num_rounds <= 0:
            print("The number of rounds is ", self.num_rounds, " rounds must be greater 0.", file=self.file)
            self.output += "The number of rounds is {} the number of rounds must be greater 0.".format(self.num_rounds)
        success_rounds = 0
        general_lists = {}  # {round:list dependencies}
        for i in range(self.num_rounds):
            if print_route:
                print("Round number:", (i + 1), file=self.file)
                self.output += "**Round number: {}**\n\n".format(i + 1)

            list_of_boxes = self.num_prisoners * [0]
            for j in range(self.num_prisoners):
                list_of_boxes[j] = j

            self.lock_shuffle.acquire()  # lock shuffling list area
            if i + 1 not in general_lists.keys():
                random.shuffle(list_of_boxes)
                general_lists[i + 1] = list_of_boxes  #### need to fix the pointing value of each box to another from 1 to n+1
                self.dict_rounds[i + 1] = deepcopy(general_lists[i + 1])  # matching dependencies of each box to another for each round
                self.dict_rounds[i + 1] = [box_i + 1 for box_i in self.dict_rounds[i + 1]]  ## making renumbering boxes from 1 to n+1
            else:
                continue
            self.lock_shuffle.release()  # release shuffling list area

            if self.run_route(general_lists[i + 1], print_route):  ## fix this for one calculation
                success_rounds += 1

        print("The total number of prisoners is", self.num_prisoners, ",the total number of rounds is", self.num_rounds, ",the number of successful rounds is ", success_rounds,
              "\n(successful_rounds / total_rounds) as percentage is", 100 * (success_rounds / self.num_rounds), "%", file=self.file)
        temp = "The total number of prisoners is -> {}\n" \
               "The total number of rounds is -> {}\n" \
               "The number of successful rounds is -> {}\n" \
               "(successful_rounds / total_rounds) as percentage is -> {}%\n".format(self.num_prisoners, success_rounds, self.num_rounds, 100 * (success_rounds / self.num_rounds))
        temp += "\n"
        success_rounds = 0
        hn = self.num_prisoners / 2
        for i in range(self.num_prisoners // 2):
            success_rounds += 1 / (hn + (i + 1))
        print("\n\nProbability by loop calculation of the geometric series:\n",
              "1 - (1/((num_prisoners/2)+1) + 1/((num_prisoners/2)+2) + ...) =", 1 - success_rounds, file=self.file)
        temp += "Probability by loop calculation of the geometric series\n" \
                "1 - (1/((num_prisoners/2)+1) + 1/((num_prisoners/2)+2) + ...) ={}%\n".format(1 - success_rounds)
        temp += "\n"

        self.close_file()
        temp += self.output
        self.output = temp

    def open_file(self) -> None:
        """
        Method for opening file for specification.\n
        :return: None.
        """
        self.file = open(self.filename, "w")

    def close_file(self) -> None:
        """
        Method for closing file for specification.\n
        :return: None.
        """
        self.file.close()

    def run_probabilities(self) -> dict:
        """
        Method that run the probability calculation concurrently by threads and afterwards return the relation between each round and its
        dependencies list of boxes.\n
        :return: dict, each round has a dependencies for the boxes, dictionary of {round number:list of box number dependencies}.
        """
        threads = []
        for i in range((int(self.num_rounds / 2)) + 1):  # this number could be bigger
            threads.append(Thread(target=self.run_all_probs(self.print_specifically)))
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        return self.dict_rounds
