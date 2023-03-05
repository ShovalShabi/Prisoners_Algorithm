import sys
import random
import threading

   
def run_single_round(n, printF):
    l = list(range(n))
    random.shuffle(l)
    success_list = [False] * n
    for j in range(n):
        if printF:
            print("j =", j)
        p = l[j]
        v = [p]
        for h in range(n):
            if printF:
                print("h =", h, " p =", p)
            if p == j and h < (n // 2):
                success_list[j] = True
                break
            elif p == j:
                break
            else:
                p = l[p]
                v.append(p)
        if printF:
            print("list l:", l)
            print("list v:", v)
            if success_list[j]:
                print("prisoner number ", j, " succeeded ",
                      "chain length =", (h + 1))
            else:
                print("prisoner number ", j, " failed ",
                      "chain length =", (h + 1))
    if printF:
        print("number of prisoners that find their number is:",
              sum(success_list), "\n    from", n, " prisoners.\n")
    return all(success_list)


def run_multiple_rounds(n, k, printF):
    successes = 0
    for i in range(k):
        if printF:
            print("round number", (i + 1))
        if run_single_round(n, printF):
            successes += 1
    return successes / k


def calculate_probability(n):
    hn = n / 2
    s = sum([1 / (hn + i + 1) for i in range(n // 2)])
    return 1 - s


def main(n, k, printF):
    if not isinstance(n, int):
        print("n =", n, " n must be integer.")
        return
    if n < 2:
        print("n =", n, " n must be > 1.")
        return
    if not isinstance(k, int):
        print("k =", k, " k must be integer.")
        return
    if k <= 0:
        print("k =", k, " k must be > 0.")
        return

    threads = []
    for i in range(k):
        t = threading.Thread(target=run_multiple_rounds, args=(n, 1, printF))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

    success_rate = run_multiple_rounds(n, k, printF)
    probability = calculate_probability(n)
    print("n =", n, " k =", k, " success rate = ", success_rate,
          "\nsuccess rate / k in % =", 100 * success_rate,
          "\nprobability by loop calculate the geometric series:\n",
          "1 - (1/((n/2)+1) + 1/((n/2)+2) + ...) =", probability)

