import math
def rec_area(n, a):
    if(n>2):
        r = a/(2*math.tan(math.pi/n))
        return round(a*n*r/2, 2)
    else:
        pass

n =int(input("Input number of sides: "))
a = int(input("Input the length of a side: "))
print("The area of the polygon is: ", rec_area(n, a))