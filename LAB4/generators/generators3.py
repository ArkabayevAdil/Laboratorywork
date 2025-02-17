def nnn(x):
    for i in range(x):
        if i%3 + i%4 == 0:
            yield i
x = int(input())
for i in nnn(x + 1):
       print(i)