def sqq(a , b):
    for i in range(a, b):
        yield i**2
a = int(input())
b = int(input())
for i in sqq(a, b):
    print(i)