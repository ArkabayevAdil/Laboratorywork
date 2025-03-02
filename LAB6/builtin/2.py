ss = input()
upper = 0
lower = 0
for i in ss:
    if i.isupper():
        upper += 1
    if i.islower():
        lower += 1
print("Upper numbers: ", upper)
print("Lower numbers: ", lower)