class Shape():
    def area(self):
        print("area equals 0")

class Rectangle(Shape):
    def __init__(self, length, width): 
        self.length = length
        self.width = width

    def area(self):
        print("area equals: ", self.length * self.width)
print("Enter the length and width of the rectangle: ")
length = int(input())  
width = int(input())   
x = Rectangle(length, width)
x.area()  

