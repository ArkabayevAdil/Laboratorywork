from itertools import permutations
ss = str(input())
def perm(ss):
    for i in permutations(ss):
        print("".join(i))
perm(ss)

