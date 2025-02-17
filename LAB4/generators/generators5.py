def rrr(n):
    for i in range(n, -1, -1):
        yield i
n = int(input())
for i in rrr(n):
    print(i)
