# author: itzhik aviv
# https://www.youtube.com/watch?v=iSNsgj1OCLA&ab_channel=Veritasium
import sys
import random


def pr(list_of_boxes, print_route):
    number_of_boxes = len(list_of_boxes)
    list_of_success = number_of_boxes * [0]
    for j in range(number_of_boxes):
        if print_route:
            print("Iteration number",j+1)
        visited_boxes = []
        pointer_box = list_of_boxes[j]
        visited_boxes.append(pointer_box)
        for attempts in range(number_of_boxes):
            success = False
            if print_route:
                print("Attempt:", attempts+1, " is leading to box",pointer_box+1)
            if pointer_box == j and attempts < (number_of_boxes // 2):
                success = True
                list_of_success[j] = 1
                break
            else:
                if pointer_box == j:
                    break
                else:
                    pointer_box = list_of_boxes[pointer_box]
                    visited_boxes.append(pointer_box)
        if print_route:
            print("Total Boxes:", end=" ")
            for o in range(number_of_boxes):
                print(list_of_boxes[o]+1, end=" ")
            print()
            print("Visited in boxes:", end=" ")
            for g in range(len(visited_boxes)):
                print(visited_boxes[g]+1, end=" ")
            print()
            if success:
                print("Prisoner number",j+1, "has been succeeded,",
                      "the chain length is", (attempts + 1))
            else:
                print("Prisoner number",j+1, "has been failed,",
                      "the chain length is", (attempts + 1))
            print()
    if print_route:
        print("The number of prisoners that found their number is:",
              sum(list_of_success), "\n    from", number_of_boxes, " prisoners.\n")
    if sum(list_of_success) == number_of_boxes:
        return True
    else:
        return False


def main(number_prisoners, rounds, print_route):
    if not isinstance(number_prisoners, int):
        print("The number of prisoners is ", number_prisoners, " the number of prisoners must be an integer.")
        return
    if number_prisoners < 2:
        print("The number of prisoners is ", number_prisoners, " the number of prisoners must be greater than 1.")
        return
    if not isinstance(rounds, int):
        print("The number of rounds is ", rounds, " rounds must be an integer.")
        return
    if rounds <= 0:
        print("The number of rounds is ", rounds, " rounds must be greater 0.")
    s = 0
    for i in range(rounds):
        if print_route:
            print("round number:", (i + 1))
        list_of_boxes = number_prisoners * [0]
        for j in range(number_prisoners):
            list_of_boxes[j] = j
        random.shuffle(list_of_boxes)
        if pr(list_of_boxes, print_route):
            s += 1
    print("The number of prisoners is ", number_prisoners, " The number of rounds is", rounds, " s = ", s,
          "\ns / k in % =", 100 * (s / rounds))
    s = 0
    hn = number_prisoners / 2
    for i in range(number_prisoners // 2):
        s += 1 / ((hn) + (i + 1))
    print("probability by loop calculate the geometric series:\n",
          "1 - (1/((n/2)+1) + 1/((n/2)+2) + ...) =", 1 - s)


sys.stdout = open("PrisonersResults.txt", "w")
main(number_prisoners=4, rounds=2, print_route=True)
sys.stdout.close()
