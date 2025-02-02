print("How legs: ")
legs = int(input())
print("How heads: ")
heads = int(input())
def ss(heads, legs):
    x = (legs - 2*heads)//2
    y = heads - x
    print("Chickens: ", y , "Rabbits: ", x)
ss(heads, legs)
