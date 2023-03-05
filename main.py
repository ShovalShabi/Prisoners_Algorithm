# author: itzhik aviv
# https://www.youtube.com/watch?v=iSNsgj1OCLA&ab_channel=Veritasium
import sys
import random
def pr(l, printF):
    n = len(l)
    u = n * [0]
    for j in range(n):
      if printF:
          print ("j =", j)
      v = []
      p = l[j]
      v.append(p)
      for h in range(n):
        success = False
        if printF:
           print("h =", h, " p =", p)
        if p == j and h < (n//2):
           success = True
           u[j] = 1
           break
        else:
            if p == j:
                break
            else:
                p = l[p]
                v.append(p)
      if printF:
         print("list l:", end=" ")
         for o in range(n):
             print(l[o], end=" ")
         print()
         print("list v:", end =" ")
         for g in range(len(v)):
             print (v[g], end = " ")
         print()
         if success:
             print("prisoner number ", j, " succeeded ",
                   "chain length =", (h+1))
         else:
             print("prisoner number ", j, " failed ",
                   "chain length =", (h+1))
    if printF:
        print("number of prisoners that find their number is:",
              sum(u), "\n    from", n, " prisoners.\n")
    if sum(u) == n:
        return True
    else:
        return False

def main(n ,k, printF):
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
    s = 0
    for i in range(k):
        if printF:
            print("round number", (i+1))
        l = n * [0]
        for j in range(n):
            l[j] = j
        random.shuffle(l)
        if pr(l, printF):
            s += 1
    print("n =", n, " k =", k, " s = ", s,
          "\ns / k in % =", 100 * (s / k))
    s = 0
    hn = n / 2
    for i in range(n//2):
        s += 1/((hn) + (i+1))
    print("probability by loop calculate the geometric series:\n",
          "1 - (1/((n/2)+1) + 1/((n/2)+2) + ...) =",
          1-s)
sys.stdout = open("PrisonersReults.txt", "w")
main(100, 100000, False)
sys.stdout.close()
