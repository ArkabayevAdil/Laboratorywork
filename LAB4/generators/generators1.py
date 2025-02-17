import cmath
def square(n):
    for i in range(n):
        yield i**2
x = int(input("Enter a number: "))
for i in square(x + 1):
    print(i)