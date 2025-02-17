def even(n):
    for i in range(n):
        if i % 2 == 0:
            yield i

x = int(input("Enter a number: "))
for i in even(x + 1):
    print(i)