ss = str(input())
def palin(ss):
    a = ss[::-1]
    if a == ss:
        print("YES")
    else:
        print("NO")
palin(ss)