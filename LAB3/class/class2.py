class Shape():
    def area(self):
        print("area equals 0")

class Square(Shape):
    def __init__ (self, lenght):
        self.lenght = lenght
    def area(self):
        print("area equals", self.lenght**2)

print("Enter the lenght of the square: ")
x = Square(int(input()))
y = Shape()
x.area()
y.area()                
