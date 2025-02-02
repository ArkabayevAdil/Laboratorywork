set = list(input().split())
def unique(set):
    res = []
    for i in set:
        if i not in res:
            res.append(i)
    ee = " ".join(res)
    print(ee)
unique(set)